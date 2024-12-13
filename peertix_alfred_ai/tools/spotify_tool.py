import json
import os
import requests
from crewai_tools import BaseTool


class SpotifyAPITool(BaseTool):
    name: str = "Spotify API Tool"
    description: str = "This tool allows you to interact with the Spotify API and get " "information about an artist."

    def get_spotify_access_token(self, client_id, client_secret):
        auth_url = "https://accounts.spotify.com/api/token"
        auth_response = requests.post(
            auth_url,
            {
                "grant_type": "client_credentials",
                "client_id": client_id,
                "client_secret": client_secret,
            },
        )

        if auth_response.status_code != 200:
            raise Exception("Failed to get Spotify access token")

        auth_data = auth_response.json()
        return auth_data["access_token"]

    def search_artist_on_spotify(self, artist_name, token):
        search_url = "https://api.spotify.com/v1/search"
        headers = {"Authorization": f"Bearer {token}"}
        params = {"q": artist_name, "type": "artist", "limit": 1}

        response = requests.get(search_url, headers=headers, params=params)

        if response.status_code != 200:
            raise Exception("Failed to search artist on Spotify")

        search_results = response.json()
        if len(search_results["artists"]["items"]) == 0:
            raise Exception(f"No artist found for {artist_name}")

        artist = search_results["artists"]["items"][0]
        return (
            artist["id"],
            artist["name"],
            artist["followers"]["total"],
            artist["popularity"],
        )

    def get_artist_listeners(self, artist_id, token):
        artist_url = f"https://api.spotify.com/v1/artists/{artist_id}"
        headers = {"Authorization": f"Bearer {token}"}

        response = requests.get(artist_url, headers=headers)

        if response.status_code != 200:
            raise Exception(f"Failed to fetch artist details for ID: {artist_id}")

        artist_data = response.json()
        return artist_data

    def _run(self, artist_name: str) -> str:
        token = self.get_spotify_access_token(os.getenv("SPOTIFY_CLIENT_ID"), os.getenv("SPOTIFY_CLIENT_SECRET"))

        # Search for artist on Spotify
        artist_id, name, followers, popularity = self.search_artist_on_spotify(artist_name, token)

        # Fetch detailed artist info including monthly listeners
        artist_data = self.get_artist_listeners(artist_id, token)

        return json.dumps(artist_data)
