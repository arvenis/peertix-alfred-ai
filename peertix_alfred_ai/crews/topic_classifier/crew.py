from crewai import LLM, Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool
from dotenv import load_dotenv
from os import getenv

load_dotenv()


@CrewBase
class TopicClassifierCrew:
    """Topic Classifier Crew"""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    @agent
    def topic_classifier(self) -> Agent:
        return Agent(
            config=self.agents_config["topic_classifier"],
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
    def topic_classification_task(self) -> Task:
        return Task(
            config=self.tasks_config["topic_classification_task"],
        )

    @crew
    def crew(self) -> Crew:
        """Creates the TopicClassifier crew"""
        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,  # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )
