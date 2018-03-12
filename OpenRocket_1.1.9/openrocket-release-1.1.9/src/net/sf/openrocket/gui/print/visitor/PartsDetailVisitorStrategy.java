/*
 * PartsDetailVisitorStrategy.java
 */
package net.sf.openrocket.gui.print.visitor;

import com.itextpdf.text.*;
import com.itextpdf.text.pdf.PdfPCell;
import com.itextpdf.text.pdf.PdfPTable;
import com.itextpdf.text.pdf.PdfWriter;
import net.sf.openrocket.gui.main.ComponentIcons;
import net.sf.openrocket.gui.print.ITextHelper;
import net.sf.openrocket.gui.print.PrintUtilities;
import net.sf.openrocket.gui.print.PrintableFinSet;
import net.sf.openrocket.logging.LogHelper;
import net.sf.openrocket.material.Material;
import net.sf.openrocket.rocketcomponent.*;
import net.sf.openrocket.startup.Application;
import net.sf.openrocket.unit.Unit;
import net.sf.openrocket.unit.UnitGroup;
import net.sf.openrocket.util.Coordinate;

import javax.swing.*;
import java.text.NumberFormat;
import java.util.Collection;
import java.util.List;
import java.util.Set;

/**
 * A visitor strategy for creating documentation about parts details.
 */
public class PartsDetailVisitorStrategy {

    /**
     * The logger.
     */
    private static final LogHelper log = Application.getLogger();

    /**
     * The number of columns in the table.
     */
    private static final int TABLE_COLUMNS = 7;

    /**
     * The parts detail is represented as an iText table.
     */
    PdfPTable grid;

    /**
     * The iText document.
     */
    protected Document document;

    /**
     * The direct iText writer.
     */
    protected PdfWriter writer;

    /**
     * The stages selected.
     */
    protected Set<Integer> stages;

    /**
     * State variable to track the level of hierarchy.
     */
    protected int level = 0;

    private static final String LINES = "Lines: ";
    private static final String MASS = "Mass: ";
    private static final String LEN = "Len: ";
    private static final String THICK = "Thick: ";
    private static final String INNER = "in ";
    private static final String DIAMETER = "Dia";
    private static final String OUTER = "out";
    private static final String WIDTH = "Width";
    private static final String LENGTH = "Length";
    private static final String SHROUD_LINES = "Shroud Lines";
    private static final String AFT_DIAMETER = "Aft Dia: ";
    private static final String FORE_DIAMETER = "Fore Dia: ";
    private static final String PARTS_DETAIL = "Parts Detail";

    /**
     * Construct a strategy for visiting a parts hierarchy for the purposes of collecting details on those parts.
     *
     * @param doc              The iText document
     * @param theWriter        The direct iText writer
     * @param theStagesToVisit The stages to be visited by this strategy
     */
    public PartsDetailVisitorStrategy (Document doc, PdfWriter theWriter, Set<Integer> theStagesToVisit) {
        document = doc;
        writer = theWriter;
        stages = theStagesToVisit;
        PrintUtilities.addText(doc, PrintUtilities.BIG_BOLD, PARTS_DETAIL);
    }

    /**
     * Print the parts detail.
     *
     * @param root  the root component
     */
    public void writeToDocument (final RocketComponent root) {
        goDeep(root.getChildren());
    }

    /**
     * Recurse through the given rocket component.
     *
     * @param theRc an array of rocket components; all children will be visited recursively
     */
    protected void goDeep (final List<RocketComponent> theRc) {
        level++;
        for (RocketComponent rocketComponent : theRc) {
            handle(rocketComponent);
        }
        level--;
    }

