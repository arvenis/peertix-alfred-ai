# Inside peertix_alfred_ai/crews/event_classifier/__init__.py
from .artist_research.crew import ArtistResearchCrew
from .event_classifier.crew import EventClassifierCrew
from .topic_classifier.crew import TopicClassifierCrew
from .sport_research.crew import SportResearchCrew
from .social_media_marketing.crew import SocialMediaMarketingCrew

# You can optionally define __all__ to specify what to import when
# using 'from event_classifier import *'
__all__ = [
    "ArtistResearchCrew",
    "EventClassifierCrew",
    "TopicClassifierCrew",
    "SportResearchCrew",
    "SocialMediaMarketingCrew",
]
