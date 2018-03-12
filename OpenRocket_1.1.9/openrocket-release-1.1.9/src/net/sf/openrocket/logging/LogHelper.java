package net.sf.openrocket.logging;

import net.sf.openrocket.util.BugException;


/**
 * Base class for all loggers used in OpenRocket.
 * <p>
 * This class contains methods for logging at various log levels, and methods
 * which take the logging level as a parameter.  All methods may take three types
 * of parameters:
 * <ul>
 * 	<li><code>levels</code>		number of additional levels of the stack trace to print
 * 								on the log line.  This is useful to determine from where
 * 								the current method has been called.  Zero if not provided.
 *  <li><code>message</code>	the String message (may be null).
 *  <li><code>cause</code>		the exception that caused this log (may be null).
 * </ul>
 * <p>
 * The logging methods are guaranteed never to throw an exception, and can thus be safely
 * used in finally blocks.
 * 
 * @author Sampo Niskanen <sampo.niskanen@iki.fi>
 */
public abstract class LogHelper {
	/**
	 * Level from which upward a TraceException is added to the log lines.
	 */
	private static final LogLevel TRACING_LOG_LEVEL =
			LogLevel.fromString(System.getProperty("openrocket.log.tracelevel"), LogLevel.INFO);
	
	private static final DelegatorLogger delegator = new DelegatorLogger();
	
	

	/**
	 * Get the logger to be used in logging.
	 * 
	 * @return	the logger to be used in all logging.
	 */
	public static LogHelper getInstance() {
		return delegator;
	}
	
	

	/**
	 * Log a LogLine object.  This method needs to be able to cope with multiple threads
	 * accessing it concurrently (for example by being synchronized).
	 * 
	 * @param line	the LogLine to log.
	 */
	public abstract void log(LogLine line);
	
	
	/**
	 * Log using VBOSE level.
	 * 
	 * @param message	the logged message (may be null).
	 */
	public void verbose(String message) {
		try {
			log(createLogLine(0, LogLevel.VBOSE, message, null));
		} catch (Exception e) {
			e.printStackTrace();
		}
	}
	
	/**
	 * Log using VBOSE level.
	 * 
	 * @param message	the logged message (may be null).
	 * @param cause		the causing exception (may be null).
	 */
	public void verbose(String message, Throwable cause) {
		try {
			log(createLogLine(0, LogLevel.VBOSE, message, cause));
		} catch (Exception e) {
			e.printStackTrace();
		}
	}
	
	/**
	 * Log using VBOSE level.
	 * 
	 * @param levels	number of additional levels of stack trace to include.
	 * @param message	the logged message (may be null).
	 */
	public void verbose(int levels, String message) {
		try {
			log(createLogLine(levels, LogLevel.VBOSE, message, null));
		} catch (Exception e) {
			e.printStackTrace();
		}
	}
	
	/**
	 * Log using VBOSE level.
	 * 
	 * @param levels	number of additional levels of stack trace to include.
	 * @param message	the logged message (may be null).
	 * @param cause		the causing exception (may be null).
	 */
	public void verbose(int levels, String message, Throwable cause) {
		try {
			log(createLogLine(levels, LogLevel.VBOSE, message, cause));
		} catch (Exception e) {
			e.printStackTrace();
		}
	}
	
	
	/**
	 * Log using DEBUG level.
	 * 
	 * @param message	the logged message (may be null).
	 */
	public void debug(String message) {
		try {
			log(createLogLine(0, LogLevel.DEBUG, message, null));
		} catch (Exception e) {
			e.printStackTrace();
		}
	}
	
	/**
	 * Log using DEBUG level.
	 * 
	 * @param message	the logged message (may be null).
	 * @param cause		the causing exception (may be null).
	 */
	public void debug(String message, Throwable cause) {
		try {
			log(createLogLine(0, LogLevel.DEBUG, message, cause));
		} catch (Exception e) {
			e.printStackTrace();
		}
	}
	
	/**
	 * Log using DEBUG level.
	 * 
	 * @param levels	number of additional levels of stack trace to include.
	 * @param message	the logged message (may be null).
	 */
	public void debug(int levels, String message) {
		try {
			log(createLogLine(levels, LogLevel.DEBUG, message, null));
		} catch (Exception e) {
			e.printStackTrace();
		}
	}
	
