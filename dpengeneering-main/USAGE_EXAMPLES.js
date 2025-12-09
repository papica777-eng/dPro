// Example usage of the Learning and Memory System API

/**
 * Example 1: Sending a message to the AI with user identification
 * The AI will remember this conversation and use it in future interactions
 */
async function exampleSendMessage() {
    // Initialize Firebase (this would be done in your app initialization)
    // firebase.initializeApp(config);
    
    const callKodyAPI = firebase.functions().httpsCallable('callKodyAPI');
    
    try {
        const result = await callKodyAPI({
            userId: 'user123',                    // Unique identifier for the user
            sessionId: 'session_abc',             // Session identifier (optional)
            chatHistory: [],                      // Previous messages in current session
            userParts: ['Как да създам функция в JavaScript?']  // User's message
        });
        
        console.log('AI Response:', result.data.text);
        // The conversation is automatically saved to Firestore!
        
    } catch (error) {
        console.error('Error:', error);
    }
}

/**
 * Example 2: Getting user learning statistics
 * See what topics the user has discussed and how many interactions they've had
 */
async function exampleGetLearningStats() {
    const getUserLearningStats = firebase.functions().httpsCallable('getUserLearningStats');
    
    try {
        const result = await getUserLearningStats({
            userId: 'user123'
        });
        
        console.log('Learning Stats:', result.data);
        // Output example:
        // {
        //   topics: ['JavaScript', 'function', 'HTML', 'CSS'],
        //   preferences: {},
        //   firstInteraction: Timestamp,
        //   lastInteraction: Timestamp,
        //   interactionCount: 15
        // }
        
    } catch (error) {
        console.error('Error:', error);
    }
}

/**
 * Example 3: Getting conversation history
 * Retrieve past conversations for a user
 */
async function exampleGetConversationHistory() {
    const getConversationHistory = firebase.functions().httpsCallable('getConversationHistory');
    
    try {
        const result = await getConversationHistory({
            userId: 'user123',
            limit: 20  // Get last 20 conversations
        });
        
        console.log('Conversation History:', result.data.conversations);
        // Each conversation contains:
        // {
        //   id: 'doc-id',
        //   userId: 'user123',
        //   sessionId: 'session_abc',
        //   timestamp: Timestamp,
        //   userMessage: 'User question',
        //   aiResponse: 'AI answer',
        //   chatHistory: []
        // }
        
    } catch (error) {
        console.error('Error:', error);
    }
}

/**
 * Example 4: Multi-turn conversation with memory
 * The AI remembers context from previous turns
 */
async function exampleMultiTurnConversation() {
    const callKodyAPI = firebase.functions().httpsCallable('callKodyAPI');
    const userId = 'user456';
    let chatHistory = [];
    
    // First message
    const response1 = await callKodyAPI({
        userId: userId,
        chatHistory: chatHistory,
        userParts: ['Покажи ми как да създам променлива в JavaScript']
    });
    
    console.log('Turn 1:', response1.data.text);
    
    // Update chat history
    chatHistory.push(
        { role: "user", parts: [{ text: 'Покажи ми как да създам променлива в JavaScript' }] },
        { role: "model", parts: [{ text: response1.data.text }] }
    );
    
    // Second message - AI remembers the previous context
    const response2 = await callKodyAPI({
        userId: userId,
        chatHistory: chatHistory,
        userParts: ['А как да я използвам в цикъл?']
    });
    
    console.log('Turn 2:', response2.data.text);
    // The AI knows "я" refers to the variable from the previous question!
}

/**
 * Example 5: Display user progress
 * Show the user what they've learned over time
 */
async function exampleDisplayProgress() {
    const getUserLearningStats = firebase.functions().httpsCallable('getUserLearningStats');
    const getConversationHistory = firebase.functions().httpsCallable('getConversationHistory');
    
    const userId = 'user789';
    
    // Get stats
    const stats = await getUserLearningStats({ userId });
    
    // Get recent conversations
    const history = await getConversationHistory({ userId, limit: 5 });
    
    // Display progress dashboard
    console.log('=== Learning Progress Dashboard ===');
    console.log(`Total Interactions: ${stats.data.interactionCount}`);
    console.log(`Topics Mastered: ${stats.data.topics.join(', ')}`);
    console.log(`Member Since: ${stats.data.firstInteraction}`);
    console.log(`Last Active: ${stats.data.lastInteraction}`);
    console.log('\nRecent Conversations:');
    history.data.conversations.forEach((conv, i) => {
        console.log(`${i + 1}. ${conv.userMessage.substring(0, 50)}...`);
    });
}

// HTML Integration Example
const htmlExample = `
<!DOCTYPE html>
<html lang="bg">
<head>
    <meta charset="UTF-8">
    <title>Коди - AI Assistant with Memory</title>
    <script src="https://www.gstatic.com/firebasejs/9.0.0/firebase-app.js"></script>
    <script src="https://www.gstatic.com/firebasejs/9.0.0/firebase-functions.js"></script>
</head>
<body>
    <div id="chat">
        <div id="messages"></div>
        <input type="text" id="userInput" placeholder="Напиши съобщение...">
        <button onclick="sendMessage()">Изпрати</button>
    </div>
    
    <div id="stats">
        <h3>Твоят Прогрес</h3>
        <div id="topicsLearned"></div>
        <div id="interactionCount"></div>
    </div>
    
    <script>
        // Initialize Firebase
        const firebaseConfig = { /* your config */ };
        firebase.initializeApp(firebaseConfig);
        
        const userId = 'user_' + Math.random().toString(36).substr(2, 9);
        let chatHistory = [];
        
        async function sendMessage() {
            const input = document.getElementById('userInput');
            const message = input.value;
            
            const callKodyAPI = firebase.functions().httpsCallable('callKodyAPI');
            
            const result = await callKodyAPI({
                userId: userId,
                chatHistory: chatHistory,
                userParts: [message]
            });
            
            // Display message
            displayMessage('user', message);
            displayMessage('ai', result.data.text);
            
            // Update history
            chatHistory.push(
                { role: "user", parts: [{ text: message }] },
                { role: "model", parts: [{ text: result.data.text }] }
            );
            
            input.value = '';
            
            // Update stats
            updateStats();
        }
        
        async function updateStats() {
            const getUserLearningStats = firebase.functions().httpsCallable('getUserLearningStats');
            const stats = await getUserLearningStats({ userId });
            
            document.getElementById('topicsLearned').innerHTML = 
                'Теми: ' + stats.data.topics.join(', ');
            document.getElementById('interactionCount').innerHTML = 
                'Разговори: ' + stats.data.interactionCount;
        }
        
        function displayMessage(role, text) {
            const messagesDiv = document.getElementById('messages');
            const msgDiv = document.createElement('div');
            msgDiv.className = role;
            msgDiv.textContent = text;
            messagesDiv.appendChild(msgDiv);
        }
    </script>
</body>
</html>
`;

console.log('Example HTML integration:', htmlExample);
