/*
 * PrintableFinSet.java
 */
package net.sf.openrocket.gui.print;

import net.sf.openrocket.rocketcomponent.FinSet;
import net.sf.openrocket.util.Coordinate;

import javax.swing.*;
import java.awt.*;
import java.awt.geom.GeneralPath;
import java.awt.image.BufferedImage;
import java.awt.print.PageFormat;
import java.awt.print.Printable;
import java.awt.print.PrinterException;

/**
 * This class allows for a FinSet to be printable.  It does so by decorating an existing finset (which will not be
 * modified) and rendering it within a JPanel.  The JPanel is not actually visualized on a display, but instead renders
 * it to a print device.
 */
public class PrintableFinSet extends JPanel implements Printable {

    /**
     * The object that represents the shape (outline) of the fin.  This gets drawn onto the Swing component.
     */
    protected GeneralPath polygon = null;

    /**
     * The X margin.
     */
    private final int marginX = (int)(PrintUnit.POINTS_PER_INCH * 0.3f);
    /**
     * The Y margin.
     */
    private final int marginY = (int)(PrintUnit.POINTS_PER_INCH * 0.3f);
    /**
     * The minimum X coordinate.
     */
    private int minX = 0;
    /**
     * The minimum Y coordinate.
     */
    private int minY = 0;

    /**
     * Constructor.
     *
     * @param fs the finset to print
     */
    public PrintableFinSet (FinSet fs) {
        this(fs.getFinPointsWithTab());
    }

    /**
     * Construct a fin set from a set of points.
     *
     * @param points an array of points.
     */
    public PrintableFinSet (Coordinate[] points) {
        super(false);
        init(points);
        setBackground(Color.white);
    }

    /**
     * Initialize the fin set polygon and set the size of the component.
     *
     * @param points an array of points.
     */
    private void init (Coordinate[] points) {

        polygon = new GeneralPath(GeneralPath.WIND_EVEN_ODD, points.length);
        polygon.moveTo(0, 0);

        int maxX = 0;
        int maxY = 0;

        for (Coordinate point : points) {
            final long x = PrintUnit.METERS.toPoints(point.x);
            final long y = PrintUnit.METERS.toPoints(point.y);
            minX = (int) Math.min(x, minX);
            minY = (int) Math.min(y, minY);
            maxX = (int) Math.max(x, maxX);
            maxY = (int) Math.max(y, maxY);
            polygon.lineTo(x, y);
        }
        polygon.closePath();

        setSize(maxX - minX, maxY - minY);
    }

    /**
     * Get the X-axis margin value.
     *
     * @return margin, in points
     */
    protected double getMarginX () {
        return marginX;
    }

    /**
     * Get the Y-axis margin value.
     *
     * @return margin, in points
     */
    protected double getMarginY () {
        return marginY;
    }

    /**
     * From the java.awt.print.Printable interface.
     * <p/>
     * Prints the page at the specified index into the specified {@link java.awt.Graphics} context in the specified
     * format. A <code>PrinterJob</code> calls the <code>Printable</code> interface to request that a page be rendered
     * into the context specified by <code>graphics</code>.  The format of the page to be drawn is specified by
     * <code>pageFormat</code>.  The zero based index of the requested page is specified by <code>pageIndex</code>. If
     * the requested page does not exist then this method returns NO_SUCH_PAGE; otherwise PAGE_EXISTS is returned. The
     * <code>Graphics</code> class or subclass implements the {@link java.awt.print.PrinterGraphics} interface to
     * provide additional information.  If the <code>Printable</code> object aborts the print job then it throws a
     * {@link java.awt.print.PrinterException}.
     * <p/>
     * Note: This is not currently used in OpenRocket.  It's only here for reference.
     *
     * @param graphics   the context into which the page is drawn
     * @param pageFormat the size and orientation of the page being drawn
     * @param pageIndex  the zero based index of the page to be drawn
     *
     * @return PAGE_EXISTS if the page is rendered successfully or NO_SUCH_PAGE if <code>pageIndex</code> specifies a
     *         non-existent page.
     *
     * @throws java.awt.print.PrinterException
     *          thrown when the print job is terminated.
     */
    @Override
    public int print (final Graphics graphics, final PageFormat pageFormat, final int pageIndex)
            throws PrinterException {

        Graphics2D g2d = (Graphics2D) graphics;
        PrintUtilities.translateToJavaOrigin(g2d, pageFormat);
        PrintUtilities.disableDoubleBuffering(this);
        paint(g2d);
        PrintUtilities.enableDoubleBuffering(this);
        return Printable.PAGE_EXISTS;
    }

    /**
     * Returns a generated image of the fin set.  May then be used wherever AWT images can be used, or converted to
     * another image/picture format and used accordingly.
     *
     * @return an awt image of the fin set
     */
    public Image createImage () {
        int width = getWidth() + marginX;
        int height = getHeight() + marginY;
        // Create a buffered image in which to draw 
        BufferedImage bufferedImage = new BufferedImage(width, height, BufferedImage.TYPE_INT_ARGB);
        // Create a graphics contents on the buffered image 
        Graphics2D g2d = bufferedImage.createGraphics();
        // Draw graphics 
        g2d.setBackground(Color.white);
        g2d.clearRect(0, 0, width, height);
        paintComponent(g2d);
        // Graphics context no longer needed so dispose it 
        g2d.dispose();
        return bufferedImage;
    }

    /**
     * Render the fin set onto the graphics context.  This is done by creating a GeneralPath component that follows the
     * outline of the fin set coordinates to create a polygon, which is then drawn onto the graphics context.
     * Through-the-wall fin tabs are supported if they are present.
     *
     * @param g the Java2D graphics context
     */
    @Override
    public void paintComponent (Graphics g) {
        super.paintComponent(g);
        Graphics2D g2d = (Graphics2D) g;

        int x = 0;
        int y = 0;

        // The minimum X/Y can be negative (primarily only Y due to fin tabs; rarely (never) X, but protect both anyway).
        if (minX < marginX) {
            x = marginX + Math.abs(minX);
        }
        if (minY < marginY) {
            y = marginY + Math.abs(minY);
        }
        // Reset the origin.
        g2d.translate(x, y);
        g2d.setPaint(TemplateProperties.getFillColor());
        g2d.fill(polygon);
        g2d.setPaint(TemplateProperties.getLineColor());
        g2d.draw(polygon);
    }

}
