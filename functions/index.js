const functions = require('firebase-functions');
const admin = require('firebase-admin');
const { GoogleGenerativeAI } = require('@google/generative-ai');

// Initialize admin if not already initialized
if (!admin.apps.length) {
    admin.initializeApp();
}
const db = admin.firestore();

// --- API Key for Google Gemini AI ---
const API_KEY = "AIzaSyD-V5YcHFaQ7oqsKFFLt8Gg-rTf3IRW24U"; 

const genAI = new GoogleGenerativeAI(API_KEY);
const model = genAI.getGenerativeModel({ model: "gemini-1.5-flash" });

const systemPrompt = `Ти си "Коди" - експертен бот-асистент по програмиране за начинаещи.
Целта ти е да помагаш с HTML, CSS, JavaScript и Python.
Винаги отговаряй на български език.
Бъди кратък, ясен и давай примери.
Ако те попитат кой те е създал, кажи че си проект на Камелия.

ВАЖНО: Ти имаш способността да учиш и помниш всичко от предишни разговори.
Използвай информацията от минали взаимодействия, за да даваш по-персонализирани и контекстуални отговори.
Всеки път, когато научиш нещо ново, го запомни и го използвай в бъдещи разговори.`;

exports.callKodyAPI = functions.https.onCall(async (data, context) => {
    // Проверка за сигурност (активирай за продукция)
    // if (!context.auth) {
    //    throw new functions.https.HttpsError('unauthenticated', 'Моля, влезте в системата.');
    // }
    
    const history = data.chatHistory || [];
    const userParts = data.userParts || [];
    const userId = data.userId || 'anonymous';
    const sessionId = data.sessionId || `session_${Date.now()}`;
    
    // Адаптация на формата за Gemini
    let partsForGemini = userParts;
    if (userParts.length > 0 && typeof userParts[0] === 'string') {
        partsForGemini = [{ text: userParts[0] }];
    }

    // Retrieve past learning context for this user
    let learningContext = '';
    try {
        const userLearningDoc = await db.collection('user_learning').doc(userId).get();
        if (userLearningDoc.exists) {
            const learningData = userLearningDoc.data();
            const recentTopics = learningData.topics || [];
            const preferences = learningData.preferences || {};
            
            if (recentTopics.length > 0) {
                learningContext = `\n\nКонтекст от предишни разговори: ${recentTopics.slice(-5).join(', ')}`;
            }
            if (Object.keys(preferences).length > 0) {
                learningContext += `\nПредпочитания: ${JSON.stringify(preferences)}`;
            }
        }
    } catch (error) {
        console.error("Error retrieving learning context:", error);
    }

    // Enhanced system prompt with learning context
    const enhancedSystemPrompt = systemPrompt + learningContext;

    history.push({ role: "user", parts: partsForGemini });

    try {
        const result = await model.generateContent({
            contents: history,
            systemInstruction: { parts: [{ text: enhancedSystemPrompt }] }
        });
        
        const response = await result.response;
        const text = response.text();
        
        // Save conversation to database for learning
        const conversationData = {
            userId: userId,
            sessionId: sessionId,
            timestamp: admin.firestore.FieldValue.serverTimestamp(),
            userMessage: userParts[0]?.text || userParts[0] || '',
            aiResponse: text,
            chatHistory: history
        };
        
        await db.collection('conversations').add(conversationData);
        
        // Extract and save learning topics
        await extractAndSaveLearning(userId, userParts[0]?.text || userParts[0] || '', text);
        
        return { text: text };

    } catch (error) {
        console.error("Error calling Gemini:", error);
        throw new functions.https.HttpsError('internal', 'Грешка в AI модела: ' + error.message);
    }
});