    /**
     * Add a line to the detail report based upon the type of the component.
     *
     * @param component  the component to print the detail for
     */
    private void handle (RocketComponent component) {
        //This ugly if-then-else construct is not object oriented.  Originally it was an elegant, and very OO savy, design
        //using the Visitor pattern.  Unfortunately, it was misunderstood and was removed.
        if (component instanceof Stage) {
            try {
                if (grid != null) {
                    document.add(grid);
                }
                document.add(ITextHelper.createPhrase(component.getName()));
                grid = new PdfPTable(TABLE_COLUMNS);
                grid.setWidthPercentage(100);
                grid.setHorizontalAlignment(Element.ALIGN_LEFT);
            }
            catch (DocumentException e) {
            }

            List<RocketComponent> rc = component.getChildren();
            goDeep(rc);
        }
        else if (component instanceof LaunchLug) {
            LaunchLug ll = (LaunchLug) component;
            grid.addCell(iconToImage(component));
            grid.addCell(createNameCell(component.getName(), true));

            grid.addCell(createMaterialCell(ll.getMaterial()));
            grid.addCell(createOuterInnerDiaCell(ll));
            grid.addCell(createLengthCell(component.getLength()));
            grid.addCell(createMassCell(component.getMass()));
        }
        else if (component instanceof NoseCone) {
            NoseCone nc = (NoseCone) component;
            grid.addCell(iconToImage(component));
            grid.addCell(createNameCell(component.getName(), true));
            grid.addCell(createMaterialCell(nc.getMaterial()));
            grid.addCell(ITextHelper.createCell(nc.getType().getName(), PdfPCell.BOTTOM));
            grid.addCell(createLengthCell(component.getLength()));
            grid.addCell(createMassCell(component.getMass()));
            List<RocketComponent> rc = component.getChildren();
            goDeep(rc);
        }
        else if (component instanceof Transition) {
            Transition tran = (Transition) component;
            grid.addCell(iconToImage(component));
            grid.addCell(createNameCell(component.getName(), true));
            grid.addCell(createMaterialCell(tran.getMaterial()));

            Chunk fore = new Chunk(FORE_DIAMETER + toLength(tran.getForeRadius() * 2));
            fore.setFont(new Font(Font.FontFamily.HELVETICA, PrintUtilities.NORMAL_FONT_SIZE));
            Chunk aft = new Chunk(AFT_DIAMETER + toLength(tran.getAftRadius() * 2));
            aft.setFont(new Font(Font.FontFamily.HELVETICA, PrintUtilities.NORMAL_FONT_SIZE));
            final PdfPCell cell = ITextHelper.createCell();
            cell.addElement(fore);
            cell.addElement(aft);
            grid.addCell(cell);
            grid.addCell(createLengthCell(component.getLength()));
            grid.addCell(createMassCell(component.getMass()));

            List<RocketComponent> rc = component.getChildren();
            goDeep(rc);
        }
        else if (component instanceof BodyTube) {
            BodyTube bt = (BodyTube) component;
            grid.addCell(iconToImage(component));
            grid.addCell(createNameCell(component.getName(), true));
            grid.addCell(createMaterialCell(bt.getMaterial()));
            grid.addCell(createOuterInnerDiaCell(bt));
            grid.addCell(createLengthCell(component.getLength()));
            grid.addCell(createMassCell(component.getMass()));
            List<RocketComponent> rc = component.getChildren();
            goDeep(rc);
        }
        else if (component instanceof FinSet) {
            handleFins((FinSet) component);
        }
        else if (component instanceof BodyComponent) {
            grid.addCell(component.getName());
            grid.completeRow();
            List<RocketComponent> rc = component.getChildren();
            goDeep(rc);
        }
        else if (component instanceof ExternalComponent) {
            ExternalComponent ext = (ExternalComponent) component;
            grid.addCell(iconToImage(component));
            grid.addCell(createNameCell(component.getName(), true));

            grid.addCell(createMaterialCell(ext.getMaterial()));
            grid.addCell(ITextHelper.createCell());
            grid.addCell(createLengthCell(component.getLength()));
            grid.addCell(createMassCell(component.getMass()));

            List<RocketComponent> rc = component.getChildren();
            goDeep(rc);
        }
        else if (component instanceof InnerTube) {
            InnerTube it = (InnerTube) component;
            grid.addCell(iconToImage(component));
            final PdfPCell pCell = createNameCell(component.getName(), true);
            grid.addCell(pCell);
            grid.addCell(createMaterialCell(it.getMaterial()));
            grid.addCell(createOuterInnerDiaCell(it));
            grid.addCell(createLengthCell(component.getLength()));
            grid.addCell(createMassCell(component.getMass()));

            List<RocketComponent> rc = component.getChildren();
            goDeep(rc);
        }
        else if (component instanceof RadiusRingComponent) {
            RadiusRingComponent rrc = (RadiusRingComponent) component;
            grid.addCell(iconToImage(component));
            grid.addCell(createNameCell(component.getName(), true));
            grid.addCell(createMaterialCell(rrc.getMaterial()));
            if (component instanceof Bulkhead) {
                grid.addCell(createDiaCell(rrc.getOuterRadius()*2));
            }
            else {
                grid.addCell(createOuterInnerDiaCell(rrc));
            }
            grid.addCell(createLengthCell(component.getLength()));
            grid.addCell(createMassCell(component.getMass()));
            List<RocketComponent> rc = component.getChildren();
            goDeep(rc);
        }
        else if (component instanceof RingComponent) {
            RingComponent ring = (RingComponent) component;
            grid.addCell(iconToImage(component));
            grid.addCell(createNameCell(component.getName(), true));
            grid.addCell(createMaterialCell(ring.getMaterial()));
            grid.addCell(createOuterInnerDiaCell(ring));
            grid.addCell(createLengthCell(component.getLength()));
            grid.addCell(createMassCell(component.getMass()));

            List<RocketComponent> rc = component.getChildren();
            goDeep(rc);
        }
        else if (component instanceof ShockCord) {
            ShockCord ring = (ShockCord) component;
            PdfPCell cell = ITextHelper.createCell();
            cell.setVerticalAlignment(PdfPCell.ALIGN_MIDDLE);
            cell.setPaddingBottom(12f);
            grid.addCell(iconToImage(component));
            grid.addCell(createNameCell(component.getName(), true));
            grid.addCell(createMaterialCell(ring.getMaterial()));
            grid.addCell(cell);
            grid.addCell(createLengthCell(ring.getCordLength()));
            grid.addCell(createMassCell(component.getMass()));
        }
        else if (component instanceof Parachute) {
            Parachute chute = (Parachute) component;
            PdfPCell cell = ITextHelper.createCell();
            cell.setVerticalAlignment(PdfPCell.ALIGN_MIDDLE);
            cell.setPaddingBottom(12f);
            grid.addCell(iconToImage(component));
            grid.addCell(createNameCell(component.getName(), true));
            grid.addCell(createMaterialCell(chute.getMaterial()));
            grid.addCell(createDiaCell(chute.getDiameter()));
            grid.addCell(createLengthCell(component.getLength()));
            grid.addCell(createMassCell(component.getMass()));

            grid.addCell(iconToImage(null));
            grid.addCell(createNameCell(SHROUD_LINES, true));
            grid.addCell(createMaterialCell(chute.getLineMaterial()));
            grid.addCell(createLinesCell(chute.getLineCount()));
            grid.addCell(createLengthCell(chute.getLineLength()));
            grid.addCell(cell);
        }
        else if (component instanceof Streamer) {
            Streamer ring = (Streamer) component;
            PdfPCell cell = ITextHelper.createCell();
            cell.setVerticalAlignment(PdfPCell.ALIGN_MIDDLE);
            cell.setPaddingBottom(12f);
            grid.addCell(iconToImage(component));
            grid.addCell(createNameCell(component.getName(), true));
            grid.addCell(createMaterialCell(ring.getMaterial()));
            grid.addCell(createStrip(ring));
            grid.addCell(createLengthCell(component.getLength()));
            grid.addCell(createMassCell(component.getMass()));
        }
        else if (component instanceof RecoveryDevice) {
            RecoveryDevice device = (RecoveryDevice) component;
            PdfPCell cell = ITextHelper.createCell();
            cell.setVerticalAlignment(PdfPCell.ALIGN_MIDDLE);
            cell.setPaddingBottom(12f);
            grid.addCell(iconToImage(component));
            grid.addCell(createNameCell(component.getName(), true));
            grid.addCell(createMaterialCell(device.getMaterial()));
            grid.addCell(cell);
            grid.addCell(createLengthCell(component.getLength()));
            grid.addCell(createMassCell(component.getMass()));
        }
        else if (component instanceof MassObject) {
            PdfPCell cell = ITextHelper.createCell();
            cell.setVerticalAlignment(PdfPCell.ALIGN_MIDDLE);
            cell.setPaddingBottom(12f);

            grid.addCell(iconToImage(component));
            final PdfPCell nameCell = createNameCell(component.getName(), true);
            nameCell.setVerticalAlignment(PdfPCell.ALIGN_MIDDLE);
            nameCell.setPaddingBottom(12f);
            grid.addCell(nameCell);
            grid.addCell(cell);
            grid.addCell(createDiaCell(((MassObject) component).getRadius() * 2));
            grid.addCell(cell);
            grid.addCell(createMassCell(component.getMass()));
        }
    }

