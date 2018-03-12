package net.sf.openrocket.rocketcomponent;

import net.sf.openrocket.l10n.Translator;
import net.sf.openrocket.startup.Application;
import net.sf.openrocket.util.MathUtil;

/**
 * This class represents a generic component that has a specific mass and an approximate shape.
 * The mass is accessed via get/setComponentMass.
 * 
 * @author Sampo Niskanen <sampo.niskanen@iki.fi>
 */
public class MassComponent extends MassObject {
	private static final Translator trans = Application.getTranslator();
	
	private double mass = 0;
	
	
	public MassComponent() {
		super();
	}
	
	public MassComponent(double length, double radius, double mass) {
		super(length, radius);
		this.mass = mass;
	}
	
	
	@Override
	public double getComponentMass() {
		return mass;
	}
	
	public void setComponentMass(double mass) {
		mass = Math.max(mass, 0);
		if (MathUtil.equals(this.mass, mass))
			return;
		this.mass = mass;
		fireComponentChangeEvent(ComponentChangeEvent.MASS_CHANGE);
	}
	
	
	@Override
	public String getComponentName() {
		//// Mass component
		return trans.get("MassComponent.MassComponent");
	}
	
	@Override
	public boolean allowsChildren() {
		return false;
	}
	
	@Override
	public boolean isCompatible(Class<? extends RocketComponent> type) {
		// Allow no components to be attached to a MassComponent
		return false;
	}
}
