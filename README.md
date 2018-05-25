# OpenMETA-Rocket
*An OpenMETA model for the conceptual design of high-powered rocket for the NASA Student Launch Competition*

Check out our [blog](https://www.metamorphsoftware.com/blog/2018/5/11/nasa-student-launch-case-study) for the full report on this project.

OpenRocket and all Python scripts that interact with it are licensed under the GNU GPL. 
For license information see the file [LICENSE.TXT](https://github.com/metamorph-inc/openmeta-rocket/blob/master/LICENSE-3RD-PARTY.txt).

## Table of Contents
* [Summary](#summary)
* [NASA Student Launch](#nasa-student-launch)
* [OpenRocket](#openrocket)
* [Setup](#setup)
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
* [Future Plans](#future-plans)
* [Further Documentation](#openmeta-documentation)
* [Helpful Links](#helpful-links)


## Summary
Using the NASA Student Launch competition as a case study, OpenRocket was integrated
into the OpenMETA framework to demonstrate the strengths of a Model Based Systems
Engineering (MBSE) in complex design fields. The MBSE approach allows an engineer
to develop a small number of models, and continuously simulate different variations
until an desirable solution is found. In this case study, 972 original rocket designs
were considered. The OpenMETA project in this repo allowed us to narrow down this
large design space to a single final design after several rounds of analysis.

This example assumes some knowledge of OpenMETA and the coding language Python 2.7.
If this is your first time using OpenMETA, we recommend that you complete this [LED Tutorial](http://docs.metamorphsoftware.com/doc/tutorials/led_tutorial/led_tutorial.html)
to develop a basic understanding of the tools. For help with Python 2.7, Code Academy has
some great [tutorials](https://www.codecademy.com/learn/learn-python). Additionally, the
official reference material is available online at [Python.org](https://docs.python.org/2/).


## NASA Student Launch
NASA Student Launch (NSL) is a STEM outreach initiative hosted by Marshall Space Flight
center in Huntsville, AL. Now in its 18th year, this exciting rocketry competition provides
research-based, experiential learning for students while simultaneously producing relevant,
cost-effective research for NASA. Over a period of 8 months, middle school, high school, and
university student teams from about 23 states design and test high-powered rockets containing
an experimental payload.

For this case study, a rocket was designed as if we were entering the [2018 collegiate-level NSL
competition](https://www.nasa.gov/sites/default/files/atoms/files/nsl_un_2018.pdf).


## OpenRocket
OpenRocket is an open source Java application that allows users to design and simulate model
rockets before building them. It features an extensive catalog of components and materials,
along with the ability to create custom components and materials. Its robust simulations provide
easily extractable results including both time series data (altitude, stability, etc) and summary
scalar values (maximum velocity, apogee, etc). Many NSL teams use this exact software to simulate
their designs before launch day.

With just a few simple source code changes and a Java-Python bridge library called JPype, this
application was integrated into the OpenMETA workflow using OpenMETA Python Components. For
specific details on these source code modifications, see the OpenRocket Modifications
section in the [blog post](https://www.metamorphsoftware.com/blog/2018/5/11/nasa-student-launch-case-study). This modified source
code is available on MetaMorph's [OpenRocket fork](https://github.com/metamorph-inc/openrocket).


## Setup
### OpenMETA
1. Download the latest version of OpenMETA from https://www.metamorphsoftware.com/openmeta/.
2. Open the installer.
3. Agree to the license terms and conditions.
4. Click *Install*.


### Cloning the openmeta-rocket repository
#### Command Line
1. Open Git Bash in your desired project directory.
2. Run the following command in Git Bash: `git clone git@github.com:metamorph-inc/openmeta-rocket.git`

#### Web Browser
1. While in the main repo folder, click the green "Clone or download" button at the top right.
2. Select Download ZIP to download the repo to your Downloads folder.
3. Once the download is complete, unzip the repo to your desired project directory.


### Java
OpenRocket is Java application, so __Java x86__ (version 6 or later) must be installed
on your machine to run simulations with it.
1. Download and install the latest version of the Java SDK for Windows x86. ([Java SDK 8](http://www.oracle.com/technetwork/java/javase/downloads/jdk8-downloads-2133151.html))

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;*Note: You must accept the license agreement and make an account to download the SDK.*

2. Create a new environment variable called "JAVA_HOME" with the path to your x86
  Java JRE (For example: "C:\Program Files (x86)\Java\jre1.8.0_161") as its value.


### JPype Library
Python Components are used to run OpenRocket from within OpenMETA, so the JPype library
is used to allow the Python scripts to access the Java functions in OpenRocket. For more
information, see the [JPype documentation](http://jpype.readthedocs.io/en/latest/).

__*Note: The Java SDK must be installed before installing the JPype library.*__

1. Open a Command Prompt *(Run as Administrator)* and navigate to this repo's JPype folder.
2. Enter:
   `"C:\Program Files (x86)\META\bin\Python27\Scripts\python.exe" -m pip install jpypex-0.5.4.2-cp27-cp27m-win32.whl -t "C:\Program Files (x86)\META\bin\Python27\Lib\site-packages"`
3. To test installation, run ``"C:\Program Files (x86)\META\bin\Python27\Scripts\python.exe" jpype_test.py``

Once installation is complete, the JPype folder can be deleted from your machine.


## Getting Started with the OpenMETA Rocket Model
### Opening the openmeta-rocket project
1. Open the openmeta-rocket folder.
2. Double-click on the openmeta-rocket.xme file.
3. GME will open and display a pop-up *Import to new project* window. Select *Create
   project file* and click *Next >*.
4. The *Save As* window will open. Click *Save* to save *openmeta-rocket.mga* inside
   the openmeta-rocket folder.


### Viewing a PET model
1. Within GME, to your right, there should be a *GME Browser* window with a single
   *RootFolder* object inside. Click on the + to expand the root folder.
2. Left-click on the + next to *Testing* to expand the testing folder.
3. Left-click on the + next to *ParametricExploration* to expand the parametric
   exploration folder.
4. You should now see a number of PETs.

![PETs](/images/GMEBrowser.PNG "PET models within GME Browser window").

5. Within the GME Browser window, double-click on *OR_PET* to open it.

![OpenRocketPET](/images/OR_PET.PNG "Basic OpenRocket PET")


### Running a PET model
1. Left-click the CyPhy Master Interpreter button located on the top toolbar.

![CyPhyMasterInterpreter](/images/cyphy-master-interpreter.png "CyPhy Master Interpreter")

2. The *CyPhy Master Interpreter* window will open. On the right side of this window, there
   is a list under the heading *Please select configurations*. These are the 972 discrete
   rocket designs generated by OR_PETs's Testbench. Select any one of these configurations
   for testing.

![MasterInterpreter](/images/master-interpreter.PNG "Selecting configuration 555 in the Master Interpreter")

3. Make sure *Post to META Job Manager* is checked and left-click *OK*.
4. The *Results Browser* window will open. The running PET will be listed under the
   *Active Jobs* tab. Yellow highlighting means that the job has been queued, blue means
   the Master Interpreter is currently running the job, red means the Master Interpreter
   failed, and green means that the Master Interpreter succeeded.
5. Once the OR_PET finishes running, left-click the PET tab of the Results Browser.
6. Information from the PET run will be displayed to your right within the Results Browser window.

![ResultsBrowser](/images/results-browser.PNG "Viewing OR_PET results in the Results Browser")


### Viewing PET model results in the Visualizer
1. Left-click the *Launch in Visualizer* button in the bottom-right corner of the
   Results Browser window to view the results in the PET Visualizer.
2. The Visualizer will open in a web browser window. Left-click the *Explore>Single Plot* tab.
3. Under the *Variables* section, set the X-Axis to *WindSpeed* and the *Y-Axis* to *Apogee*. Notice
the inverse trend this plot reveals between Wind Speed and the rocket's apogee.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;*Note: Plot markers can be modified as shown here via the Markers tab.*

![SinglePlot](/images/visualizer-single-plot.PNG "Examining the relationship between Wind Speed and Apogee")


### Viewing PET images in the Visualizer
OR_PET creates plots of the rocket's simulated trajectory and its motor's thrust
curve for each run. These plots are saved in the results folder and can be viewed
in the Visualizer.
1. With OR_PET open in the Visualzer, click on the *Explore>Point Details* tab.

![PointDetails](/images/visualizer-point-details.PNG "Viewing point details and the trajectory plot")

2. This tab shows the Objective and Design Variable values for a specific PET record,
along with the images saved for that record.
3. Use the *GUID* drop-down menu to choose between PET records.
4. Use the *Images* drop-down menu to switch between the trajectory plot and the
thrust curve plot.


### PETs included in openmeta-rocket
#### OR_PET
This PET was designed to test multiple unique rocket configurations in one PET.
Its test bench includes 972 unique discrete rocket configurations to pick from,
and its Parameter Study Driver covers a range of the rocket design's continuous
variables. It exports several key simulation results and images of the rocket’s
trajectory and thrust curve for each run.

#### OR_PET_Fast
This PET is functionally equivalent to OR_PET, but does not save images of the
rocket's trajectory and thrust curve. As a result, it completes each run much faster,
making this PET ideal for testing a large design space.

#### OR_PET_2ndIter
This PET is functionally equivalent to OR_PET_Fast, but its design space is
specialized for the 2nd iteration of testing described in our [blog post](https://www.metamorphsoftware.com/blog/2018/5/11/nasa-student-launch-case-study). (Its Test Bench is constrained to only the 256 discrete configurations that passed the
first iteration of testing.)

#### Full_Mission_PET
This PET was designed to test a single rocket configuration over a range of launch
conditions. Its inputs allow you to test the effect of parameters such as wind speed,
launch altitude, and the launch rod length on your rocket design. Like OR_PET, it
exports several key simulation results and images of the rocket’s trajectory and
thrust curve for each run.

#### Full_Mission_PET_Fast
This PET is functionally equivalent to Full_Mission_PET, but does not save images of the
rocket's trajectory and thrust curve. As a result, it completes each run much faster,
making this PET ideal for testing a large design space.

### Python Component Scripts
All the Python component scripts used to build the openmeta-rocket PETs are located
in the `openmeta-rocket/scripts` folder, along with a guide for writing your own
OpenRocket scripts. To learn more about OpenMETA Python Components in general, see
OpenMETA's [Python Wrapper documentation](http://docs.metamorphsoftware.com/doc/reference_modeling/pet/pet_analysis_blocks.html#python-wrappers) as well as [OpenMDAO's documentation](http://openmdao.readthedocs.io/en/1.7.3/).


## Viewing ORK Files in OpenRocket
Once a specific rocket design is selected, it may be desirable to view it in OpenRocket.
1. [Download](http://openrocket.info/) the official OpenRocket application. (The
  OpenRocket application in this repo does not support the GUI.)
2. Open a command prompt and navigate to the directory where the OpenRocket JAR was saved.
3. Enter `java -jar OpenRocket-VERSION.jar` in the command prompt, replacing VERSION
   with the version you downloaded.
4. To open your rocket design, use the drop-down menus at the top to Select *File > Open*.
   Navigate to your .ork file and click *Open*.

![OpenRocket](/images/OpenRocket.PNG "Viewing a rocket design in OpenRocket")

For more information on the OpenRocket GUI, check out the developer's [Wiki](http://wiki.openrocket.info/User%27s_Guide).


## Future Plans
### Optimization
One large problem in the field of optimization is sampling. Currently, the design
space is built so that every component is forced to have the same material and
surface finish. This is a realistic simplification for rockets on our scale, but
would quickly lead to failure for orbital rockets. If each component were allowed
to have a different material and finish, the discrete space would allow for 8748
possible configurations. When scaled up to large rockets, the design space could
explode into millions of possible combinations. But how can we efficiently sample
millions of configurations?
We are working on a way to sample a large, discrete design space based on the level
of effect each decision has on overall system performance. The level of effect each
decision has will be stored as a metric inside of the design container. When the
configuration generator runs, it will follow a protocol to generate the most diverse
designs by first varying the components that have the largest impact. This allows
for the full range to be coarsely sampled, while keeping the total number of configurations
low. Once a satisfactory performance range is determined, the process can be repeated
iteratively allowing for more configurations within each refined range until a
desirable design is found.

### Motor Impulse Sensitivity Analysis
During the 2017-2018 competition year, we met with a student design team and discussed
some of the problems they had while designing their rocket. They found that they had
designed their rocket around a motor that had a ±20% uncertainty in the total impulse
specified by the manufacturer, which led to them not being able to accurately predict
how high their rocket would launch. We plan on countering this by designing a sensitivity
analysis comparing motor impulse (and impulse curve) with apogee, rail clearance
velocity, and other vehicle requirements.

### Software Improvements
In addition to improving the rocket model itself, changes could be implemented in
OpenRocket to improve the design process in OpenMETA. The first of these would be
upgrading to OpenRocket version 15.03. Currently, OpenRocket version 1.1.9 is being
used, since the OpenRocket developers provided support for modifying the sources
code and writing Python scripts for this version. Upgrading would involve changing
the source code of version 15.03 and potentially rewriting the OpenRocket helper
python library.
Additionally, to enable visualization of the rocket during the design process,
sketches of the rocket design could be saved along with the trajectory and thrust
curve images during PETs. Such a design sketch can be accessed currently by opening
a generated ork file in OpenRocket, but integrating this feature into the OpenMETA
toolset would streamline the design process.


## Further Documentation
For additional information regarding the OpenMETA toolset, please consult the [documentation](http://docs.metamorphsoftware.com/doc/index.html).

#### Quick links:
[Introduction](http://docs.metamorphsoftware.com/doc/getting_started/introduction/introduction.html)  
[PET Tutorial](http://docs.metamorphsoftware.com/doc/tutorials/pet_tutorial/pet_tutorial.html)  
[Results Browser](http://docs.metamorphsoftware.com/doc/reference_execution/results_browser/results_browser.html)  
[Visualizer](http://docs.metamorphsoftware.com/doc/reference_execution/visualizer/visualizer.html)


## Helpful Links
__[Contact MetaMorph!](https://www.metamorphsoftware.com/contact/)__

[MetaMorph Blog](https://www.metamorphsoftware.com/blog/)

[NASA Student Launch Competition](https://www.nasa.gov/audience/forstudents/studentlaunch/home/index.html)

[OpenRocket Simulator](http://openrocket.info/)
