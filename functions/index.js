require('dotenv').config();
const functions = require("firebase-functions");
const admin = require("firebase-admin");
const { OpenAI } = require("openai");
const { onCall } = require("firebase-functions/v2/https");

admin.initializeApp();
const openai = new OpenAI({ apiKey: process.env.OPENAI_API_KEY });

exports.chatCompletion = onCall(async (request) => {
  const { messages } = request.data;
  console.log("Received messages:", messages);

  if (!messages || !Array.isArray(messages)) {
    throw new functions.https.HttpsError("invalid-argument", "messages must be an array");
  }

  try {
    const response = await openai.chat.completions.create({
      model: "gpt-4",
      messages: messages,
    });

    const reply = response.choices[0].message.content;
    return { reply };
  } catch (error) {
    console.error("OpenAI API error:", error);
    throw new functions.https.HttpsError("internal", "Failed to generate reply");
  }
});