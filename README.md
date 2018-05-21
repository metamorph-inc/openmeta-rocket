# TODO
* Embed link to PET Tutorial in OpenMETA section note
* Clean up rocket project & rename openmeta-rocket
* Remove old versions of project
* Snip image of OR_PET for Viewing a PET model
* Figure out simple PET demo for View/Run/Visualizer PET
* Ask about the cloning thing

# OpenMETA-Rocket
_An OpenMETA model for the conceptual design of high-powered rocket for the NASA Student Launch Competition_

**Table of Contents**
* [Summary](#summary)
* [NASA Student Launch](#nasa-student-launch)
* [OpenRocket](#openrocket)
* [Requirements](#requirements)
  * [OpenMETA](#openmeta)
  * [Java](#java)
  * [JPype Library](#jpype-library)
* [Getting Started with the OpenMETA Rocket Model](#getting-started-with-the-openmeta-rocket-model)
  * [Cloning the openmeta-rocket repository](#cloning-the-openmeta-rocket-repository)
  * [Opening the openmeta-rocket project](#opening-the-openmeta-rocket-project)
  * [Viewing a PET model](#viewing-a-pet-model)
  * [Running a PET model](#running-a-pet-model)
  * [Viewing PET model results in the Visualizer](#viewing-pet-model-results-in-the-visualizer)
  * [PETs included in openmeta-rocket](#pets-included-in-openmeta-rocket)
  * [Python Component scripts](#python-component-scripts)
* [Viewing ORK Files in OpenRocket](#viewing-ork-files-in-openrocket)
* [Further Documentation](#openmeta-documentation)
* [Future Plans](#future-plans-and-improvements-to-vahana-configuration-trade-study)

## Summary
Using the NASA Student Launch competition as a case study, OpenRocket was integrated
into the OpenMETA framework to demonstrate the strengths of a Model Based Systems
Engineering (MBSE) in complex design fields. The MBSE approach allows an engineer
to develop a small number of models, and continuously simulate different variations
until an desirable solution is found. In this case study, 972 original rocket designs
were considered. The OpenMETA project in this repo allowed us to narrow down this
large design space to a single final design after several rounds of analysis.

## NASA Student Launch

## OpenRocket

## Requirements
### OpenMETA
1. Download the latest version of OpenMETA from https://www.metamorphsoftware.com/openmeta/.
1. Open the installer.
1. Agree to the license terms and conditions.
1. Left-click 'Install'.

*Note: If this is your first time using OpenMETA, we recommend that you complete
the PET Tutorial to develop a basic understanding of the tools!*

### Java

### JPype Python Library
1. Create a new environment variable called "JAVA_HOME" with the path (For example:
   "C:\Program Files (x86)\Java\jre1.8.0_161") to your x86 Java JRE as its value.
1. Download the Jpype wheel (jpypex-0.5.4.2-cp27-cp27m-win32.whl) and test file
   (jpype_test.py) from this repo.
1. Open a command prompt and navigate to the folder where the Jpype wheel is stored.
1. Enter: `"C:\Program Files (x86)\META\bin\Python27\Scripts\python.exe" -m pip install jpypex-0.5.4.2-cp27-cp27m-win32.whl -t "C:\Program Files (x86)\META\bin\Python27\Lib\site-packages"`

   If this doesn't work, open Windows Powershell (admin), navigate to where the
   jpype wheel is stored, and run this version of the previous command:
   `C:\"Program Files (x86)"\META\bin\Python27\Scripts\python.exe C:\"Program Files (x86)"\META\bin\Python27\Scripts\pip.exe install jpypex-0.5.4.2-cp27-cp27m-win32.whl -t C:\"Program Files (x86)"\META\bin\Python27\Lib\site-packages`

1. To test installation, run ``"C:\Program Files (x86)\META\bin\Python27\Scripts\python.exe" jpype_test.py``

_Once installation is complete, the JPype folder can be deleted from your machine._

## Getting Started with the OpenMETA Rocket Model
### Cloning the openmeta-rocket repository
#### Command Line
1. Copy the following key onto your clipboard: `git@github.com:metamorph-inc/openmeta-rocket.git`
1. Open Git Bash in your desired project directory.
1. Run the following command in Git Bash: `git clone git@github.com:metamorph-inc/openmeta-rocket.git`

#### Web Browser

### Opening the openmeta-rocket project
1. Open the openmeta-rocket folder.
1. Double-click on the openmeta-rocket.xme file.
1. GME will open and display a pop-up 'Import to new project' window. Select 'Create
   project file' and click 'Next >'.
1. The 'Save As' window will open. Click 'Save' to save 'openmeta-rocket.mga' inside
   the openmeta-rocket folder.

### Viewing a PET model
1. Within GME, to your right, there should be a 'GME Browser' window with a single
   'RootFolder' object inside. Click on the '+' to expand the root folder.
1. Left-click on the '+' next to 'Testing' to expand the testing folder.
1. Left-click on the '+' next to 'ParametricExploration' to expand the parametric
   exploration folder.
1. You should now see a number of PETs  
![PETs](images/viewing-the-pet-models-1.png "PET models within GME Browser window").  
1. Within the GME Browser window, double-click on 'OR_PET' to open it.   
![DEMOVahanaTiltWingPET](images/viewing-the-pet-models-2.png "Vahana Tilt Wing PET")

### Running a PET model
1. Left-click the CyPhy Master Interpreter button located on the top toolbar.   
![CyPhyMasterInterpreter](images/running-a-pet-model-1.png "CyPhy Master Interpreter")  
1. The 'CyPhy Master Interpreter' window will open. Make sure 'Post to META Job Manager'
   is checked and left-click 'OK'.
1. The 'Results Browser' window will open. The running PET will be listed under the
   'Active Jobs' tab. Blue means the Master Interpreter is still running, red means
   the Master Interpreter failed, and green means that the Master Interpreter succeeded.
1. Once the OR_PET finishes running, left-click the PET tab of the Results Browser.
1. Information from the PET run will be displayed to your right within the Results Browser window.

### Viewing PET model results in the Visualizer
1. Left-click the 'Launch in Visualizer' button in the bottom-right corner (of the
   Results Browser window) to view the results in the PET Visualizer.
1. The Visualizer will open in a browser window. Left-click the 'Explore>Single Plot' tab.
1. Under the 'Variables' section, set the X-Axis to 'Range' and the 'Y-Axis' to 'DOCPerKm'.

### PETs included in openmeta-rocket

### Python Component Scripts
All the Python component scripts used to build the openmeta-rocket PETs are located
in the `openmeta-rocket/scripts` folder, along with a guide for writing your own
OpenRocket scripts. To learn more about OpenMETA Python Components in general, see
OpenMETA's [Python Wrapper documentation](http://docs.metamorphsoftware.com/doc/reference_modeling/pet/pet_analysis_blocks.html#python-wrappers) as well as [OpenMDAO's documentation](http://openmdao.readthedocs.io/en/1.7.3/).

## Viewing ORK Files in OpenRocket
Once a specific rocket design is selected, it may be desirable to view it in OpenRocket
itself.
- how to open it `java -jar OpenRocket-version.jar`
- short description of GUI

## Further Documentation
For additional information regarding the OpenMETA toolset, please consult the [documentation](http://docs.metamorphsoftware.com/doc/index.html).

*Quick links:*  
[Introduction](http://docs.metamorphsoftware.com/doc/getting_started/introduction/introduction.html)  
[PET Tutorial](http://docs.metamorphsoftware.com/doc/tutorials/pet_tutorial/pet_tutorial.html)  
[Results Browser](http://docs.metamorphsoftware.com/doc/reference_execution/results_browser/results_browser.html)  
[Visualizer](http://docs.metamorphsoftware.com/doc/reference_execution/visualizer/visualizer.html)

## Future Plans
