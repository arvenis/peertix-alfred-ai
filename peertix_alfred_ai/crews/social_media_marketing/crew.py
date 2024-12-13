import os
import secrets
import string
import uuid

from crewai import LLM, Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

# Check our tools documentations for more information on how to use them
from crewai_tools import (
    MDXSearchTool,
    RagTool,
    ScrapeElementFromWebsiteTool,
    ScrapeWebsiteTool,
    SerperDevTool,
    TXTSearchTool,
    WebsiteSearchTool,
    YoutubeVideoSearchTool,
)

from peertix_alfred_ai.tools import InstagramAPITool

# from peertix_alfred_ai.tools import SpotifyAPITool


# Initialize Market Research Tool
market_research_tool = SerperDevTool()
# Initialize Competitor Scraping Tool
competitor_scraping_tool = ScrapeWebsiteTool()
# Initialize Content Keyword Analysis Tool
txt_search_tool = TXTSearchTool()
# Initialize YouTube Video Search Tool
youtube_video_search_tool = YoutubeVideoSearchTool()
# Initialize Website Element Scraping Tool
scrape_element_tool = ScrapeElementFromWebsiteTool()
# Initialize Research Assistance Tool
rag_tool = RagTool()

instagramAPITool = InstagramAPITool()


@CrewBase
class SocialMediaMarketingCrew:
    """Social Media Marketing crew"""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    def generate_unique_hash(length=5):
        # Define the characters to use in the hash (alphanumeric)
        characters = string.ascii_letters + string.digits
        # Generate a random hash of the specified length
        hash_value = "".join(secrets.choice(characters) for _ in range(length))
        return hash_value

    @agent
    def lead_market_analyst_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["lead_market_analyst_agent"],
            tools=[SerperDevTool(), ScrapeWebsiteTool()],
            # tools=[SpotifyAPITool()],
            # llm=LLM(model="ollama/qwen2.5:14b", base_url="http://localhost:11434"),
            llm=LLM(model="gemini/gemini-1.5-pro-002", api_key=os.getenv("GEMINI_API_KEY")),
            # llm=LLM(model="gpt-4o", api_key=os.getenv("OPENAI_API_KEY")),
            verbose=True,
        )

    @agent
    def social_media_content_creator_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["social_media_content_creator_agent"],
            # tools=[MyCustomTool()], # Example of custom tool, loaded on the beginning of file
            tools=[instagramAPITool, YoutubeVideoSearchTool()],
            # llm=LLM(model="ollama/qwen2.5:14b", base_url="http://localhost:11434"),
            # llm=LLM(model="gemini/gemini-1.5-pro-002", api_key=os.getenv("GEMINI_API_KEY")),
            llm=LLM(model="gpt-4o", api_key=os.getenv("OPENAI_API_KEY")),
            verbose=True,
        )

    @agent
    def trend_analyst_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["trend_analyst_agent"],
            # tools=[MyCustomTool()], # Example of custom tool, loaded on the beginning of file
            tools=[SerperDevTool(), WebsiteSearchTool()],
            # llm=LLM(model="ollama/qwen2.5:14b", base_url="http://localhost:11434"),
            llm=LLM(model="gemini/gemini-1.5-pro-002", api_key=os.getenv("GEMINI_API_KEY")),
            # llm=LLM(model="gpt-4o", api_key=os.getenv("OPENAI_API_KEY")),
            verbose=True,
        )

    @agent
    def chief_marketing_strategist_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["chief_marketing_strategist_agent"],
            # tools=[MyCustomTool()], # Example of custom tool, loaded on the beginning of file
            tools=[MDXSearchTool()],
            # llm=LLM(model="ollama/qwen2.5:14b", base_url="http://localhost:11434"),
            llm=LLM(model="gemini/gemini-1.5-pro-002", api_key=os.getenv("GEMINI_API_KEY")),
            # llm=LLM(model="gpt-4o", api_key=os.getenv("OPENAI_API_KEY")),
            verbose=True,
        )

    @task
    def market_and_product_analyssis_task(self) -> Task:
        return Task(
            config=self.tasks_config["market_and_product_analyssis_task"],
        )

    @task
    def competitor_researh_and_trend_identification_task(self) -> Task:
        return Task(config=self.tasks_config["competitor_researh_and_trend_identification_task"])

    @task
    def social_media_content_creation_task(self) -> Task:
        return Task(
            config=self.tasks_config["social_media_content_creation_task"],
            output_file=f"results/marketing_posts_{uuid.uuid4().hex}.md",
        )

    @task
    def keyword_and_hashtag_research_task(self) -> Task:
        return Task(config=self.tasks_config["keyword_and_hashtag_research_task"])

    @task
    def content_review_and_strategic_oversight_task(self) -> Task:
        return Task(
            config=self.tasks_config["content_review_and_strategic_oversight_task"],
            output_file=f"results/marketing_posts_{uuid.uuid4().hex}.md",
        )

    @crew
    def crew(self) -> Crew:
        """Creates the SocialMediaResearchCrew crew"""
        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,  # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )
