# PeerTix Alfred AI

## Prerequisites

- A running Kubernetes cluster
- [Poetry](https://python-poetry.org/docs/#installation) installed with python 3.11 (<https://python-poetry.org/docs/main/managing-environments>)
- [flytectl](https://docs.flyte.org/projects/flytectl/en/latest/) installed
- [skaffold](https://skaffold.dev/docs/install) installed (you might need a newer version than the one installed on your system)

## Setup

Create a `.env` file in the root directory according to the `.env_example`:

```text
# API Key for Gemini
# https://aistudio.google.com/u/1/apikey
GEMINI_API_KEY=gemini_api_key

# Provide the API key for the SerperDev Tool to work
# https://serper.dev/
SERPER_API_KEY=serper_api_key

# Needed for the Spotify API Tool to work
# https://developer.spotify.com/documentation/web-api/quick-start/
SPOTIFY_CLIENT_ID=client_id
SPOTIFY_CLIENT_SECRET=client_secret
```

Install dependencies

```shell
poetry install
```

Get a shell running in the current virtual environment

```shell
poetry shell
```

Create Alfred AI image and install Flyte with all the dependencies (minio,postgres)

```shell
skaffold run
```

> If a new image is needed, simply run `skaffold run` again

Now we should have Flyte with all of it's dependencies running.

## Communication with the Flyte Admin API

Create a Flyte config file (`~/.flyte/config.yaml`) to communicate with the Flyte cluster

```yaml
admin:
  endpoint: localhost:8089 # Use the GRPC port that is forwarded from the Flyte Admin service
  authType: Pkce
  insecure: true
logger:
  show-source: true
  level: 6
```

Port forward following services to be able to communicate with Flyte

```shell
# Flyte Admin HTTP Server
kubectl port-forward svc/flyteadmin 8088:8088 -n flyte

# Flyte Admin GRPC Server
kubectl port-forward svc/flyteadmin 8089:8089 -n flyte

# MinIO
kubectl port-forward svc/minio 9000:9000 -n flyte

# Flyte Console (Not necessery to run the workflow)
kubectl port-forward svc/flyteconsole 8080:8080 -n flyte
```

Now you should be able to run workflows on the Flyte cluster via the CLI

```shell
pyflyte run --remote peertix_alfred_ai/workflows/process_ticket.py process_ticket_wf
```

## Using requests to interact with the Flyte Admin API

We need to use the HTTP Server of Flyte Admin API to communicate with the Flyte cluster.

The OpenAPI documentation can be found at `http://localhost:8088/api/v1/docs`

Example for an execution:

```shell
curl -X GET "http://localhost:8088/api/v1/data/executions/flytesnacks/development/a4srxvhjzq5qbvtdpw2r" -H "Accept: application/json"
```

Response:

```json
{
  "outputs": {
    "url": "",
    "bytes": "0"
  },
  "inputs": {
    "url": "",
    "bytes": "0"
  },
  "full_inputs": {
    "literals": {
      "topic": {
        "scalar": {
          "primitive": {
            "string_value": "FC Barcelona"
          }
        },
        "hash": "",
        "metadata": {}
      }
    }
  },
  "full_outputs": {
    "literals": {
      "o0": {
        "scalar": {
          "primitive": {
            "string_value": "The observation above contains links to various websites providing information on FC Barcelona's previous and upcoming matches, current standings, and relevant statistics.  These sites include Soccerway, FcTables, FootyStats, ESPN, WhoScored, Sky Sports, the official FC Barcelona website, and Sofascore.  The snippets provide a preview of the type of data available on each site, including match results, league standings, team statistics, and upcoming fixtures.  To access the complete information, please visit the links provided."
          }
        },
        "hash": "",
        "metadata": {}
      }
    }
  }
}
```
