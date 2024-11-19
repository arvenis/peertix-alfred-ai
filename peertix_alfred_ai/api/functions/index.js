// Import Firebase Functions and Firebase Admin SDK
const functions = require("firebase-functions");
const { setGlobalOptions } = require("firebase-functions/v2");
const { defineString, defineSecret } = require("firebase-functions/params");

const { ChatGoogleGenerativeAI } = require("@langchain/google-genai");
const { HumanMessage, SystemMessage } = require("@langchain/core/messages");
const { readFileSync } = require("fs");
const fs = require("fs");
const yaml = require("js-yaml");
const { promptConstructor } = require("./utils/utils.js");

const admin = require("firebase-admin");
const { onCall, HttpsError } = require("firebase-functions/v2/https");

admin.initializeApp();

setGlobalOptions({ region: "europe-west3" });

// define gemini api
const geminiApiKey = defineSecret('GEMINI_API_KEY');

const mediaPath = __dirname;

// A callable function that requires authentication
exports.ptTicketProcessingApi = onCall(async (request) => {
  console.log("request:", request); // Log the context for debugging

  // Checking that the user is authenticated.
  if (!request.auth) {
    // Throwing an HttpsError so that the client gets the error details.
    throw new HttpsError(
      "failed-precondition",
      "The function must be " + "called while authenticated."
    );
  }
  
  const body = request.data;
  scannedTicketImage = body.pdf;

  // // Decode the base64 string to binary data
  const buffer = Buffer.from(scannedTicketImage, "base64");

  const model = new ChatGoogleGenerativeAI({
    model: "gemini-1.5-pro-002",
    // model: "gemini-1.5-flash",
    maxOutputTokens: 2048,
    apiKey: geminiApiKey.value(),
  });

  // Read the openapi definition content 
  // todo: get this from secret when this logic sits in k8s
  const pt_openapi_scheme = fs.readFileSync(
    `${mediaPath}/bundled-openapi-def.yaml`,
    "utf8"
  );
  // Parse YAML content into a JavaScript object
  const pt_ticket_form = yaml.load(pt_openapi_scheme);

  // Define the variables to replace in the template
  const variables = {
    proccess_ticket_request_schema: pt_ticket_form,
  };

  system_input = promptConstructor(
    ["p0_guidelines", "p1_get_ticket_details", "p2_ticket_examples"],
    variables
  );

  const messages = [
    new SystemMessage((content = system_input)),
    new HumanMessage({
      content: [
        {
          type: "text",
          text: "From the pdf provided, acquire all the data required to create a valid digital twin of the ticket and its corresponding event, program and order! Fill all values based on the OpenAPI schema! Your answer will be deserialised and if one of the values are missing, it will fail! Please make sure you will acquire the ticketcode properly that could be ONLY within the QR or barcode that is the MOST important value of all! You must fill all attributes that are defined inside the OpenAPI description, always try to out a logical value there, even if it is not on the ticket. For example, if the toDate for an event is missing, use the from date. NEVER use the value null! Write NA for string types, write 0 for integer and write 0.0 for double types if you cannot find out the value!",
        },
        {
          type: "image_url",
          image_url: `data:application/pdf;base64,${buffer.toString("base64")
          }`,
          // image_url: `data:application/pdf;base64,${image}`,
        },
      ],
    }),
  ];

  //  Invoke the model with the combined input
  result = await model.invoke(messages);

  // todo: silly xd
  // Step 1: Remove the extra ```json\n and \n``` parts
  const cleanedStr = result.content
    .toString()
    .replace(/^```json\n/, "")
    .replace(/\n```$/, "");

  // Step 2: Parse the cleaned string into a JSON object
  try {
    // Assume cleanedStr is a string that can be parsed into an object
    const cleanedObj = JSON.parse(cleanedStr); // Parse the cleanedStr to an object if needed
    console.log(cleanedStr);

    const response = {
      header: {
        txId: "string", // You can replace this with the actual transaction ID or another identifier
      },
      processedTicket: cleanedObj, // Assuming cleanedStr is a representation of the processed ticket
    };

    // Ensure response is sent only once

    return { response };
  } catch (error) {
    console.error("Error parsing JSON:", error);
    return { status: 500, error: "Something went wrong" + error.message };
  }
});
