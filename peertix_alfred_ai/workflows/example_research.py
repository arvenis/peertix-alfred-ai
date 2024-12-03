from flytekit import task, workflow, conditional, LaunchPlan, current_context
from crewai.crews.crew_output import CrewOutput

from peertix_alfred_ai.env import ENVS

from peertix_alfred_ai.crews import (
    TopicClassifierCrew,
    ArtistResearchCrew,
    SportResearchCrew,
)


@task(container_image="peertix-alfred-ai:dev", environment=ENVS)
def topic_classifier(topic: str) -> str:
    result: CrewOutput = TopicClassifierCrew().crew().kickoff(inputs={"topic": topic})
    return result.raw


@task(container_image="peertix-alfred-ai:dev", environment=ENVS)
def artist_research(topic: str) -> str:
    result: CrewOutput = ArtistResearchCrew().crew().kickoff(inputs={"topic": topic})
    return result.raw


@task(container_image="peertix-alfred-ai:dev", environment=ENVS)
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


example_research_lp = LaunchPlan.create(
    name="example_research_lp", workflow=example_research_wf, default_inputs={"topic": "FC Barcelona"}
)

example_research_default_lp = LaunchPlan.get_default_launch_plan(current_context(), example_research_wf)
