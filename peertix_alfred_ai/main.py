from crewai.crews.crew_output import CrewOutput

from peertix_alfred_ai.crews import (
    # EventClassifierCrew,
    ArtistResearchCrew,
    TopicClassifierCrew,
    SportResearchCrew,
    SocialMediaMarketingCrew,
)


def main():
    topic = "Ed Rush"
    result: CrewOutput = TopicClassifierCrew().crew().kickoff(inputs={"topic": topic})

    topic_type = result.raw

    match topic_type:
        case "Musician":
            response = ArtistResearchCrew().crew().kickoff(inputs={"topic": topic})
            print(response)
        case "Sport":
            response = SportResearchCrew().crew().kickoff(inputs={"topic": topic})
            print(response)
        case _:
            print("Unknown event detected")


def run_artist_research_crew():
    event_name = "Bladerunnaz pres. Audio - Ed Rush - Merikan - Pythius - Spor"
    result: CrewOutput = (
        ArtistResearchCrew().crew().kickoff(inputs={"event_name": event_name})
    )
    print(result)


def run_topic_classifier_crew():
    topic = "Ed Rush"
    result: CrewOutput = TopicClassifierCrew().crew().kickoff(inputs={"topic": topic})
    print(result)


def run_sport_research_crew():
    topic = "FC Barcelona"
    result: CrewOutput = SportResearchCrew().crew().kickoff(inputs={"topic": topic})
    print(result)

def run_instagram_research_crew():
    product_desc = ''''''
    result: CrewOutput = SocialMediaMarketingCrew().crew().kickoff(inputs={"product_desc": product_desc})
    print(result)