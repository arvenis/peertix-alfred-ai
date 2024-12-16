import logging
from pathlib import Path
from jinja2 import Environment, FileSystemLoader
from flytekit import current_context

from peertix_alfred_ai.env import LOG_LEVEL, SecretConfig

logging.basicConfig(format="[%(asctime)s] [%(levelname)s] %(message)s", level=LOG_LEVEL)
logger = logging.getLogger(__name__)


def get_rendered_template(templateFolder: str, templateName: str, templateData: any) -> str:  # type: ignore
    return (
        Environment(loader=FileSystemLoader(templateFolder), trim_blocks=True, lstrip_blocks=True)
        .get_template(templateName)
        .render(**templateData)
    )


def prompt_constructor(args, variables=None):
    if variables is None:
        variables = {}

    prompt = ""
    base_path = Path(__file__).parent.parent / "prompts"

    for arg in args:
        formatted_content = get_rendered_template(
            str(base_path),
            arg,
            variables,
        )
        prompt += formatted_content

    return prompt


def get_secret_value(secret_name: str) -> str:
    """
    Get the value of a secret from the current context.
    Args:
        `secret_name` (str): The name of the secret to get the value of.
    Returns:
        str: The value of the secret.
    Throws an exception if the secret is not found.
    """
    context = current_context()
    return context.secrets.get(SecretConfig.GROUP, secret_name)


def get_secret_file_path(secret_name: str) -> str:
    """
    Get the path to a secret file from the current context.
    Args:
        `secret_name` (str): The name of the secret to get the value of.
    Returns:
        str: The path to the secret file.
    Throws an exception if the secret is not found.
    """
    context = current_context()
    return context.secrets.get_secrets_file(SecretConfig.GROUP, secret_name)