    /**
     * Close the strategy by adding the last grid to the document.
     */
    public void close () {
        try {
            if (grid != null) {
                document.add(grid);
            }
        }
        catch (DocumentException e) {
            log.error("Could not write last cell to document.", e);
        }
    }

    /**
     * Create a cell to document an outer 'diameter'.  This is used for components that have no inner diameter, such as
     * a solid parachute or bulkhead.
     *
     * @param diameter  the diameter in default length units
     *
     * @return a formatted cell containing the diameter
     */
    private PdfPCell createDiaCell (final double diameter) {
        PdfPCell result = new PdfPCell();
        Phrase p = new Phrase();
        p.setLeading(12f);
        result.setVerticalAlignment(Element.ALIGN_TOP);
        result.setBorder(Rectangle.BOTTOM);
        Chunk c = new Chunk();
        c.setFont(new Font(Font.FontFamily.HELVETICA, PrintUtilities.NORMAL_FONT_SIZE));
        c.append(DIAMETER);
        p.add(c);

        c = new Chunk();
        c.setFont(new Font(Font.FontFamily.HELVETICA, PrintUtilities.SMALL_FONT_SIZE));
        c.append(OUTER);
        p.add(c);

        c = new Chunk();
        c.setFont(new Font(Font.FontFamily.HELVETICA, PrintUtilities.NORMAL_FONT_SIZE));
        c.append(" " + toLength(diameter));
        p.add(c);
        result.addElement(p);
        return result;
    }

