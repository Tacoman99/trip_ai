from crewai_tools import SerperDevTool, ScrapeWebsiteTool
from crewai import Agent, LLM, Task, Crew, Process
from config.base_models import City_guide
from tools.google_places_tool import GooglePlacesTool
import yaml
from typing import Dict


# Define file paths for YAML configurations
files = {   
    "agents": "config/agents.yaml",
    "tasks": "config/tasks.yaml",
        }

        # Load configurations from YAML files
configs = {}
for config_type, file_path in files.items():
    with open(file_path, "r") as file:
        configs[config_type] = yaml.safe_load(file)

class ResearchCrew:
    """
    A crew of agents to plan a trip
    """

    def __init__(
        self,
        model: str,
        api_key: str,
        travelers_input: str,

    ):
        """
        Initialize the TripCrew

        Args:
          model: The model to use
          api_key: The API key to use
          travelers_input: The inputs for the crew
          agents_config: The configuration for the agents
          tasks_config: The configuration for the tasks

        Returns:
          result: The result of the crew
        """


        # Assign loaded configurations to specific variables
        self.llm = LLM(model=model, api_key=api_key, timeout=60)
        self.model = model
        self.api_key = api_key
        self.travelers_input = travelers_input
        self.agents_config = configs["agents"]
        self.tasks_config = configs["tasks"]

    def run(self):
        # Initialize the agents
        local_expert_agent = Agent(
            llm=self.llm,
            config=self.agents_config["local_expert_agent"],
            cache=True,
            tools=[SerperDevTool(), ScrapeWebsiteTool()],
        )
        google_search_agent = Agent(
            llm=self.llm,
            config=self.agents_config["google_search_agent"],
            cache=True,
            tools=[GooglePlacesTool()],
        )

        # itinerary_agent = Agent(
        #     llm=self.llm,
        #     config=self.agents_config["itinerary_agent"],
        #     tools=[GooglePlacesTool()],
        # )

        # Initialize the tasks

        gather_task = Task(
            agent=local_expert_agent,
            config=self.tasks_config["gather_task"],
            output_pydantic=City_guide,
        )
        reviews_task = Task(
            agent=google_search_agent,
            config=self.tasks_config["reviews_task"],
            output_pydantic=City_guide,
            output_file="guide.json",
        )
        # plan_task = Task(
        #     agent=itinerary_agent,
        #     config=self.tasks_config["plan_task"],
        #     context=[gather_task],
        #     output_file="itinerary2.md",
        # )

        crew = Crew(
            agents=[local_expert_agent,google_search_agent],
            tasks=[gather_task,reviews_task],
            process=Process.sequential,
            verbose=True,
        )
        #converting the travelers_input to a dictionary
        inputs = {"travelers_input": self.travelers_input}

        result = crew.kickoff(inputs=inputs)
        return result

class PlanCrew:
    """
    A crew of agents to plan a trip
    """

    def __init__(
        self,
        model: str,
        api_key: str,
        travelers_input: str,  # Fixed indentation
        crew_output: Dict,


    ):
        self.llm = LLM(model=model, api_key=api_key, timeout=60)
        self.model = model
        self.api_key = api_key
        self.travelers_input = travelers_input
        self.crew_output = crew_output
        self.agents_config = configs["agents"]
        self.tasks_config = configs["tasks"]

    def run(self):
        # Fixed indentation
        # Initialize the agent
        itinerary_agent = Agent(
            llm=self.llm,
            config=self.agents_config["itinerary_agent"],
            tools=[GooglePlacesTool()],
        )

        itinerary_task = Task(
            agent=itinerary_agent,
            config=self.tasks_config["plan_task"],
            output_file="docs/itinerary.md",
        )

        crew = Crew(
            agents=[itinerary_agent],
            tasks=[itinerary_task],
            process=Process.sequential,
            verbose=True,
        )
        
        # Converting the travelers_input to a dictionary
        inputs = {"travelers_input": self.travelers_input, "crew_output": self.crew_output}

        
        result = crew.kickoff(inputs=inputs)
        return result
