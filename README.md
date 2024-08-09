# Modeling the Driving Behavior of UV Express in Mixed Traffic Scenarios
UV Express Agent-Based Model Simulation is a simulation built using SUMO (Simulation of Urban MObility) and Python. The primary purpose of this system is to simulate the driving behavior of UV Express in mixed traffic scenarios. The program integrates real-world driving data with traffic simulation software, SUMO, to create a detailed model of UV Express operations. This approach enables a comprehensive understanding of driving patterns and interactions in urban environments.

## Proponents
* ANG, Audric 
    * ***Email Address:*** [audric_ang@dlsu.edu.ph](mailto:audric_ang@dlsu.edu.ph)
    * ***GitHub:*** [oodorikku](https://github.com/oodorikku)
* MARTINEZ, Kyle
    * ***Email Address:*** [kyle_martinez@dlsu.edu.ph](mailto:kyle_martinez@dlsu.edu.ph)
    * ***GitHub:*** [MartinezKyle](https://github.com/MartinezKyle)
* PIANO, Gabriel Edward
    * ***Email Address:*** [gabriel_edward_piano@dlsu.edu.ph](mailto:gabriel_edward_piano@dlsu.edu.ph)
    * ***GitHub:*** [Poije](https://github.com/Poije)
* UY, Shane Owen
    * ***Email Address:*** [shane_owen_uy@dlsu.edu.ph](mailto:shane_owen_uy@dlsu.edu.ph)
    * ***GitHub:*** [Shaneuy](https://github.com/Shaneuy)

## Adviser
* Dr. Briane Paul V. Samson, PhD. 
    * ***Email Address:*** [briane.samson@dlsu.edu.ph](mailto:briane.samson@dlsu.edu.ph)

## Repository Structure
* `EDA and HMM/`<br>
  \- *Folder containing the notebook and the annotated data used to do exploratory data analysis and training a sample HMM model*
    * `HMM EDA.ipynb`<br>
      \- *Notebook used to do exploratory data analysis and training a sample HMM model*
    * `data.csv`<br>
      \- *CSV File containing the annotated data from videos collected from all the trips. Used to train the HMM Model* 
    * `peak.csv`<br>
      \- *CSV File containing the annotated data from videos collected from all the trips during peak hours. Used for exploratory data analysis* 
    * `non_peak.csv`<br>
      \- *CSV File containing the annotated data from videos collected from all the trips during non-peak hours. Used for exploratory data analysis*
* `SUMO/` <br>
  \- *Folder containing the necessary files to run the simulation in SUMO*
    * `HMMTraCI.py`<br>
      \- *Python script used to run and control the simulation using TraCI, sumolib, and hmmlearn*
    * `HMM.py`<br>
      \- *Python module containing the class that is used to create and train an HMM model*
    * `Vehicle.py`<br>
      \- *Python module containing the class that represents and is responsible for managing individual UV express vehicle instances and SUMO agents*
    * `PedestrianEdges.py`<br>
      \- *Python module containing the class that represents pedestrian edges, and their associated bus stops within the transportation network*
    * `TraCIHelper.py`<br>
      \- *Python module that contains functions that handles initialization of different agent in the simulation, such as random vehicles and people into the simulation*  
    * `UVTraCIHelper.py`<br>
      \- *Python module that contains functions that handle initialization and behavior handling of the UV Express vehicles within the SUMO environment*      
    * `data.csv`<br>
      \- *CSV File containing the annotated data from videos collected from all the trips. Used to train the HMM Model*
    * `NoPolyGons-Full-route.net.xml`<br>
      \- *XML file containing the *
    * `Passenger_Routes.rou.xml`<br>
      \- *XML file containing the possible routes of the UV Express passengers, containing their pickup and dropoff points*
    * `Southbound_Validation_Routes.rou.xml`<br>
      \- *XML file containing the possible routes of different non-UV EXpress vehicle agents during Soutbound validation*
    * `BusStops.add.xml`<br>
      \- *XML file containing the bus stops to be added in the simulation*
    * `UVExpressSimulation.sumocfg`<br>
      \- *SUMO configuration file*
    * `UVRoutes.rou.xml`<br>
      \- *XML file containing the possible routes of all the vehicle agents in the simulation*
    * `Northbound_Validation_Routes.rou.xml`<br>
      \- *XML file containing the possible routes of different non-UV EXpress vehicle agents during Northbound validation*
    * `Passenger_Validation_Routes.rou.xml`<br>
      \- *XML file containing the possible routes of the UV Express passengers during validation, containing their pickup and dropoff points*
* `requirements.txt`
  \- TXT file that contains the list of Python libraries required by the program used to install the said libraries.

## Prerequisites
1. [Python](<https://www.python.org/downloads/release/python-3122/>)
2. [SUMO](<https://eclipse.dev/sumo/>)

## How To Run
### Install requirements
If this the first time running the project,
1. Open a command line interface on the main projet directory and type the following command: <br>
`pip install -r requirements.txt`

### Running the simulation
1. Open a command line interface on the `SUMO/` folder and type<br>
`python HMMTraci.py`
2. After running the Python TraCI script, a SUMO GUI window will open. To run the simulation, press the Run Button as seen below:
![Running The Simulation](/README_Images/Run_Simulation.png)

### Adjusting Simulation Elements
#### Adjusting View Type
1. Click on the currently selected view type (default value is `standard`) as seen below:
![Opening The View Menu](/README_Images/View_Dropdown.png)
2. Select the preferred view type (the one used on the study is `real world`) as seen below:
![View Menu](/README_Images/View_Dropdown_Menu.png)

#### Adjusting Simulation Speed
To adjust the simulation speed, you can use the following options below
* Manually place an integer value on the text box beside the `Delay (ms)` label (default value is `20`) as seen below:
![Delay Text Box](/README_Images/Delay_Textbox.png)
* Use the up and down step arrows to increase and decrease the delay, respectively, as seen below:
![Delay Step Arrow](/README_Images/Delay_StepArrows.png)
* Use the slider by sliding the pointer to the right to increase delay or slide the pointer to the left to decrease the delay as seen below:
![Delay Slider](/README_Images/Delay_Slider.png)

#### Stopping the Simulation
To stop the simulation, click the Stop Button as seen below:
![Stop Simulation](/README_Images/Stop_Simulation.png)