    /**
     * Create a PDF cell for a streamer.
     *
     * @param component  a component that is a Coaxial
     * @return  the PDF cell that has the streamer documented
     */
    private PdfPCell createStrip (final Streamer component) {
        PdfPCell result = new PdfPCell();
        Phrase p = new Phrase();
        p.setLeading(12f);
        result.setVerticalAlignment(Element.ALIGN_TOP);
        result.setBorder(Rectangle.BOTTOM);
        Chunk c = new Chunk();
        c.setFont(new Font(Font.FontFamily.HELVETICA, PrintUtilities.NORMAL_FONT_SIZE));
        c.append(LENGTH);
        p.add(c);

        c = new Chunk();
        c.setFont(new Font(Font.FontFamily.HELVETICA, PrintUtilities.NORMAL_FONT_SIZE));
        c.append(" " + toLength(component.getStripLength()));
        p.add(c);
        result.addElement(p);

        Phrase pw = new Phrase();
        pw.setLeading(14f);
        c = new Chunk();
        c.setFont(new Font(Font.FontFamily.HELVETICA, PrintUtilities.NORMAL_FONT_SIZE));
        c.append(WIDTH);
        pw.add(c);

        c = new Chunk();
        c.setFont(new Font(Font.FontFamily.HELVETICA, PrintUtilities.NORMAL_FONT_SIZE));
        c.append("  " + toLength(component.getStripWidth()));
        pw.add(c);
        result.addElement(pw);

        return result;
    }