	/**
	 * Log using DEBUG level.
	 * 
	 * @param levels	number of additional levels of stack trace to include.
	 * @param message	the logged message (may be null).
	 * @param cause		the causing exception (may be null).
	 */
	public void debug(int levels, String message, Throwable cause) {
		try {
			log(createLogLine(levels, LogLevel.DEBUG, message, cause));
		} catch (Exception e) {
			e.printStackTrace();
		}
	}
	
	
	/**
	 * Log using INFO level.
	 * 
	 * @param message	the logged message (may be null).
	 */
	public void info(String message) {
		try {
			log(createLogLine(0, LogLevel.INFO, message, null));
		} catch (Exception e) {
			e.printStackTrace();
		}
	}
	
	/**
	 * Log using INFO level.
	 * 
	 * @param message	the logged message (may be null).
	 * @param cause		the causing exception (may be null).
	 */
	public void info(String message, Throwable cause) {
		try {
			log(createLogLine(0, LogLevel.INFO, message, cause));
		} catch (Exception e) {
			e.printStackTrace();
		}
	}
	
	/**
	 * Log using INFO level.
	 * 
	 * @param levels	number of additional levels of stack trace to include.
	 * @param message	the logged message (may be null).
	 */
	public void info(int levels, String message) {
		try {
			log(createLogLine(levels, LogLevel.INFO, message, null));
		} catch (Exception e) {
			e.printStackTrace();
		}
	}
	
	/**
	 * Log using INFO level.
	 * 
	 * @param levels	number of additional levels of stack trace to include.
	 * @param message	the logged message (may be null).
	 * @param cause		the causing exception (may be null).
	 */
	public void info(int levels, String message, Throwable cause) {
		try {
			log(createLogLine(levels, LogLevel.INFO, message, cause));
		} catch (Exception e) {
			e.printStackTrace();
		}
	}
	
	
	/**
	 * Log using USER level.
	 * 
	 * @param message	the logged message (may be null).
	 */
	public void user(String message) {
		try {
			log(createLogLine(0, LogLevel.USER, message, null));
		} catch (Exception e) {
			e.printStackTrace();
		}
	}
	
	/**
	 * Log using USER level.
	 * 
	 * @param message	the logged message (may be null).
	 * @param cause		the causing exception (may be null).
	 */
	public void user(String message, Throwable cause) {
		try {
			log(createLogLine(0, LogLevel.USER, message, cause));
		} catch (Exception e) {
			e.printStackTrace();
		}
	}
	
	/**
	 * Log using USER level.
	 * 
	 * @param levels	number of additional levels of stack trace to include.
	 * @param message	the logged message (may be null).
	 */
	public void user(int levels, String message) {
		try {
			log(createLogLine(levels, LogLevel.USER, message, null));
		} catch (Exception e) {
			e.printStackTrace();
		}
	}
	
	/**
	 * Log using USER level.
	 * 
	 * @param levels	number of additional levels of stack trace to include.
	 * @param message	the logged message (may be null).
	 * @param cause		the causing exception (may be null).
	 */
	public void user(int levels, String message, Throwable cause) {
		try {
			log(createLogLine(levels, LogLevel.USER, message, cause));
		} catch (Exception e) {
			e.printStackTrace();
		}
	}
	
	
	/**
	 * Log using WARN level.
	 * 
	 * @param message	the logged message (may be null).
	 */
	public void warn(String message) {
		try {
			log(createLogLine(0, LogLevel.WARN, message, null));
		} catch (Exception e) {
			e.printStackTrace();
		}
	}
	
	/**
	 * Log using WARN level.
	 * 
	 * @param message	the logged message (may be null).
	 * @param cause		the causing exception (may be null).
	 */
	public void warn(String message, Throwable cause) {
		try {
			log(createLogLine(0, LogLevel.WARN, message, cause));
		} catch (Exception e) {
			e.printStackTrace();
		}
	}
	
	/**
	 * Log using WARN level.
	 * 
	 * @param levels	number of additional levels of stack trace to include.
	 * @param message	the logged message (may be null).
	 */
	public void warn(int levels, String message) {
		try {
			log(createLogLine(levels, LogLevel.WARN, message, null));
		} catch (Exception e) {
			e.printStackTrace();
		}
	}
	
	/**
	 * Log using WARN level.
	 * 
	 * @param levels	number of additional levels of stack trace to include.
	 * @param message	the logged message (may be null).
	 * @param cause		the causing exception (may be null).
	 */
	public void warn(int levels, String message, Throwable cause) {
		try {
			log(createLogLine(levels, LogLevel.WARN, message, cause));
		} catch (Exception e) {
			e.printStackTrace();
		}
	}
	
	
	/**
	 * Log using ERROR level.
	 * 
	 * @param message	the logged message (may be null).
	 */
	public void error(String message) {
		try {
			log(createLogLine(0, LogLevel.ERROR, message, null));
		} catch (Exception e) {
			e.printStackTrace();
		}
	}
	
