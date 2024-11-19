const fs = require("fs");
const path = require("path");

function promptConstructor(args, variables = {}) {

  let prompt = "";
  args.forEach((arg) => {
    const filePath = path.join(__dirname + "/../prompts", arg);
    let fileContent = fs.readFileSync(filePath, "utf-8").trim();

    // Replace the placeholders in the file content with the variables passed
    Object.keys(variables).forEach((key) => {
      const placeholder = new RegExp(`{${key}}`, "g"); // Create a regex to match placeholders
      fileContent = fileContent.replace(placeholder, variables[key]);
    });

    prompt += fileContent;
  });
  return prompt;
}

module.exports = { promptConstructor };
