// functions/index.js
const functions = require("firebase-functions");

// Enable CORS for both domains
const cors = require('cors')({
  origin: [
    'https://sentimental-f95e6.web.app', 
    'https://sentimentalapp.com',
    'https://www.sentimentalapp.com',
    'https://sentimental-f95e6.firebaseapp.com'
  ],
  optionsSuccessStatus: 200
});

/**
 * Firebase Cloud Function to handle chat completions
 */
exports.chatCompletion = functions.https.onCall(async (data, context) => {
  try {
    // Import OpenAI inside the function to avoid initialization errors during deployment
    const { OpenAI } = require("openai");
    
    // Initialize OpenAI with the API key from environment variables
    const openai = new OpenAI({
      apiKey: process.env.OPENAI_API_KEY
    });
    
    // Validate input
    if (!data.messages || !Array.isArray(data.messages)) {
      throw new Error("Invalid messages format");
    }

    // Format messages for OpenAI API
    const messages = data.messages.map(msg => ({
      role: msg.role,
      content: msg.content
    }));

    // Ensure there's a system message if not provided
    if (!messages.some(msg => msg.role === 'system')) {
      messages.unshift({
        role: 'system',
        content: 'You are a thoughtful reflection guide, helping users explore their thoughts and feelings. Be empathetic, curious, and supportive. Ask thoughtful questions to help users gain deeper insights. Keep your responses relatively brief (2-3 paragraphs max) and always end with a gentle question to encourage further reflection.'
      });
    }

    // Call OpenAI API
    const completion = await openai.chat.completions.create({
      model: "gpt-3.5-turbo",
      messages: messages,
      max_tokens: 1000,
      temperature: 0.7,
    });

    // Extract and return the reply
    const reply = completion.choices[0].message.content;
    return { reply };
  } catch (error) {
    console.error("Error in chatCompletion:", error);
    
    // Return error information
    return {
      error: true,
      message: error.message,
      reply: "I apologize, but I'm having trouble processing your message. Please try again in a moment."
    };
  }
});

// Alternative REST API endpoint if you prefer to use fetch
exports.chatApi = functions.https.onRequest((request, response) => {
  return cors(request, response, async () => {
    try {
      // Import OpenAI inside the function to avoid initialization errors during deployment
      const { OpenAI } = require("openai");
      
      // Initialize OpenAI with the API key from environment variables
      const openai = new OpenAI({
        apiKey: process.env.OPENAI_API_KEY
      });
      
      // Only allow POST requests
      if (request.method !== 'POST') {
        return response.status(405).send({ error: 'Method not allowed' });
      }

      const { messages } = request.body;
      
      // Validate input
      if (!messages || !Array.isArray(messages)) {
        return response.status(400).send({ error: 'Invalid messages format' });
      }

      // Format messages for OpenAI API
      const formattedMessages = messages.map(msg => ({
        role: msg.role,
        content: msg.content
      }));

      // Ensure there's a system message if not provided
      if (!formattedMessages.some(msg => msg.role === 'system')) {
        formattedMessages.unshift({
          role: 'system',
          content: 'You are a thoughtful reflection guide, helping users explore their thoughts and feelings. Be empathetic, curious, and supportive. Ask thoughtful questions to help users gain deeper insights. Keep your responses relatively brief (2-3 paragraphs max) and always end with a gentle question to encourage further reflection.'
        });
      }

      // Call OpenAI API
      const completion = await openai.chat.completions.create({
        model: "gpt-3.5-turbo",
        messages: formattedMessages,
        max_tokens: 1000,
        temperature: 0.7,
      });

      // Extract and return the reply
      const reply = completion.choices[0].message.content;
      return response.status(200).send({ reply });
    } catch (error) {
      console.error("Error in chatApi:", error);
      return response.status(500).send({ 
        error: true, 
        message: error.message,
        reply: "I apologize, but I'm having trouble processing your message. Please try again in a moment."
      });
    }
  });
});