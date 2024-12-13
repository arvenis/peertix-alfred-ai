import base64
import json
import time
from os import getenv
from pathlib import Path

from flytekit import task, workflow
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_google_genai import ChatGoogleGenerativeAI

from peertix_alfred_ai.env import ENVS
from peertix_alfred_ai.lib.utils import logger, prompt_constructor
from peertix_alfred_ai.tasks.firestore_write import write_to_firestore


@task(container_image="peertix-alfred-ai:dev", environment=ENVS)
def process_ticket() -> dict:
    start_time = time.time()
    logger.info("Starting ticket processing")
    test_ticket_path = Path(__file__).parent.parent / "examples" / "test_ticket.jpeg"
    logger.debug(test_ticket_path)
    with open(test_ticket_path, "rb") as f:
        scanned_ticket_image = base64.b64encode(f.read()).decode("utf-8")

    # Initialize Gemini model
    model = ChatGoogleGenerativeAI(
        model="gemini-1.5-flash",
        max_output_tokens=2048,
        api_key=getenv("GEMINI_API_KEY"),
    )

    # Read OpenAPI definition
    bundled_openapi_def_path = Path(__file__).parent / "bundled-openapi-def.yaml"
    with open(bundled_openapi_def_path, "r", encoding="utf-8") as f:
        pt_openapi_scheme = f.read().strip()

    # Define template variables
    variables = {"proccess_ticket_request_schema": pt_openapi_scheme}

    # Construct system prompt
    system_input = prompt_constructor(
        ["p0_guidelines.jinja", "p1_get_ticket_details.jinja", "p2_ticket_examples.jinja"], variables
    )

    # Prepare messages
    messages = [
        SystemMessage(content=system_input),
        HumanMessage(
            content=[
                {
                    "type": "text",
                    "text": "From the pdf provided, acquire all the data required to create a valid digital twin of the ticket and its corresponding event, program and order! Fill all values based on the OpenAPI schema! Your answer will be deserialised and if one of the values are missing, it will fail! Please make sure you will acquire the ticketcode properly that could be ONLY within the QR or barcode that is the MOST important value of all! You must fill all attributes that are defined inside the OpenAPI description, always try to out a logical value there, even if it is not on the ticket. For example, if the toDate for an event is missing, use the from date. NEVER use the value null! Write NA for string types, write 0 for integer and write 0.0 for double types if you cannot find out the value!",
                },
                {
                    "type": "image_url",
                    # "image_url": f"data:application/pdf;base64,{scanned_ticket_image}",
                    "image_url": f"data:image/jpeg;base64,{scanned_ticket_image}",
                },
            ]
        ),
    ]

    # Invoke model
    logger.info("Invoking Gemini model")
    result = model.invoke(messages)

    try:
        # Clean and parse response
        cleaned_str = result.content.strip().replace("```json\n", "").replace("\n```", "")
        cleaned_obj = json.loads(cleaned_str)

        response = {"processedTicket": cleaned_obj}

        logger.debug("Processed ticket: {response}")
        logger.info("--- FINISHED %s seconds ---" % (time.time() - start_time))
        return response

    except json.JSONDecodeError as error:
        print(f"Error parsing JSON: {error}")
        return {"error": f"Something went wrong: {str(error)}"}


@workflow
def process_ticket_wf() -> None:
    processed_ticket = process_ticket()
    write_to_firestore(collection="test_details", data=processed_ticket)

    # *This would automatically start in parallel with the other write_to_firestore task :D
    # write_to_firestore(collection="test_details", data=processed_ticket)
