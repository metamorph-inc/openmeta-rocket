package net.sf.openrocket.gui.configdialog;


import java.awt.Color;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.event.FocusEvent;
import java.awt.event.FocusListener;
import java.util.ArrayList;
import java.util.Iterator;
import java.util.List;

import javax.swing.BorderFactory;
import javax.swing.JButton;
import javax.swing.JCheckBox;
import javax.swing.JColorChooser;
import javax.swing.JComboBox;
import javax.swing.JLabel;
import javax.swing.JPanel;
import javax.swing.JScrollPane;
import javax.swing.JSpinner;
import javax.swing.JTabbedPane;
import javax.swing.JTextArea;
import javax.swing.JTextField;

import net.miginfocom.swing.MigLayout;
import net.sf.openrocket.document.OpenRocketDocument;
import net.sf.openrocket.gui.SpinnerEditor;
import net.sf.openrocket.gui.adaptors.BooleanModel;
import net.sf.openrocket.gui.adaptors.DoubleModel;
import net.sf.openrocket.gui.adaptors.EnumModel;
import net.sf.openrocket.gui.adaptors.MaterialModel;
import net.sf.openrocket.gui.components.BasicSlider;
import net.sf.openrocket.gui.components.ColorIcon;
import net.sf.openrocket.gui.components.StyledLabel;
import net.sf.openrocket.gui.components.StyledLabel.Style;
import net.sf.openrocket.gui.components.UnitSelector;
import net.sf.openrocket.l10n.Translator;
import net.sf.openrocket.material.Material;
import net.sf.openrocket.rocketcomponent.ComponentAssembly;
import net.sf.openrocket.rocketcomponent.ExternalComponent;
import net.sf.openrocket.rocketcomponent.ExternalComponent.Finish;
import net.sf.openrocket.rocketcomponent.NoseCone;
import net.sf.openrocket.rocketcomponent.RocketComponent;
import net.sf.openrocket.startup.Application;
import net.sf.openrocket.unit.UnitGroup;
import net.sf.openrocket.util.GUIUtil;
import net.sf.openrocket.util.Invalidatable;
import net.sf.openrocket.util.LineStyle;
import net.sf.openrocket.util.Prefs;

public class RocketComponentConfig extends JPanel {
	
	private static final Translator trans = Application.getTranslator();
	
	protected final OpenRocketDocument document;
	protected final RocketComponent component;
	protected final JTabbedPane tabbedPane;
	
	private final List<Invalidatable> invalidatables = new ArrayList<Invalidatable>();
	

	protected final JTextField componentNameField;
	protected JTextArea commentTextArea;
	private final TextFieldListener textFieldListener;
	private JButton colorButton;
	private JCheckBox colorDefault;
	private JPanel buttonPanel;
	