// Function to extract and save learning from conversations
async function extractAndSaveLearning(userId, userMessage, aiResponse) {
    try {
        // Extract topics from the conversation
        const topics = extractTopics(userMessage + ' ' + aiResponse);
        
        // Update or create user learning profile
        const userLearningRef = db.collection('user_learning').doc(userId);
        const userLearningDoc = await userLearningRef.get();
        
        if (userLearningDoc.exists) {
            const currentData = userLearningDoc.data();
            const currentTopics = currentData.topics || [];
            const updatedTopics = [...new Set([...currentTopics, ...topics])];
            
            await userLearningRef.update({
                topics: updatedTopics.slice(-50), // Keep last 50 topics
                lastInteraction: admin.firestore.FieldValue.serverTimestamp(),
                interactionCount: admin.firestore.FieldValue.increment(1)
            });
        } else {
            await userLearningRef.set({
                topics: topics,
                preferences: {},
                firstInteraction: admin.firestore.FieldValue.serverTimestamp(),
                lastInteraction: admin.firestore.FieldValue.serverTimestamp(),
                interactionCount: 1
            });
        }
    } catch (error) {
        console.error("Error saving learning:", error);
    }
}

// Simple topic extraction function
function extractTopics(text) {
    const keywords = [
        'HTML', 'CSS', 'JavaScript', 'Python', 'функция', 'клас', 'променлива',
        'масив', 'обект', 'цикъл', 'условие', 'if', 'for', 'while', 'function',
        'class', 'array', 'loop', 'variable', 'Firebase', 'база данни', 'API'
    ];
    
    const topics = [];
    const lowerText = text.toLowerCase();
    
    keywords.forEach(keyword => {
        if (lowerText.includes(keyword.toLowerCase())) {
            topics.push(keyword);
        }
    });
    
    return [...new Set(topics)]; // Remove duplicates
}

// --- Existing Functions ---

// --- Функция 1: Самодиагностика ---
exports.systemHealth = functions.https.onRequest(async (request, response) => {
    let healthStatus = 'OK';
    const checks = {};
    checks.server = {status: 'PASSED', message: 'Cloud Function работи.'};
    
    try {
        await db.collection('system_checks').doc('health_test').get();
        checks.database = {status: 'PASSED', message: 'Firestore е достъпен.'};
    } catch (error) {
        checks.database = {status: 'FAILED', message: `Грешка: ${error.message}`};
        healthStatus = 'ERROR';
    }
    response.json({ status: healthStatus, checks: checks });
});

// --- Функция 2: Поздрав ---
exports.greetUserDB = functions.https.onRequest(async (request, response) => {
  const userName = request.query.name;
  let greetingMessage;
  
  if (userName) {
    const userRef = db.collection('users').doc(userName);
    const doc = await userRef.get();
    
    if (doc.exists) {
      greetingMessage = `Здравей отново, ${userName}! Радвам се да те видя пак.`;
    } else {
      await userRef.set({ firstVisit: new Date() });
      greetingMessage = `Здравей, ${userName}! Вече си записан в базата.`;
    }
  } else {
    greetingMessage = "Здравей! Как се казваш?";
  }
  
  response.send(greetingMessage);
});

// --- New Function: Get User Learning Stats ---
exports.getUserLearningStats = functions.https.onCall(async (data, context) => {
    const userId = data.userId || 'anonymous';
    
    try {
        const userLearningDoc = await db.collection('user_learning').doc(userId).get();
        
        if (userLearningDoc.exists) {
            return userLearningDoc.data();
        } else {
            return {
                message: 'Все още няма данни за обучение за този потребител.',
                topics: [],
                interactionCount: 0
            };
        }
    } catch (error) {
        console.error("Error getting learning stats:", error);
        throw new functions.https.HttpsError('internal', 'Грешка при извличане на статистика: ' + error.message);
    }
});

// --- New Function: Get Conversation History ---
exports.getConversationHistory = functions.https.onCall(async (data, context) => {
    const userId = data.userId || 'anonymous';
    const limit = data.limit || 10;
    
    try {
        const conversationsSnapshot = await db.collection('conversations')
            .where('userId', '==', userId)
            .orderBy('timestamp', 'desc')
            .limit(limit)
            .get();
        
        const conversations = [];
        conversationsSnapshot.forEach(doc => {
            conversations.push({
                id: doc.id,
                ...doc.data()
            });
        });
        
        return { conversations: conversations };
    } catch (error) {
        console.error("Error getting conversation history:", error);
        throw new functions.https.HttpsError('internal', 'Грешка при извличане на история: ' + error.message);
    }
});