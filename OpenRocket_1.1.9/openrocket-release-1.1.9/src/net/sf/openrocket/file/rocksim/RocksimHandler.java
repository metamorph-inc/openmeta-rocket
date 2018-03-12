/*
 * RocksimHandler.java
 *
 */
package net.sf.openrocket.file.rocksim;

import net.sf.openrocket.aerodynamics.Warning;
import net.sf.openrocket.aerodynamics.WarningSet;
import net.sf.openrocket.document.OpenRocketDocument;
import net.sf.openrocket.file.simplesax.ElementHandler;
import net.sf.openrocket.file.simplesax.PlainTextHandler;
import net.sf.openrocket.rocketcomponent.Rocket;
import net.sf.openrocket.rocketcomponent.RocketComponent;
import net.sf.openrocket.rocketcomponent.Stage;
import org.xml.sax.SAXException;

import java.util.HashMap;

/**
 * This class is a Sax element handler for Rocksim version 9 design files.  It parses the Rocksim file (typically
 * a .rkt extension) and creates corresponding OpenRocket components.  This is a best effort approach and may not
 * be an exact replica.
 * <p/>
 * Limitations: Rocksim flight simulations are not imported; tube fins are not supported; Rocksim 'pods' are not supported.
 */
public class RocksimHandler extends ElementHandler {

    /**
     * Length conversion.  Rocksim is in millimeters, OpenRocket in meters.
     */
    public static final int ROCKSIM_TO_OPENROCKET_LENGTH = 1000;

    /**
     * Mass conversion.  Rocksim is in grams, OpenRocket in kilograms.
     */
    public static final int ROCKSIM_TO_OPENROCKET_MASS = 1000;

    /**
     * Bulk Density conversion.  Rocksim is in kilograms/cubic meter, OpenRocket in kilograms/cubic meter.
     */
    public static final int ROCKSIM_TO_OPENROCKET_BULK_DENSITY = 1;

    /**
     * Surface Density conversion.  Rocksim is in grams/sq centimeter, OpenRocket in kilograms/sq meter.  1000/(100*100) = 1/10
     */
    public static final double ROCKSIM_TO_OPENROCKET_SURFACE_DENSITY = 1/10d;

    /**
     * Line Density conversion.  Rocksim is in kilograms/meter, OpenRocket in kilograms/meter. 
     */
    public static final int ROCKSIM_TO_OPENROCKET_LINE_DENSITY = 1;

    /**
     * Radius conversion.  Rocksim is always in diameters, OpenRocket mostly in radius.
     */
    public static final int ROCKSIM_TO_OPENROCKET_RADIUS = 2 * ROCKSIM_TO_OPENROCKET_LENGTH;

    /**
     * The main content handler.
     */
    private RocksimContentHandler handler = null;

    /**
     * Return the OpenRocketDocument read from the file, or <code>null</code> if a document
     * has not been read yet.
     *
     * @return the document read, or null.
     */
    public OpenRocketDocument getDocument() {
        return handler.getDocument();
    }

    @Override
    public ElementHandler openElement(String element, HashMap<String, String> attributes,
                                      WarningSet warnings) {

        // Check for unknown elements
        if (!element.equals("RockSimDocument")) {
            warnings.add(Warning.fromString("Unknown element " + element + ", ignoring."));
            return null;
        }

        // Check for first call
        if (handler != null) {
            warnings.add(Warning.fromString("Multiple document elements found, ignoring later "
                                            + "ones."));
            return null;
        }

        handler = new RocksimContentHandler();
        return handler;
    }

}

/**
 * Handles the content of the <DesignInformation> tag.
 */
class RocksimContentHandler extends ElementHandler {
    /**
     * The OpenRocketDocument that is the container for the rocket.
     */
    private final OpenRocketDocument doc;

    /**
     * The top-level component, from which all child components are added.
     */
    private final Rocket rocket;

    /**
     * The rocksim file version.
     */
    private String version;

    /**
     * Constructor.
     */
    public RocksimContentHandler() {
        this.rocket = new Rocket();
        this.doc = new OpenRocketDocument(rocket);
    }

    /**
     * Get the OpenRocket document that has been created from parsing the Rocksim design file.
     *
     * @return the instantiated OpenRocketDocument
     */
    public OpenRocketDocument getDocument() {
        return doc;
    }

    @Override
    public ElementHandler openElement(String element, HashMap<String, String> attributes,
                                      WarningSet warnings) {
        if ("DesignInformation".equals(element)) {
            //The next sub-element is "RocketDesign", which is really the only thing that matters.  Rather than
            //create another handler just for that element, handle it here.
            return this;
        }
        if ("FileVersion".equals(element)) {
            return PlainTextHandler.INSTANCE;
        }
        if ("RocketDesign".equals(element)) {
            return new RocketDesignHandler(rocket);
        }
        return null;
    }

    @Override
    public void closeElement(String element, HashMap<String, String> attributes,
                             String content, WarningSet warnings) throws SAXException {
        /**
         * SAX handler for Rocksim file version number.  The value is not used currently, but could be used in the future
         * for backward/forward compatibility reasons (different lower level handlers could be called via a strategy pattern).
         */
        if ("FileVersion".equals(element)) {
            version = content;
        }
    }

    /**
     * Answer the file version.
     *
     * @return the version of the Rocksim design file
     */
    public String getVersion() {
        return version;
    }
}


/**
 * A SAX handler for the high level Rocksim design.  This structure includes sub-structures for each of the stages.
 * Correct functioning of this handler is predicated on the stage count element appearing before the actual stage parts
 * structures.  If that invariant is not true, then behavior will be unpredictable.
 */
class RocketDesignHandler extends ElementHandler {
    /**
     * The parent component.
     */
    private final RocketComponent component;
    /**
     * The parsed stage count.  Defaults to 1.
     */
    private int stageCount = 1;
    /**
     * The overridden stage 1 mass.
     */
    private double stage1Mass = 0d;
    /**
     * The overridden stage 2 mass.
     */
    private double stage2Mass = 0d;
    /**
     * The overridden stage 3 mass.
     */
    private double stage3Mass = 0d;
    /**
     * The overridden stage 1 Cg.
     */
    private double stage1CG = 0d;
    /**
     * The overridden stage 2 Cg.
     */
    private double stage2CG = 0d;
    /**
     * The overridden stage 3 Cg.
     */
    private double stage3CG = 0d;

    /**
     * Constructor.
     *
     * @param c the parent component
     */
    public RocketDesignHandler(RocketComponent c) {
        component = c;
    }

    @Override
    public ElementHandler openElement(String element, HashMap<String, String> attributes, WarningSet warnings) {
        /**
         * In Rocksim stages are from the top down, so a single stage rocket is actually stage '3'.  A 2-stage
         * rocket defines stage '2' as the initial booster with stage '3' sitting atop it.  And so on.
         */
        if ("Stage3Parts".equals(element)) {
            final Stage stage = new Stage();
            if (stage3Mass > 0.0d) {
                stage.setMassOverridden(true);
                stage.setOverrideSubcomponents(true); //Rocksim does not support this type of override
                stage.setOverrideMass(stage3Mass);
            }
            if (stage3CG > 0.0d) {
                stage.setCGOverridden(true);
                stage.setOverrideSubcomponents(true); //Rocksim does not support this type of override
                stage.setOverrideCGX(stage3CG);
            }
            component.addChild(stage);
            return new StageHandler(stage);
        }
        if ("Stage2Parts".equals(element)) {
            if (stageCount >= 2) {
                final Stage stage = new Stage();
                if (stage2Mass > 0.0d) {
                    stage.setMassOverridden(true);
                    stage.setOverrideSubcomponents(true); //Rocksim does not support this type of override
                    stage.setOverrideMass(stage2Mass);
                }
                if (stage2CG > 0.0d) {
                    stage.setCGOverridden(true);
                    stage.setOverrideSubcomponents(true); //Rocksim does not support this type of override
                    stage.setOverrideCGX(stage2CG);
                }
                component.addChild(stage);
                return new StageHandler(stage);
            }
        }
        if ("Stage1Parts".equals(element)) {
            if (stageCount == 3) {
                final Stage stage = new Stage();
                if (stage1Mass > 0.0d) {
                    stage.setMassOverridden(true);
                    stage.setOverrideSubcomponents(true); //Rocksim does not support this type of override
                    stage.setOverrideMass(stage1Mass);
                }
                if (stage1CG > 0.0d) {
                    stage.setCGOverridden(true);
                    stage.setOverrideSubcomponents(true); //Rocksim does not support this type of override
                    stage.setOverrideCGX(stage1CG);
                }
                component.addChild(stage);
                return new StageHandler(stage);
            }
        }
        if ("Name".equals(element)) {
            return PlainTextHandler.INSTANCE;
        }
        if ("StageCount".equals(element)) {
            return PlainTextHandler.INSTANCE;
        }
        if ("Stage3Mass".equals(element)) {
            return PlainTextHandler.INSTANCE;
        }
        if ("Stage2Mass".equals(element)) {
            return PlainTextHandler.INSTANCE;
        }
        if ("Stage1Mass".equals(element)) {
            return PlainTextHandler.INSTANCE;
        }
        if ("Stage3CG".equals(element)) {
            return PlainTextHandler.INSTANCE;
        }
        if ("Stage2CGAlone".equals(element)) {
            return PlainTextHandler.INSTANCE;
        }
        if ("Stage1CGAlone".equals(element)) {
            return PlainTextHandler.INSTANCE;
        }
        return null;
    }

    @Override
    public void closeElement(String element, HashMap<String, String> attributes,
                             String content, WarningSet warnings) throws SAXException {
        try {
            if ("Name".equals(element)) {
                component.setName(content);
            }
            if ("StageCount".equals(element)) {
                stageCount = Integer.parseInt(content);
            }
            if ("Stage3Mass".equals(element)) {
                stage3Mass = Double.parseDouble(content) / RocksimHandler.ROCKSIM_TO_OPENROCKET_MASS;
            }
            if ("Stage2Mass".equals(element)) {
                stage2Mass = Double.parseDouble(content) / RocksimHandler.ROCKSIM_TO_OPENROCKET_MASS;
            }
            if ("Stage1Mass".equals(element)) {
                stage1Mass = Double.parseDouble(content) / RocksimHandler.ROCKSIM_TO_OPENROCKET_MASS;
            }
            if ("Stage3CG".equals(element)) {
                stage3CG = Double.parseDouble(content) / RocksimHandler.ROCKSIM_TO_OPENROCKET_LENGTH;
            }
            if ("Stage2CGAlone".equals(element)) {
                stage2CG = Double.parseDouble(content) / RocksimHandler.ROCKSIM_TO_OPENROCKET_LENGTH;
            }
            if ("Stage1CGAlone".equals(element)) {
                stage1CG = Double.parseDouble(content) / RocksimHandler.ROCKSIM_TO_OPENROCKET_LENGTH;
            }
        }
        catch (NumberFormatException nfe) {
            warnings.add("Could not convert " + element + " value of " + content + ".  It is expected to be a number.");
        }
    }

}

/**
 * A SAX handler for a Rocksim stage.
 */
class StageHandler extends ElementHandler {
    /**
     * The parent OpenRocket component.
     */
    private final RocketComponent component;

    /**
     * Constructor.
     *
     * @param c the parent component
     * @throws IllegalArgumentException thrown if <code>c</code> is null
     */
    public StageHandler(RocketComponent c) throws IllegalArgumentException {
        if (c == null) {
            throw new IllegalArgumentException("The stage component may not be null.");
        }
        component = c;
    }

    @Override
    public ElementHandler openElement(String element, HashMap<String, String> attributes, WarningSet warnings) {
        if ("NoseCone".equals(element)) {
            return new NoseConeHandler(component, warnings);
        }
        if ("BodyTube".equals(element)) {
            return new BodyTubeHandler(component, warnings);
        }
        if ("Transition".equals(element)) {
            return new TransitionHandler(component, warnings);
        }
        return null;
    }
}