    /**
     * Create a PDF cell that documents both an outer and an inner diameter of a component.
     *
     * @param component  a component that is a Coaxial
     * @return  the PDF cell that has the outer and inner diameters documented
     */
    private PdfPCell createOuterInnerDiaCell (final Coaxial component) {
        PdfPCell result = new PdfPCell();
        Phrase p = new Phrase();
        p.setLeading(12f);
        result.setVerticalAlignment(Element.ALIGN_TOP);
        result.setBorder(Rectangle.BOTTOM);
        Chunk c = new Chunk();
        c.setFont(new Font(Font.FontFamily.HELVETICA, PrintUtilities.NORMAL_FONT_SIZE));
        c.append(DIAMETER);
        p.add(c);

        c = new Chunk();
        c.setFont(new Font(Font.FontFamily.HELVETICA, PrintUtilities.SMALL_FONT_SIZE));
        c.append(OUTER);
        p.add(c);

        c = new Chunk();
        c.setFont(new Font(Font.FontFamily.HELVETICA, PrintUtilities.NORMAL_FONT_SIZE));
        c.append(" " + toLength(component.getOuterRadius() * 2));
        p.add(c);
        createInnerDiaCell(component, result);
        result.addElement(p);
        return result;
    }

    /**
     * Add inner diameter data to a cell.
     *
     * @param component  a component that is a Coaxial
     * @param cell       the PDF cell to add the inner diameter data to
     */
    private void createInnerDiaCell (final Coaxial component, PdfPCell cell) {
        Phrase p = new Phrase();
        p.setLeading(14f);
        Chunk c = new Chunk();
        c.setFont(new Font(Font.FontFamily.HELVETICA, PrintUtilities.NORMAL_FONT_SIZE));
        c.append(DIAMETER);
        p.add(c);

        c = new Chunk();
        c.setFont(new Font(Font.FontFamily.HELVETICA, PrintUtilities.SMALL_FONT_SIZE));
        c.append(INNER);
        p.add(c);

        c = new Chunk();
        c.setFont(new Font(Font.FontFamily.HELVETICA, PrintUtilities.NORMAL_FONT_SIZE));
        c.append("  " + toLength(component.getInnerRadius() * 2));
        p.add(c);
        cell.addElement(p);
    }

    /**
     * Add PDF cells for a fin set.
     *
     * @param theFinSet  the fin set
     */
    private void handleFins (FinSet theFinSet) {

        Image img = null;
        java.awt.Image awtImage = new PrintableFinSet(theFinSet).createImage();

        Collection<Coordinate> x = theFinSet.getComponentBounds();

        try {
            img = Image.getInstance(writer, awtImage, 0.25f);
        }
        catch (Exception e) {
            log.error("Could not write image to document.", e);
        }

        grid.addCell(iconToImage(theFinSet));
        grid.addCell(createNameCell(theFinSet.getName() + " (" + theFinSet.getFinCount() + ")", true));
        grid.addCell(createMaterialCell(theFinSet.getMaterial()));
        grid.addCell(ITextHelper.createCell(THICK + toLength(theFinSet.getThickness()), PdfPCell.BOTTOM));
        final PdfPCell pCell = new PdfPCell();
        pCell.setBorder(Rectangle.BOTTOM);
        pCell.addElement(img);

        grid.addCell(ITextHelper.createCell());
        grid.addCell(createMassCell(theFinSet.getMass()));

        List<RocketComponent> rc = theFinSet.getChildren();
        goDeep(rc);
    }

    /**
     * Create a length formatted cell.
     *
     * @param length  the length, in default length units
     *
     * @return a PdfPCell that is formatted with the length
     */
    protected PdfPCell createLengthCell (double length) {
        return ITextHelper.createCell(LEN + toLength(length), PdfPCell.BOTTOM);
    }

    /**
     * Create a mass formatted cell.
     *
     * @param mass  the mass, in default mass units
     *
     * @return a PdfPCell that is formatted with the mass
     */
    protected PdfPCell createMassCell (double mass) {
        return ITextHelper.createCell(MASS + toMass(mass), PdfPCell.BOTTOM);
    }

    /**
     * Create a (shroud) line count formatted cell.
     *
     * @param count  the number of shroud lines
     *
     * @return a PdfPCell that is formatted with the line count
     */
    protected PdfPCell createLinesCell (int count) {
        return ITextHelper.createCell(LINES + count, PdfPCell.BOTTOM);
    }

