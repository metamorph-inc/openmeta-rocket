package net.sf.openrocket.file;

import java.io.BufferedInputStream;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.InputStream;

import net.sf.openrocket.aerodynamics.WarningSet;
import net.sf.openrocket.document.OpenRocketDocument;
import net.sf.openrocket.logging.LogHelper;
import net.sf.openrocket.startup.Application;


public abstract class RocketLoader {
	protected final WarningSet warnings = new WarningSet();
	private static final LogHelper log = Application.getLogger();
	
	
	/**
	 * Loads a rocket from the specified File object.
	 */
	public final OpenRocketDocument load(File source) throws RocketLoadException {
		log.info("Hello out there!");
		warnings.clear();
		InputStream stream = null;
		
		try {
			log.info("Trying to get file.");
			stream = new BufferedInputStream(new FileInputStream(source));
			log.info("Stream created. Return!");
			return load(stream);
			
		} catch (FileNotFoundException e) {
			throw new RocketLoadException("File not found: " + source);
		} finally {
			if (stream != null) {
				try {
					stream.close();
				} catch (IOException e) {
					e.printStackTrace();
				}
			}
		}
	}
	
	/**
	 * Loads a rocket from the specified InputStream.
	 */
	public final OpenRocketDocument load(InputStream source) throws RocketLoadException {
		warnings.clear();
		
		try {
			return loadFromStream(source);
		} catch (RocketLoadException e) {
			throw e;
		} catch (IOException e) {
			throw new RocketLoadException("I/O error: " + e.getMessage(), e);
		}
	}
	
	

	/**
	 * This method is called by the default implementations of {@link #load(File)} 
	 * and {@link #load(InputStream)} to load the rocket.
	 * 
	 * @throws RocketLoadException	if an error occurs during loading.
	 */
	protected abstract OpenRocketDocument loadFromStream(InputStream source) throws IOException,
			RocketLoadException;
	
	

	public final WarningSet getWarnings() {
		return warnings;
	}
}
