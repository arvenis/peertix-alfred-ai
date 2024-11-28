from os import getenv
from crewai import LLM, Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

from peertix_alfred_ai.tools.spotify_tool import SpotifyAPITool


@CrewBase
class ArtistResearchCrew:
    """Artist Research crew"""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    @agent
    def artist_identifying_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["artist_identifying_agent"],
            # tools=[MyCustomTool()], # Example of custom tool, loaded on the beginning of file
            # tools=[SpotifyAPITool()],
            # llm=LLM(model="ollama/qwen2.5:14b", base_url="http://localhost:11434"),
            llm=LLM(
                model="gemini/gemini-1.5-flash",
                api_key=getenv("GEMINI_API_KEY"),
            ),
            # llm=LLM(model="gpt-4"),
            verbose=True,
        )

    @agent
    def artist_research_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["artist_research_agent"],
            # tools=[MyCustomTool()], # Example of custom tool, loaded on the beginning of file
            tools=[SpotifyAPITool()],
            # llm=LLM(model="ollama/qwen2.5:14b", base_url="http://localhost:11434"),
            llm=LLM(
                model="gemini/gemini-1.5-flash",
                api_key=getenv("GEMINI_API_KEY"),
            ),
            # llm=LLM(model="gpt-4"),
            verbose=True,
        )

    @task
    def artist_identifying_task(self) -> Task:
        return Task(
            config=self.tasks_config["artist_identifying_task"],
        )

    @task
    def artist_research_task(self) -> Task:
        return Task(
            config=self.tasks_config["artist_research_task"],
            # output_file="concert.md",
        )

    @crew
    def crew(self) -> Crew:
        """Creates the ArtistResearch crew"""
        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,  # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )
