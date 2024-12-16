from flytekit import Secret
from peertix_alfred_ai.env import SecretConfig

# Define a secret for the firebase credentials
# The secret should live inside the same namespace as the task
# If the task runs in the project `peertix` and domain `development`
# then the secret should be in the `peertix-development` namespace
firebase_secret = Secret(
    group=SecretConfig.GROUP,
    key=SecretConfig.FIREBASE,
    mount_requirement=Secret.MountType.FILE,
)

serper_secret = Secret(
    group=SecretConfig.GROUP,
    key=SecretConfig.SERPER,
    mount_requirement=Secret.MountType.ENV_VAR,
)

spotify_id_secret = Secret(
    group=SecretConfig.GROUP,
    key=SecretConfig.SPOTIFY_CLIENT_ID,
    mount_requirement=Secret.MountType.ENV_VAR,
)

spotify_secret = Secret(
    group=SecretConfig.GROUP,
    key=SecretConfig.SPOTIFY_CLIENT_SECRET,
    mount_requirement=Secret.MountType.ENV_VAR,
)

gemini_secret = Secret(
    group=SecretConfig.GROUP,
    key=SecretConfig.GEMINI,
    mount_requirement=Secret.MountType.ENV_VAR,
)
