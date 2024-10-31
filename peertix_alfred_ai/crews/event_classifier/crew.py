from crewai import LLM, Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task


@CrewBase
class EventClassifierCrew:
    """Event Classifier Crew"""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    @agent
    def event_classifier(self) -> Agent:
        return Agent(
            config=self.agents_config["event_classifier"],
            # tools=[MyCustomTool()], # Example of custom tool, loaded on the beginning of file
            # tools=[SpotifyAPITool()],
            llm=LLM(model="ollama/qwen2.5:14b", base_url="http://localhost:11434"),
            # llm=LLM(model="gpt-4"),
            verbose=True,
        )

    @task
    def event_classification_task(self) -> Task:
        return Task(
            config=self.tasks_config["event_classification_task"],
        )

    @crew
    def crew(self) -> Crew:
        """Creates the EventClassifier crew"""
        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,  # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )
