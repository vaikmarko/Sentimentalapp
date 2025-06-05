const functions = require('firebase-functions');
const admin = require('firebase-admin');
const OpenAI = require("openai");

admin.initializeApp();

const openai = new OpenAI({
  apiKey: functions.config().openai.key,
});

// Generate assistant response (chat-style)
exports.chatCompletion = functions.https.onCall(async (data, context) => {
  const { messages, model } = data;

  try {
    const completion = await openai.chat.completions.create({
      model: model || 'gpt-4',
      messages: messages,
    });

    return { reply: completion.choices[0].message.content };
  } catch (error) {
    console.error("chatCompletion error:", error);
    throw new functions.https.HttpsError('internal', error.message);
  }
});

// Analyze story progress
exports.analyzeProgress = functions.https.onCall(async (data, context) => {
  const { storyId } = data;

  try {
    const storyDoc = await admin.firestore().collection('stories').doc(storyId).get();

    if (!storyDoc.exists) {
      throw new functions.https.HttpsError('not-found', 'Story not found');
    }

    const storyData = storyDoc.data();
    const conversation = storyData.conversation;

    if (!Array.isArray(conversation)) {
      throw new functions.https.HttpsError('invalid-argument', 'Conversation missing or invalid');
    }

    const completion = await openai.chat.completions.create({
      model: 'gpt-4',
      messages: [
        {
          role: "system",
          content:
            "You are a calm and thoughtful conversational partner who helps people uncover meaningful personal stories. Your role is to evaluate how emotionally whole and narratively complete the story feels based on the conversation so far. Focus on emotional flow, vulnerability, insight, and coherence. Return only a JSON object like: { \"percent\": 75 }.",
        },
        ...conversation,
        {
          role: "system",
          content:
            "Provide a JSON object with a single key 'percent' indicating the story completeness as an integer percentage (0-100).",
        },
      ],
    });

    const result = completion.choices[0].message.content;
    let percent = 0;

    try {
      const json = JSON.parse(result);
      if (typeof json.percent === 'number') {
        percent = json.percent;
      }
    } catch (e) {
      console.error("Failed to parse analyzeProgress result:", result);
    }

    return { percent };
  } catch (error) {
    console.error("analyzeProgress error:", error);
    throw new functions.https.HttpsError('internal', error.message);
  }
});

// Generate formatted version of story (tweet, poem, etc.)
exports.generateFormat = functions.https.onCall(async (data, context) => {
  const { storyId, formatType } = data;

  try {
    const storyDoc = await admin.firestore().collection('stories').doc(storyId).get();

    if (!storyDoc.exists) {
      throw new functions.https.HttpsError('not-found', 'Story not found');
    }

    const storyData = storyDoc.data();
    const base = storyData.gptGeneratedText || storyData.text || '';

    let prompt = '';
    if (formatType === 'tweet') {
      prompt = `Summarize the following story as a viral, deeply personal and insightful tweet (max 240 characters, no hashtags):\n\n${base}`;
    } else if (formatType === 'poem') {
      prompt = `Write a brief, free verse poem (max 5 lines) summarizing the inner journey of this story:\n\n${base}`;
    } else if (formatType === 'script') {
      prompt = `Turn the story into a short script or dialogue (max 5 exchanges), focusing on the emotional core and life insight:\n\n${base}`;
    } else if (formatType === 'therapeutic' || formatType === 'insight') {
      prompt = `Give a therapeutic summary of this story: What is the main lesson, what inner dynamic or emotion is being worked through? Give advice for self-reflection or growth. (max 3 sentences)\n\n${base}`;
    } else {
      prompt = `Rewrite this story in the format of a ${formatType}:\n\n${base}`;
    }

    const completion = await openai.chat.completions.create({
      model: 'gpt-4',
      messages: [{ role: 'user', content: prompt }],
    });

    return { result: completion.choices[0].message.content };
  } catch (error) {
    console.error("generateFormat error:", error);
    throw new functions.https.HttpsError('internal', error.message);
  }
});

// Generate full story and save it
exports.generateFullStory = functions.https.onCall(async (data, context) => {
  const { storyId } = data;

  try {
    const storyRef = admin.firestore().collection('stories').doc(storyId);
    const storySnap = await storyRef.get();

    if (!storySnap.exists) {
      throw new functions.https.HttpsError('not-found', 'Story not found');
    }

    const storyData = storySnap.data();
    const conversation = storyData.conversation;

    if (!Array.isArray(conversation)) {
      throw new functions.https.HttpsError('invalid-argument', 'Conversation is missing');
    }

    // --- Lisa keele tuvastus ---
    const userText = conversation
      .filter(msg => msg.role === "user")
      .map(msg => msg.content)
      .join(" ");

    let detectedLang = "en";
    try {
      const langResult = await openai.chat.completions.create({
        model: 'gpt-4',
        messages: [
          {
            role: "system",
            content: "You are a language identifier. Detect the language of the following text. Reply only with the 2-letter ISO code (e.g., 'et' for Estonian, 'en' for English, 'ru' for Russian)."
          },
          {
            role: "user",
            content: userText
          }
        ],
        max_tokens: 10,
      });
      detectedLang = langResult.choices[0].message.content.trim().replace(/[^a-z]/gi, '').slice(0,2).toLowerCase();
    } catch (err) {
      console.error("Language detection failed, fallback to EN.", err);
    }

    // --- Loo prompt, mis annab korralduse kirjutada pealkiri ja tekst õiges keeles ---
    const promptObj = {
      role: "system",
      content:
        `You are a masterful, empathetic personal storyteller. Based on the following authentic conversation, write a compelling, emotionally intelligent real-life story. The result must sound like a genuine reflection, never fantasy or fairy tale. Use only the user's actual themes, metaphors, and vocabulary. Structure the output as valid JSON: { "title": "A deep, emotional, authentic title", "text": "A concise but emotionally rich story (max 2 paragraphs), focusing on inner growth, insight, and self-reflection. Make it meaningful for the reader." } Write both title and text in the following language: ${detectedLang}.`
    };

    const completion = await openai.chat.completions.create({
      model: 'gpt-4',
      messages: [
        promptObj,
        ...conversation,
      ],
      max_tokens: 1500,
    });

    const raw = completion.choices[0].message.content;
    console.log("generateFullStory raw output:", raw);

    // Logi OpenAI vastus Firestore'sse debugimiseks
    await storyRef.update({ gptRawStory: raw });

    let result = { title: "Untitled", text: "" };
    try {
      result = JSON.parse(raw);
      if (!result.title || !result.text) throw new Error("Missing fields");
    } catch (err) {
      console.error("Failed to parse story completion", raw);
      // Fallback: proovi regexiga leida pealkiri ja tekst
      const match = raw.match(/\{\s*"?title"?\s*:\s*"([^"]+)"\s*,\s*"?text"?\s*:\s*"([\s\S]+)"\s*\}/i);
      if (match) {
        result.title = match[1];
        result.text = match[2];
      } else {
        // Fallback: proovi "Title: ...\nText: ..." formaati
        const titleMatch = raw.match(/title\s*[:\-]\s*(.+)/i);
        const textMatch = raw.match(/text\s*[:\-]\s*([\s\S]+)/i);
        if (titleMatch && textMatch) {
          result.title = titleMatch[1].trim();
          result.text = textMatch[1].trim();
        } else {
          // Kui ikka ei õnnestu, salvesta kogu tekst story'ks
          result.text = raw;
        }
      }
    }

    await storyRef.update({
      gptGeneratedTitle: result.title,
      gptGeneratedText: result.text,
    });

    return { success: true };
  } catch (error) {
    console.error("generateFullStory error:", error);
    throw new functions.https.HttpsError('internal', error.message);
  }
});