import sys
from jpype import *
print "Testing JPype Installation...\n"

try:
    startJVM(getDefaultJVMPath())
    java.lang.System.out.println("Jpype 0.5.4.2 has been installed successfully!\n")
    shutdownJVM()
except NameError:
    print "JPype undefined: library did not install correctly."
except TypeError:
    print "JVM failed: please make sure that an x86 version of Java is installed and JAVA_HOME is defined correctly."
except:
    print "Unexpected error: ", sys.exc_info()[0]
