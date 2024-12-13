import uuid

import firebase_admin
import firebase_admin.db
import firebase_admin.firestore
from firebase_admin import credentials
from flytekit import Secret, current_context, task

from peertix_alfred_ai.env import ENVS, FirebaseConfig
from peertix_alfred_ai.lib.utils import logger

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
def write_to_firestore(collection: str, data: dict, id: str | None = None) -> str:
    """
    Write data to a Firebase firestore database.
    Args:
        `collection` (str): The firestore collection path.
        `data` (dict): The data to write to firestore.
        `id` (str, optional): The ID of the document to write to. If not provided, a new UUID will be generated.
    Returns:
        str: The ID of the document that was written.
    """

    # Get the Firabese secret from Flyte secret manager
    secret_manager = current_context().secrets
    credentials_file_path = secret_manager.get_secrets_file(FirebaseConfig.SECRET_GROUP, FirebaseConfig.SECRET_NAME)

    # Initialize Firebase
    cred = credentials.Certificate(credentials_file_path)
    firebase_admin.initialize_app(cred)
    logger.info("Firebase init successful")

    # Write data to Firestore
    logger.debug(f"Writing data to Firestore: {data}")
    db = firebase_admin.firestore.client().collection(collection)

    # If id is not provided, generate a new UUID
    if id is None:
        id = str(uuid.uuid4())

    db.document(id).set(data)

    logger.info(f"Document written with ID: {id}")
    return id