    /**
     * Create a cell formatted for a name (or any string for that matter).
     *
     * @param v  the string to format into a PDF cell
     * @param withIndent  if true, then an indention is made scaled to the level of the part in the parent hierarchy
     *
     * @return a PdfPCell that is formatted with the string <code>v</code>
     */
    protected PdfPCell createNameCell (String v, boolean withIndent) {
        PdfPCell result = new PdfPCell();
        result.setBorder(Rectangle.BOTTOM);
        Chunk c = new Chunk();
        c.setFont(new Font(Font.FontFamily.HELVETICA, PrintUtilities.NORMAL_FONT_SIZE));
        if (withIndent) {
            for (int x = 0; x < (level - 2) * 10; x++) {
                c.append(" ");
            }
        }
        c.append(v);
        result.setColspan(2);
        result.addElement(c);
        return result;
    }

    /**
     * Create a cell that describes a material.
     *
     * @param material  the material
     *
     * @return a PdfPCell that is formatted with a description of the material
     */
    protected PdfPCell createMaterialCell (Material material) {
        PdfPCell cell = ITextHelper.createCell();
        cell.setLeading(13f, 0);

        Chunk c = new Chunk();
        c.setFont(new Font(Font.FontFamily.HELVETICA, PrintUtilities.NORMAL_FONT_SIZE));
        c.append(toMaterialName(material));
        cell.addElement(c);
        Chunk density = new Chunk();
        density.setFont(new Font(Font.FontFamily.HELVETICA, PrintUtilities.SMALL_FONT_SIZE));
        density.append(toMaterialDensity(material));
        cell.addElement(density);
        return cell;
    }

    /**
     * Get the icon of the particular type of rocket component and conver it to an image in a PDF cell.
     *
     * @param visitable  the rocket component to create a cell with it's image
     *
     * @return a PdfPCell that is just an image that can be put into a PDF
     */
    protected PdfPCell iconToImage (final RocketComponent visitable) {
        if (visitable != null) {
            final ImageIcon icon = (ImageIcon) ComponentIcons.getLargeIcon(visitable.getClass());
            try {
                if (icon != null) {
                    Image im = Image.getInstance(icon.getImage(), null);
                    if (im != null) {
                        im.scaleToFit(icon.getIconWidth() * 0.6f, icon.getIconHeight() * 0.6f);
                        PdfPCell cell = new PdfPCell(im);
                        cell.setFixedHeight(icon.getIconHeight() * 0.6f);
                        cell.setHorizontalAlignment(PdfPCell.ALIGN_CENTER);
                        cell.setVerticalAlignment(PdfPCell.ALIGN_MIDDLE);
                        cell.setBorder(PdfPCell.NO_BORDER);
                        return cell;
                    }
                }
            }
            catch (Exception e) {
            }
        }
        PdfPCell cell = new PdfPCell();
        cell.setHorizontalAlignment(PdfPCell.ALIGN_CENTER);
        cell.setVerticalAlignment(PdfPCell.ALIGN_MIDDLE);
        cell.setBorder(PdfPCell.NO_BORDER);
        return cell;
    }

    /**
     * Format the length as a displayable string.
     *
     * @param length the length (assumed to be in default length units)
     *
     * @return a string representation of the length with unit abbreviation
     */
    protected String toLength (double length) {
        final Unit defaultUnit = UnitGroup.UNITS_LENGTH.getDefaultUnit();
        return NumberFormat.getNumberInstance().format(defaultUnit.toUnit(length)) + defaultUnit.toString();
    }

    /**
     * Format the mass as a displayable string.
     *
     * @param mass  the mass (assumed to be in default mass units)
     *
     * @return a string representation of the mass with mass abbreviation
     */
    protected String toMass (double mass) {
        final Unit defaultUnit = UnitGroup.UNITS_MASS.getDefaultUnit();
        return NumberFormat.getNumberInstance().format(defaultUnit.toUnit(mass)) + defaultUnit.toString();
    }

    /**
     * Get a displayable string of the material's name.
     *
     * @param material  the material to output
     *
     * @return the material name
     */
    protected String toMaterialName (Material material) {
        return material.getName();
    }

    /**
     * Format the material density as a displayable string.
     *
     * @param material  the material to output
     *
     * @return a string representation of the material density
     */
    protected String toMaterialDensity (Material material) {
        return " (" + material.getType().getUnitGroup().getDefaultUnit().toStringUnit(material.getDensity()) + ")";
    }

}
