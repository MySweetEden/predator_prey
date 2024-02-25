from mesa import Agent, Model
from mesa.space import MultiGrid
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import random
import streamlit as st
import warnings

warnings.filterwarnings('ignore', category=FutureWarning)

custom_css = """
    <style>
        .stApp {
            margin-top: -50px;  /* Adjust the value as needed */
        }
    </style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

class Rabbit(Agent):
    def __init__(self, unique_id, pos, model):
        super().__init__(unique_id, model)
        self.pos = pos
        self.reproduce_ratio = REPRODUCE_RATIO_RABBITS
    
    def move(self):
        try:
            possible_moves = self.model.grid.get_neighborhood(
                self.pos,
                moore=True,
                include_center=False
            )
            new_position = self.random.choice(possible_moves)
            self.model.grid.move_agent(self, new_position)
        
        except Exception:
            pass
        
    def reproduce(self):
        if random.random() < self.reproduce_ratio:
            baby = self.model.create_agent(Rabbit, self.pos)
    
    def step(self):
        self.move()
        self.reproduce()

class Fox(Agent):
    def __init__(self, unique_id, pos, model):
        super().__init__(unique_id, model)
        self.pos = pos
        self.reproduce_ratio = REPRODUCE_RATIO_FOXES
        self.energy = ENERGY_INIT_FOXES
        self.energy_decrease = ENERGY_DECREASE_FOXES
        self.energy_recover = ENERGY_RECOVER_FOXES
    
    def move(self):
        try:
            possible_moves = self.model.grid.get_neighborhood(
                self.pos,
                moore=True,
                include_center=False
            )
            new_position = self.random.choice(possible_moves)
            if len(self.model.grid[new_position]) != 0:
                for agent in self.model.grid[new_position]:
                    if isinstance(agent, Rabbit):
                        prey = agent
                        self.model.grid.remove_agent(prey)
                        self.model.schedule.remove(prey)
                        self.energy += self.energy_recover
                        break
                    else:
                        pass
            
            self.model.grid.move_agent(self, new_position)
            self.energy -= self.energy_decrease
            if self.energy <= 0:
                self.model.grid.remove_agent(self)
                self.model.schedule.remove(self)

        except Exception:
            pass
    
    def reproduce(self):
        if random.random() < self.reproduce_ratio:
            baby = self.model.create_agent(Fox, self.pos)
    
    def step(self):
        self.move()
        self.reproduce()

class UniqueIDGenerator:
    def __init__(self):
        self._counters = {}

    def get_next_id(self, AgentClass):
        if AgentClass not in self._counters:
            self._counters[AgentClass] = 0
        self._counters[AgentClass] += 1
        return f"{AgentClass.__name__}_{self._counters[AgentClass]}"

class Environment(MultiGrid):
    def __init__(self, width, height):
        super().__init__(width, height, torus=False)
    
    def place_agent(self, agent, pos):
        super().place_agent(agent, pos)
    
    def move_agent(self, agent, pos):
        super().move_agent(agent, pos)

    def remove_agent(self, agent):
        super().remove_agent(agent)

class PredatorPrey(Model):
    def __init__(self, width, height):
        self.schedule = RandomActivation(self)
        self.grid = Environment(width, height)
        self.id_generator = UniqueIDGenerator()
        self._steps = 0
        self._time = 0
        self.dc = DataCollector(agent_reporters={
                "x": lambda a: a.pos[0],
                "y": lambda a: a.pos[1],
                "AgentType": lambda a: a.__class__.__name__
            }
        )

    def set_init_agent(self, AgentClass, num_agents):
        for _ in range(num_agents):
            self.create_agent(AgentClass)
    
    def create_agent(self, AgentClass, pos=None):
        agent_id = self.id_generator.get_next_id(AgentClass)
        if pos == None:
            x = random.randrange(self.grid.width)
            y = random.randrange(self.grid.height)
            pos = (x, y)
        agent = AgentClass(agent_id, pos, self)
        self.grid.place_agent(agent, pos)
        self.schedule.add(agent)
        return agent
    
    def plot_agent_movement(self):
        history_df = self.dc.get_agent_vars_dataframe()

        # When specific categorical values does not exist in step (e.g. Rabbit agent does not exist),
        # px.scatter behaves strangely (Data points remains on the plot)
        # So we need to add dummy values outside of the drawing range
        rabbit_df = pd.DataFrame(
            {"Step": np.arange(0,STEPS+1), "AgentID": ["Rabbit"]*(STEPS+1), "x": [-1]*(STEPS+1), "y": [-1]*(STEPS+1), "AgentType": ["Rabbit"]*(STEPS+1)}
        ).set_index(["Step", "AgentID"])
        fox_df = pd.DataFrame(
            {"Step": np.arange(0,STEPS+1), "AgentID": ["Fox"]*(STEPS+1), "x": [-1]*(STEPS+1), "y": [-1]*(STEPS+1), "AgentType": ["Fox"]*(STEPS+1)}
        ).set_index(["Step", "AgentID"])
        history_df = pd.concat([history_df, rabbit_df, fox_df])

        fig = px.scatter(history_df.reset_index(),
            x="x", y="y", animation_frame="Step",
            color="AgentType", hover_name="AgentID", animation_group="AgentID",
            range_x=[0,self.grid.width-1], range_y=[0,self.grid.height-1],
            title="Predator-Prey", width=600, height=600
        )
        fig.update_layout(
            xaxis=dict(
                dtick=1,
            ),
            yaxis=dict(
                dtick=1,
            )
        )
        return fig

    def plot_agent_population(self):
        history_df = self.dc.get_agent_vars_dataframe()
        rabbit_count = history_df[history_df["AgentType"] == "Rabbit"]["AgentType"].groupby("Step").count()
        fox_count = history_df[history_df["AgentType"] == "Fox"]["AgentType"].groupby("Step").count()
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=rabbit_count.index, y=rabbit_count, name="Rabbit"))
        fig.add_trace(go.Scatter(x=fox_count.index, y=fox_count, name="Fox"))
        fig.update_layout(
            title="Population transition graph",
            xaxis_title="Step", yaxis_title="Count",
            width=800, height=400,
            xaxis_range = [0,STEPS]
        )
        return fig

    def step(self):
        self.schedule.step()
        self.dc.collect(self)

st.title("Predator-Prey Simulation")

WIDTH = int(st.sidebar.number_input('WIDTH (int)', value=10))
HEIGHT = int(st.sidebar.number_input('HEIGHT (int)', value=10))
STEPS = int(st.sidebar.number_input('STEPS (int)', value=100))
NUM_RABBITS = int(st.sidebar.number_input('NUM_RABBITS (int)', value=10))
NUM_FOXES = int(st.sidebar.number_input('NUM_FOXES (int)', value=10))
REPRODUCE_RATIO_RABBITS = float(st.sidebar.number_input('REPRODUCE_RATIO_RABBITS (float)', value=0.1))
REPRODUCE_RATIO_FOXES = float(st.sidebar.number_input('REPRODUCE_RATIO_FOXES (float)', value=0.05))
ENERGY_INIT_FOXES = int(st.sidebar.number_input('ENERGY_INIT_FOXES (int)', value=10))
ENERGY_DECREASE_FOXES = int(st.sidebar.number_input('ENERGY_DECREASE_FOXES (int)', value=1))
ENERGY_RECOVER_FOXES = int(st.sidebar.number_input('ENERGY_RECOVER_FOXES (int)', value=10))
RANDOM_SEED = int(st.sidebar.number_input('RANDOM_SEED (int)', value=1))

random.seed(RANDOM_SEED)

model = PredatorPrey(WIDTH, HEIGHT)
model.set_init_agent(Rabbit, NUM_RABBITS)
model.set_init_agent(Fox, NUM_FOXES)
model.dc.collect(model)

for i in range(STEPS):
    model.step()

st.plotly_chart(model.plot_agent_movement(), use_container_width=True, theme=None)
st.plotly_chart(model.plot_agent_population(), use_container_width=True, theme=None)