	/**
	 * Log using ERROR level.
	 * 
	 * @param message	the logged message (may be null).
	 * @param cause		the causing exception (may be null).
	 */
	public void error(String message, Throwable cause) {
		try {
			log(createLogLine(0, LogLevel.ERROR, message, cause));
		} catch (Exception e) {
			e.printStackTrace();
		}
	}
	
	/**
	 * Log using ERROR level.
	 * 
	 * @param levels	number of additional levels of stack trace to include.
	 * @param message	the logged message (may be null).
	 */
	public void error(int levels, String message) {
		try {
			log(createLogLine(levels, LogLevel.ERROR, message, null));
		} catch (Exception e) {
			e.printStackTrace();
		}
	}
	
	/**
	 * Log using ERROR level.
	 * 
	 * @param levels	number of additional levels of stack trace to include.
	 * @param message	the logged message (may be null).
	 * @param cause		the causing exception (may be null).
	 */
	public void error(int levels, String message, Throwable cause) {
		try {
			log(createLogLine(levels, LogLevel.ERROR, message, cause));
		} catch (Exception e) {
			e.printStackTrace();
		}
	}
	
	

	/**
	 * Log using the provided log level.
	 * 
	 * @param level		the logging level.
	 * @param message	the logged message (may be null).
	 */
	public void log(LogLevel level, String message) {
		try {
			log(createLogLine(0, level, message, null));
		} catch (Exception e) {
			e.printStackTrace();
		}
	}
	
	/**
	 * Log using the provided log level.
	 * 
	 * @param level		the logging level.
	 * @param message	the logged message (may be null).
	 * @param cause		the causing exception (may be null).
	 */
	public void log(LogLevel level, String message, Throwable cause) {
		try {
			log(createLogLine(0, level, message, cause));
		} catch (Exception e) {
			e.printStackTrace();
		}
	}
	
	/**
	 * Log using the provided log level.
	 * 
	 * @param levels	number of additional levels of stack trace to include.
	 * @param level		the logging level.
	 * @param message	the logged message (may be null).
	 */
	public void log(int levels, LogLevel level, String message) {
		try {
			log(createLogLine(levels, level, message, null));
		} catch (Exception e) {
			e.printStackTrace();
		}
	}
	
	/**
	 * Log using the provided log level.
	 * 
	 * @param levels	number of additional levels of stack trace to include.
	 * @param level		the logging level.
	 * @param message	the logged message (may be null).
	 * @param cause		the causing exception (may be null).
	 */
	public void log(int levels, LogLevel level, String message, Throwable cause) {
		try {
			log(createLogLine(levels, level, message, cause));
		} catch (Exception e) {
			e.printStackTrace();
		}
	}
	
	

	/**
	 * Instantiates, logs and throws a BugException.  The message is logged at
	 * ERROR level.
	 * <p>
	 * This method never returns normally.
	 * 
	 * @param message	the message for the log and exception.
	 * @throws BugException	always.
	 */
	public void throwBugException(String message) throws BugException {
		BugException e = new BugException(message);
		log(createLogLine(0, LogLevel.ERROR, message, e));
		throw e;
	}
	
	/**
	 * Instantiates, logs and throws a BugException.  The message is logged at
	 * ERROR level with the specified cause.
	 * <p>
	 * This method never returns normally.
	 * 
	 * @param message	the message for the log and exception.
	 * @param cause		the causing exception (may be null).
	 * @throws BugException	always.
	 */
	public void throwBugException(String message, Throwable cause) throws BugException {
		BugException e = new BugException(message, cause);
		log(createLogLine(0, LogLevel.ERROR, message, cause));
		throw e;
	}
	
	


	/**
	 * Create a LogLine object from the provided information.  This method must be
	 * called directly from the called method in order for the trace position
	 * to be correct!
	 * 
	 * @param additionalLevels	how many additional stack trace levels to include on the line. 
	 * @param level				the log level.
	 * @param message			the log message (null ok).
	 * @param cause				the log exception (null ok).
	 * 
	 * @return					a LogLine populated with all necessary fields.
	 */
	private LogLine createLogLine(int additionalLevels, LogLevel level, String message,
			Throwable cause) {
		TraceException trace;
		if (level.atLeast(TRACING_LOG_LEVEL)) {
			trace = new TraceException(2, 2 + additionalLevels);
		} else {
			trace = null;
		}
		return new LogLine(level, trace, message, cause);
	}
}
