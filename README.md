# Predator-Prey
## Overview
This project is a Python-based multi-agent simulation of predator-prey dynamics, utilizing the Mesa library for the agent-based modeling framework and Plotly for visualizing the agents' processes throughout the simulation. The focus is on exploring the interactions between predators and prey within a simulated environment, examining patterns such as population dynamics, behavior changes, and the impact of various environmental factors.  

**Experience it firsthand through interactive GUI.** Adjust parameters in real-time and witness the complex ecosystem adapt and evolve:

[Predator-Prey Simulation](https://predatorprey-g8tdmsixgl25qijfzn5urm.streamlit.app/)

## Sneak Peek
Get a glimpse of what awaits you in the simulation with movie and screenshot:

https://github.com/MySweetEden/predator_prey/assets/58873594/a82dbecc-87be-43bf-b49f-516688410201

![Population_transition_graph](https://github.com/MySweetEden/predator_prey/assets/58873594/0d4a8b8c-b671-4659-9a14-e13780bbf128)

## Key Features
Agent-Based Modeling: Leverages the Mesa library to create complex predator-prey interactions within a simulated ecosystem.  
Dynamic Visualization: Utilizes Plotly to provide insightful visualizations of the simulation process, allowing for real-time observation of agent behaviors and population changes.  
Customizable Parameters: Offers the ability to adjust various simulation parameters to explore different ecological scenarios and outcomes.
Interactive GUI: Fine-tune simulation parameters on-the-fly and explore different ecological scenarios.

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
# To run the simulation, execute the following py file.
streamlit run ./src/predator_prey/app.py

# Or, execute the following jupyter notebook.
./src/predator_prey/main.ipynb
```

## Usage
The simulation can be customized through various parameters defined in app.py or main.ipynb. Adjust these parameters to explore different predator-prey dynamics and ecological conditions.

## License
This project is licensed under the Apache-2.0 license.

## Acknowledgments
- [Mesa: An Agent-Based Modeling Framework](https://pdfs.semanticscholar.org/28a1/6e1b01b5897bde0e6fc676eacbc73d179ad6.pdf)
- [Agent-Based Models with Python: An Introduction to Mesa](https://www.complexityexplorer.org/courses/172-agent-based-models-with-python-an-introduction-to-mesa)
- [Creating a Simple Predator-Prey Model with Mesa: A Python Simulation Library](https://medium.com/@ulriktpedersen/creating-a-simple-predator-prey-model-with-mesa-a-python-simulation-library-4835f29791ae)
