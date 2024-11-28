from os import getenv
from crewai import LLM, Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool


@CrewBase
class SportResearchCrew:
    """Sport Research Crew"""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    @agent
    def sport_research_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["sport_research_agent"],
            # tools=[MyCustomTool()], # Example of custom tool, loaded on the beginning of file
            tools=[SerperDevTool()],
            # llm=LLM(model="ollama/qwen2.5:14b", base_url="http://localhost:11434"),
            llm=LLM(
                model="gemini/gemini-1.5-flash",
                api_key=getenv("GEMINI_API_KEY"),
            ),
            # llm=LLM(model="gpt-4"),
            verbose=True,
        )

    @task
    def sport_research_task(self) -> Task:
        return Task(
            config=self.tasks_config["sport_research_task"],
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Sport Research crew"""
        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,  # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )
