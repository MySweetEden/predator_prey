# Predator-Prey
## Overview
This project is a Python-based multi-agent simulation of predator-prey dynamics, utilizing the Mesa library for the agent-based modeling framework and Plotly for visualizing the agents' processes throughout the simulation. The focus is on exploring the interactions between predators and prey within a simulated environment, examining patterns such as population dynamics, behavior changes, and the impact of various environmental factors.  
<video src="./predator_prey.mp4" width="500" height="500" controls></video>

## Features
Agent-Based Modeling: Leverages the Mesa library to create complex predator-prey interactions within a simulated ecosystem.  
Dynamic Visualization: Utilizes Plotly to provide insightful visualizations of the simulation process, allowing for real-time observation of agent behaviors and population changes.  

## Getting Started
### Prerequisites
Python 3.x  
Rye (or other package management tool)

### Installation
```
# 1. Clone the repository:
git clone https://github.com/MySweetEden/predator_prey
# 2. Navigate to the project directory:
cd predator_prey
# 3. Install dependencies using Rye:
rye sync
```
If Rye is not part of your workflow, you can alternatively install the necessary packages using the requirements.lock file or the pyproject.toml file.

### Running the Simulation
```
# To run the simulation, execute the following jupyter notebook.
./src/predator_prey/main.ipynb
```

## Usage
The simulation can be customized through various parameters defined in main.ipynb. Adjust these parameters to explore different predator-prey dynamics and ecological conditions.

## License
This project is licensed under the MIT License.

## Acknowledgments
- [Introduction to Agent-Based Modeling (PDF)](https://pdfs.semanticscholar.org/28a1/6e1b01b5897bde0e6fc676eacbc73d179ad6.pdf)
- [Agent-Based Models with Python: An Introduction to Mesa](https://www.complexityexplorer.org/courses/172-agent-based-models-with-python-an-introduction-to-mesa)
- [Creating a Simple Predator-Prey Model with Mesa: A Python Simulation Library](https://medium.com/@ulriktpedersen/creating-a-simple-predator-prey-model-with-mesa-a-python-simulation-library-4835f29791ae)