	private JLabel massLabel;
	
	
	public RocketComponentConfig(OpenRocketDocument document, RocketComponent component) {
		setLayout(new MigLayout("fill", "[grow, fill]"));
		this.document = document;
		this.component = component;
		
		//// Component name:
		JLabel label = new JLabel(trans.get("RocketCompCfg.lbl.Componentname"));
		//// The component name.
		label.setToolTipText(trans.get("RocketCompCfg.ttip.Thecomponentname"));
		this.add(label, "split, gapright 10");
		
		componentNameField = new JTextField(15);
		textFieldListener = new TextFieldListener();
		componentNameField.addActionListener(textFieldListener);
		componentNameField.addFocusListener(textFieldListener);
		//// The component name.
		componentNameField.setToolTipText(trans.get("RocketCompCfg.ttip.Thecomponentname"));
		this.add(componentNameField, "growx, growy 0, wrap");
		

		tabbedPane = new JTabbedPane();
		this.add(tabbedPane, "growx, growy 1, wrap");
		
		//// Override and Mass and CG override options
		tabbedPane.addTab(trans.get("RocketCompCfg.tab.Override"), null, overrideTab(),
				trans.get("RocketCompCfg.tab.MassandCGoverride"));
		if (component.isMassive())
			//// Figure and Figure style options
			tabbedPane.addTab(trans.get("RocketCompCfg.tab.Figure"), null, figureTab(),
					trans.get("RocketCompCfg.tab.Figstyleopt"));
		//// Comment and Specify a comment for the component
		tabbedPane.addTab(trans.get("RocketCompCfg.tab.Comment"), null, commentTab(),
				trans.get("RocketCompCfg.tab.Specifyacomment"));
		
		addButtons();
		
		updateFields();
	}
	
	
	protected void addButtons(JButton... buttons) {
		if (buttonPanel != null) {
			this.remove(buttonPanel);
		}
		
		buttonPanel = new JPanel(new MigLayout("fill, ins 0"));
		
		//// Mass:
		massLabel = new StyledLabel(trans.get("RocketCompCfg.lbl.Mass") + " ", -1);
		buttonPanel.add(massLabel, "growx");
		
		for (JButton b : buttons) {
			buttonPanel.add(b, "right, gap para");
		}
		
		//// Close button
		JButton closeButton = new JButton(trans.get("dlg.but.close"));
		closeButton.addActionListener(new ActionListener() {
			@Override
			public void actionPerformed(ActionEvent arg0) {
				ComponentConfigDialog.hideDialog();
			}
		});
		buttonPanel.add(closeButton, "right, gap 30lp");
		
		updateFields();
		
		this.add(buttonPanel, "spanx, growx");
	}
	
	
	/**
	 * Called when a change occurs, so that the fields can be updated if necessary.
	 * When overriding this method, the supermethod must always be called.
	 */
	public void updateFields() {
		// Component name
		componentNameField.setText(component.getName());
		
		// Component color and "Use default color" checkbox
		if (colorButton != null && colorDefault != null) {
			colorButton.setIcon(new ColorIcon(getColor()));
			
			if ((component.getColor() == null) != colorDefault.isSelected())
				colorDefault.setSelected(component.getColor() == null);
		}
		
		// Mass label
		if (component.isMassive()) {
			//// Component mass:
			String text = trans.get("RocketCompCfg.lbl.Componentmass") + " ";
			text += UnitGroup.UNITS_MASS.getDefaultUnit().toStringUnit(
					component.getComponentMass());
			
			String overridetext = null;
			if (component.isMassOverridden()) {
				//// (overridden to 
				overridetext = trans.get("RocketCompCfg.lbl.overriddento") + " " + UnitGroup.UNITS_MASS.getDefaultUnit().
						toStringUnit(component.getOverrideMass()) + ")";
			}
			
			for (RocketComponent c = component.getParent(); c != null; c = c.getParent()) {
				if (c.isMassOverridden() && c.getOverrideSubcomponents()) {
					///// (overridden by
					overridetext = trans.get("RocketCompCfg.lbl.overriddenby") + " " + c.getName() + ")";
				}
			}
			
			if (overridetext != null)
				text = text + " " + overridetext;
			
			massLabel.setText(text);
		} else {
			massLabel.setText("");
		}
	}
	
	
	protected JPanel materialPanel(JPanel panel, Material.Type type) {
		////Component material: and Component finish:
		return materialPanel(panel, type, trans.get("RocketCompCfg.lbl.Componentmaterial"),
				trans.get("RocketCompCfg.lbl.Componentfinish"));
	}
	
