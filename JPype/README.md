Installing JPype in OpenMETA
----------------------------
Requirements: OpenMETA, Java JDK/JRE x86

1. Create a new environment variable called "JAVA_HOME" with the path to your x86 Java JRE as its value.
   For example: "C:\Program Files (x86)\Java\jre1.8.0_161"

2. Download the Jpype wheel (jpypex-0.5.4.2-cp27-cp27m-win32.whl) and test file (jpype_test.py) from this repo.

3. Open a command prompt and navigate to the folder where the Jpype wheel is stored.

4. Enter: `"C:\Program Files (x86)\META\bin\Python27\Scripts\python.exe" -m pip install jpypex-0.5.4.2-cp27-cp27m-win32.whl -t "C:\Program Files (x86)\META\bin\Python27\Lib\site-packages"`

   If this doesn't work, open Windows Powershell (admin), navigate to where the jpype wheel is stored, and run this version of the previous command:
   `C:\"Program Files (x86)"\META\bin\Python27\Scripts\python.exe C:\"Program Files (x86)"\META\bin\Python27\Scripts\pip.exe install jpypex-0.5.4.2-cp27-cp27m-win32.whl -t C:\"Program Files (x86)"\META\bin\Python27\Lib\site-packages`

5. To test installation, run ``"C:\Program Files (x86)\META\bin\Python27\Scripts\python.exe" jpype_test.py`


Python Wheel Building Guide
---------------------------
https://cowboyprogrammer.org/2014/06/building-python-wheels-for-windows/
