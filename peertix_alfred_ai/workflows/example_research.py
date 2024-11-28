from flytekit import task, workflow, conditional, ImageSpec
from crewai.crews.crew_output import CrewOutput

from peertix_alfred_ai.crews import (
    TopicClassifierCrew,
    ArtistResearchCrew,
    SportResearchCrew,
)

# image_spec = ImageSpec(
#     packages=["crewai"],
#     # base_image="peertix-alfred-ai:0974f51dd7c520da43eb163584ec7a8cb7659eb8",
#     # registry="localhost:30000",
# )


@task
def topic_classifier(topic: str) -> str:
    result: CrewOutput = TopicClassifierCrew().crew().kickoff(inputs={"topic": topic})
    return result.raw


@task
def artist_research(topic: str) -> str:
    result: CrewOutput = ArtistResearchCrew().crew().kickoff(inputs={"topic": topic})
    return result.raw


@task
def sport_research(topic: str) -> str:
    result: CrewOutput = SportResearchCrew().crew().kickoff(inputs={"topic": topic})
    return result.raw


@workflow
def example_research_wf(topic: str) -> str:
    topic_type = topic_classifier(topic=topic)
    return (
        conditional("topic_classifier")
        .if_(topic_type == "Musician")
        .then(artist_research(topic=topic))
        .elif_(topic_type == "Sport")
        .then(sport_research(topic=topic))
        .else_()
        .fail("Unkown.")
    )