	protected JPanel materialPanel(JPanel panel, Material.Type type,
			String materialString, String finishString) {
		JLabel label = new JLabel(materialString);
		//// The component material affects the weight of the component.
		label.setToolTipText(trans.get("RocketCompCfg.lbl.ttip.componentmaterialaffects"));
		panel.add(label, "spanx 4, wrap rel");
		
		JComboBox combo = new JComboBox(new MaterialModel(panel, component, type));
		//// The component material affects the weight of the component.
		combo.setToolTipText(trans.get("RocketCompCfg.combo.ttip.componentmaterialaffects"));
		panel.add(combo, "spanx 4, growx, wrap paragraph");
		

		if (component instanceof ExternalComponent) {
			label = new JLabel(finishString);
			////<html>The component finish affects the aerodynamic drag of the component.<br>
			String tip = trans.get("RocketCompCfg.lbl.longA1")
					//// The value indicated is the average roughness height of the surface.
					+ trans.get("RocketCompCfg.lbl.longA2");
			label.setToolTipText(tip);
			panel.add(label, "spanx 4, wmin 220lp, wrap rel");
			
			combo = new JComboBox(new EnumModel<ExternalComponent.Finish>(component, "Finish"));
			combo.setToolTipText(tip);
			panel.add(combo, "spanx 4, growx, split");
			
			//// Set for all
			JButton button = new JButton(trans.get("RocketCompCfg.but.Setforall"));
			//// Set this finish for all components of the rocket.
			button.setToolTipText(trans.get("RocketCompCfg.but.ttip.Setforall"));
			button.addActionListener(new ActionListener() {
				@Override
				public void actionPerformed(ActionEvent e) {
					Finish f = ((ExternalComponent) component).getFinish();
					try {
						document.startUndo("Set rocket finish");
						
						// Do changes
						Iterator<RocketComponent> iter = component.getRoot().iterator();
						while (iter.hasNext()) {
							RocketComponent c = iter.next();
							if (c instanceof ExternalComponent) {
								((ExternalComponent) c).setFinish(f);
							}
						}
					} finally {
						document.stopUndo();
					}
				}
			});
			panel.add(button, "wrap paragraph");
		}
		
		return panel;
	}
	
	
	private JPanel overrideTab() {
		JPanel panel = new JPanel(new MigLayout("align 50% 20%, fillx, gap rel unrel",
				"[][65lp::][30lp::][]", ""));
		//// Override the mass or center of gravity of the
		panel.add(new StyledLabel(trans.get("RocketCompCfg.lbl.Overridemassorcenter") + " " +
				component.getComponentName() + ":", Style.BOLD), "spanx, wrap 20lp");
		
		JCheckBox check;
		BooleanModel bm;
		UnitSelector us;
		BasicSlider bs;
		
		////  Mass
		bm = new BooleanModel(component, "MassOverridden");
		check = new JCheckBox(bm);
		//// Override mass:
		check.setText(trans.get("RocketCompCfg.checkbox.Overridemass"));
		panel.add(check, "growx 1, gapright 20lp");
		
		DoubleModel m = new DoubleModel(component, "OverrideMass", UnitGroup.UNITS_MASS, 0);
		
		JSpinner spin = new JSpinner(m.getSpinnerModel());
		spin.setEditor(new SpinnerEditor(spin));
		bm.addEnableComponent(spin, true);
		panel.add(spin, "growx 1");
		
		us = new UnitSelector(m);
		bm.addEnableComponent(us, true);
		panel.add(us, "growx 1");
		
		bs = new BasicSlider(m.getSliderModel(0, 0.03, 1.0));
		bm.addEnableComponent(bs);
		panel.add(bs, "growx 5, w 100lp, wrap");
		

		////  CG override
		bm = new BooleanModel(component, "CGOverridden");
		check = new JCheckBox(bm);
		//// Override center of gravity:"
		check.setText(trans.get("RocketCompCfg.checkbox.Overridecenterofgrav"));
		panel.add(check, "growx 1, gapright 20lp");
		
		m = new DoubleModel(component, "OverrideCGX", UnitGroup.UNITS_LENGTH, 0);
		// Calculate suitable length for slider
		DoubleModel length;
		if (component instanceof ComponentAssembly) {
			double l = 0;
			
			Iterator<RocketComponent> iterator = component.iterator(false);
			while (iterator.hasNext()) {
				RocketComponent c = iterator.next();
				if (c.getRelativePosition() == RocketComponent.Position.AFTER)
					l += c.getLength();
			}
			length = new DoubleModel(l);
		} else {
			length = new DoubleModel(component, "Length", UnitGroup.UNITS_LENGTH, 0);
		}
		
		spin = new JSpinner(m.getSpinnerModel());
		spin.setEditor(new SpinnerEditor(spin));
		bm.addEnableComponent(spin, true);
		panel.add(spin, "growx 1");
		
		us = new UnitSelector(m);
		bm.addEnableComponent(us, true);
		panel.add(us, "growx 1");
		
		bs = new BasicSlider(m.getSliderModel(new DoubleModel(0), length));
		bm.addEnableComponent(bs);
		panel.add(bs, "growx 5, w 100lp, wrap 35lp");
		

		// Override subcomponents checkbox
		bm = new BooleanModel(component, "OverrideSubcomponents");
		check = new JCheckBox(bm);
		//// Override mass and CG of all subcomponents
		check.setText(trans.get("RocketCompCfg.checkbox.OverridemassandCG"));
		panel.add(check, "gap para, spanx, wrap para");
		
		//// <html>The overridden mass does not include motors.<br>
		panel.add(new StyledLabel(trans.get("RocketCompCfg.lbl.longB1") +
				//// The center of gravity is measured from the front end of the
				trans.get("RocketCompCfg.lbl.longB2") + " " +
				component.getComponentName().toLowerCase() + ".", -1),
				"spanx, wrap, gap para, height 0::30lp");
		
		return panel;
	}
	
	
	private JPanel commentTab() {
		JPanel panel = new JPanel(new MigLayout("fill"));
		
		//// Comments on the
		panel.add(new StyledLabel(trans.get("RocketCompCfg.lbl.Commentsonthe") + " " + component.getComponentName() + ":",
				Style.BOLD), "wrap");
		
		// TODO: LOW:  Changes in comment from other sources not reflected in component
		commentTextArea = new JTextArea(component.getComment());
		commentTextArea.setLineWrap(true);
		commentTextArea.setWrapStyleWord(true);
		commentTextArea.setEditable(true);
		GUIUtil.setTabToFocusing(commentTextArea);
		commentTextArea.addFocusListener(textFieldListener);
		
		panel.add(new JScrollPane(commentTextArea), "width 10px, height 10px, growx, growy");
		
		return panel;
	}
	
	

	private JPanel figureTab() {
		JPanel panel = new JPanel(new MigLayout("align 20% 20%"));
		
		//// Figure style:
		panel.add(new StyledLabel(trans.get("RocketCompCfg.lbl.Figurestyle"), Style.BOLD), "wrap para");
		
		//// Component color:
		panel.add(new JLabel(trans.get("RocketCompCfg.lbl.Componentcolor")), "gapleft para, gapright 10lp");
		
		colorButton = new JButton(new ColorIcon(getColor()));
		colorButton.addActionListener(new ActionListener() {
			@Override
			public void actionPerformed(ActionEvent e) {
				Color c = component.getColor();
				if (c == null) {
					c = Prefs.getDefaultColor(component.getClass());
				}
				
				//// Choose color
				c = JColorChooser.showDialog(tabbedPane, trans.get("RocketCompCfg.lbl.Choosecolor"), c);
				if (c != null) {
					component.setColor(c);
				}
			}
		});
		panel.add(colorButton, "gapright 10lp");
		
		//// Use default color
		colorDefault = new JCheckBox(trans.get("RocketCompCfg.checkbox.Usedefaultcolor"));
		if (component.getColor() == null)
			colorDefault.setSelected(true);
		colorDefault.addActionListener(new ActionListener() {
			@Override
			public void actionPerformed(ActionEvent e) {
				if (colorDefault.isSelected())
					component.setColor(null);
				else
					component.setColor(Prefs.getDefaultColor(component.getClass()));
			}
		});
		panel.add(colorDefault, "wrap para");
		
		//// Component line style:
		panel.add(new JLabel(trans.get("RocketCompCfg.lbl.Complinestyle")), "gapleft para, gapright 10lp");
		
		LineStyle[] list = new LineStyle[LineStyle.values().length + 1];
		System.arraycopy(LineStyle.values(), 0, list, 1, LineStyle.values().length);
		
		JComboBox combo = new JComboBox(new EnumModel<LineStyle>(component, "LineStyle",
				//// Default style
				list, trans.get("LineStyle.Defaultstyle")));
		panel.add(combo, "spanx 2, growx, wrap 50lp");
		
		//// Save as default style
		JButton button = new JButton(trans.get("RocketCompCfg.but.Saveasdefstyle"));
		button.addActionListener(new ActionListener() {
			@Override
			public void actionPerformed(ActionEvent e) {
				if (component.getColor() != null) {
					Prefs.setDefaultColor(component.getClass(), component.getColor());
					component.setColor(null);
				}
				if (component.getLineStyle() != null) {
					Prefs.setDefaultLineStyle(component.getClass(), component.getLineStyle());
					component.setLineStyle(null);
				}
			}
		});
		panel.add(button, "gapleft para, spanx 3, growx, wrap");
		
		return panel;
	}
	
	
	private Color getColor() {
		Color c = component.getColor();
		if (c == null) {
			c = Prefs.getDefaultColor(component.getClass());
		}
		return c;
	}
	
	

