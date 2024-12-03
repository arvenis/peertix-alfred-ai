from pathlib import Path
from jinja2 import Environment, FileSystemLoader

# env = Environment(loader=PackageLoader("peertix_alfred_ai"), autoescape=select_autoescape())


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


if __name__ == "__main__":
    prompt_constructor(["p1_get_ticket_details.jinja"], {"proccess_ticket_request_schema": "asd"})
