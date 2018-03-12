package net.sf.openrocket.l10n;

import java.util.Locale;
import java.util.MissingResourceException;

import net.sf.openrocket.gui.main.ExceptionHandler;

/**
 * A translator that suppresses MissingResourceExceptions and handles them gracefully.
 * For the first missing key this class calls the exception handler, and afterwards
 * always returns the key for missing translations.
 * 
 * @author Sampo Niskanen <sampo.niskanen@iki.fi>
 */
public class ExceptionSuppressingTranslator implements Translator {
	
	static boolean errorReported = false;
	
	private final Translator translator;
	
	
	/**
	 * Sole constructor.
	 * 
	 * @param translator	the translator to use
	 */
	public ExceptionSuppressingTranslator(Translator translator) {
		this.translator = translator;
	}
	
	

	@Override
	public String get(String key) {
		try {
			return translator.get(key);
		} catch (MissingResourceException e) {
			handleError(key, e);
		}
		
		return key;
	}
	
	

	private static synchronized void handleError(String key, MissingResourceException e) {
		if (!errorReported) {
			errorReported = true;
			ExceptionHandler.handleErrorCondition("Can not find translation for '" + key + "' locale=" + Locale.getDefault(), e);
		}
	}
	
}