	protected JPanel shoulderTab() {
		JPanel panel = new JPanel(new MigLayout("fill"));
		JPanel sub;
		DoubleModel m, m2;
		DoubleModel m0 = new DoubleModel(0);
		BooleanModel bm;
		JCheckBox check;
		JSpinner spin;
		

		////  Fore shoulder, not for NoseCone
		
		if (!(component instanceof NoseCone)) {
			sub = new JPanel(new MigLayout("gap rel unrel", "[][65lp::][30lp::]", ""));
			
			//// Fore shoulder
			sub.setBorder(BorderFactory.createTitledBorder(trans.get("RocketCompCfg.border.Foreshoulder")));
			

			////  Radius
			//// Diameter:
			sub.add(new JLabel(trans.get("RocketCompCfg.lbl.Diameter")));
			
			m = new DoubleModel(component, "ForeShoulderRadius", 2, UnitGroup.UNITS_LENGTH, 0);
			m2 = new DoubleModel(component, "ForeRadius", 2, UnitGroup.UNITS_LENGTH);
			
			spin = new JSpinner(m.getSpinnerModel());
			spin.setEditor(new SpinnerEditor(spin));
			sub.add(spin, "growx");
			
			sub.add(new UnitSelector(m), "growx");
			sub.add(new BasicSlider(m.getSliderModel(m0, m2)), "w 100lp, wrap");
			

			////  Length:
			sub.add(new JLabel(trans.get("RocketCompCfg.lbl.Length")));
			
			m = new DoubleModel(component, "ForeShoulderLength", UnitGroup.UNITS_LENGTH, 0);
			
			spin = new JSpinner(m.getSpinnerModel());
			spin.setEditor(new SpinnerEditor(spin));
			sub.add(spin, "growx");
			
			sub.add(new UnitSelector(m), "growx");
			sub.add(new BasicSlider(m.getSliderModel(0, 0.02, 0.2)), "w 100lp, wrap");
			

			////  Thickness:
			sub.add(new JLabel(trans.get("RocketCompCfg.lbl.Thickness")));
			
			m = new DoubleModel(component, "ForeShoulderThickness", UnitGroup.UNITS_LENGTH, 0);
			m2 = new DoubleModel(component, "ForeShoulderRadius", UnitGroup.UNITS_LENGTH);
			
			spin = new JSpinner(m.getSpinnerModel());
			spin.setEditor(new SpinnerEditor(spin));
			sub.add(spin, "growx");
			
			sub.add(new UnitSelector(m), "growx");
			sub.add(new BasicSlider(m.getSliderModel(m0, m2)), "w 100lp, wrap");
			

			////  Capped
			bm = new BooleanModel(component, "ForeShoulderCapped");
			check = new JCheckBox(bm);
			//// End capped
			check.setText(trans.get("RocketCompCfg.checkbox.Endcapped"));
			//// Whether the end of the shoulder is capped.
			check.setToolTipText(trans.get("RocketCompCfg.ttip.Endcapped"));
			sub.add(check, "spanx");
			

			panel.add(sub);
		}
		

		////  Aft shoulder
		sub = new JPanel(new MigLayout("gap rel unrel", "[][65lp::][30lp::]", ""));
		
		if (component instanceof NoseCone)
			//// Nose cone shoulder
			sub.setBorder(BorderFactory.createTitledBorder(trans.get("RocketCompCfg.title.Noseconeshoulder")));
		else
			//// Aft shoulder
			sub.setBorder(BorderFactory.createTitledBorder(trans.get("RocketCompCfg.title.Aftshoulder")));
		

		////  Radius
		//// Diameter:
		sub.add(new JLabel(trans.get("RocketCompCfg.lbl.Diameter")));
		
		m = new DoubleModel(component, "AftShoulderRadius", 2, UnitGroup.UNITS_LENGTH, 0);
		m2 = new DoubleModel(component, "AftRadius", 2, UnitGroup.UNITS_LENGTH);
		
		spin = new JSpinner(m.getSpinnerModel());
		spin.setEditor(new SpinnerEditor(spin));
		sub.add(spin, "growx");
		
		sub.add(new UnitSelector(m), "growx");
		sub.add(new BasicSlider(m.getSliderModel(m0, m2)), "w 100lp, wrap");
		

		////  Length:
		sub.add(new JLabel(trans.get("RocketCompCfg.lbl.Length")));
		
		m = new DoubleModel(component, "AftShoulderLength", UnitGroup.UNITS_LENGTH, 0);
		
		spin = new JSpinner(m.getSpinnerModel());
		spin.setEditor(new SpinnerEditor(spin));
		sub.add(spin, "growx");
		
		sub.add(new UnitSelector(m), "growx");
		sub.add(new BasicSlider(m.getSliderModel(0, 0.02, 0.2)), "w 100lp, wrap");
		

		////  Thickness:
		sub.add(new JLabel(trans.get("RocketCompCfg.lbl.Thickness")));
		
		m = new DoubleModel(component, "AftShoulderThickness", UnitGroup.UNITS_LENGTH, 0);
		m2 = new DoubleModel(component, "AftShoulderRadius", UnitGroup.UNITS_LENGTH);
		
		spin = new JSpinner(m.getSpinnerModel());
		spin.setEditor(new SpinnerEditor(spin));
		sub.add(spin, "growx");
		
		sub.add(new UnitSelector(m), "growx");
		sub.add(new BasicSlider(m.getSliderModel(m0, m2)), "w 100lp, wrap");
		

		////  Capped
		bm = new BooleanModel(component, "AftShoulderCapped");
		check = new JCheckBox(bm);
		//// End capped
		check.setText(trans.get("RocketCompCfg.checkbox.Endcapped"));
		//// Whether the end of the shoulder is capped.
		check.setToolTipText(trans.get("RocketCompCfg.ttip.Endcapped"));
		sub.add(check, "spanx");
		

		panel.add(sub);
		

		return panel;
	}
	
	


	/*
	 * Private inner class to handle events in componentNameField.
	 */
	private class TextFieldListener implements ActionListener, FocusListener {
		@Override
		public void actionPerformed(ActionEvent e) {
			setName();
		}
		
		@Override
		public void focusGained(FocusEvent e) {
		}
		
		@Override
		public void focusLost(FocusEvent e) {
			setName();
		}
		
		private void setName() {
			if (!component.getName().equals(componentNameField.getText())) {
				component.setName(componentNameField.getText());
			}
			if (!component.getComment().equals(commentTextArea.getText())) {
				component.setComment(commentTextArea.getText());
			}
		}
	}
	
	
	protected void register(Invalidatable model) {
		this.invalidatables.add(model);
	}
	
	public void invalidateModels() {
		for (Invalidatable i : invalidatables) {
			i.invalidate();
		}
	}
	
}