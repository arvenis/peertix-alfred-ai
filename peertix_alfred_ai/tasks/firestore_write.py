import firebase_admin
import firebase_admin.db
from firebase_admin import credentials
import firebase_admin.firestore
from flytekit import Secret, current_context, task

from peertix_alfred_ai.env import FirebaseConfig, ENVS

# Define a secret for the firebase credentials
# The secret should live inside the same namespace as the task
# If the task runs in the project `peertix` and domain `development`
# then the secret should be in the `peertix-development` namespace
firebase_secret = Secret(
    group=FirebaseConfig.SECRET_GROUP,
    key=FirebaseConfig.SECRET_NAME,
    mount_requirement=Secret.MountType.FILE,
)


@task(
    container_image="peertix-alfred-ai:dev",
    environment=ENVS,
    secret_requests=[firebase_secret],  # Provide the secret config
)
def write_to_firestore(collection: str, data: dict) -> None:
    """
    Write data to a Firebase firestore database.
    Args:
        `collection` (str): The firestore collection path.
        `data` (dict): The data to write to firestore.
    """

    # Get the Firabese secret from Flyte secret manager
    secret_manager = current_context().secrets
    credentials_file_path = secret_manager.get_secrets_file(FirebaseConfig.SECRET_GROUP, FirebaseConfig.SECRET_NAME)

    # Initialize Firebase
    cred = credentials.Certificate(credentials_file_path)
    firebase_admin.initialize_app(cred)

    # Write data to Firestore
    db = firebase_admin.firestore.client().collection(collection)
    db.add(data)
