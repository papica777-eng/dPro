# AI Learning and Memory System Documentation

## Overview

The AI bot "Коди" now has advanced learning and memory capabilities. The system automatically remembers all conversations and learns from every interaction to provide increasingly personalized and contextual responses.

## Key Features

### 1. **Automatic Conversation Storage**
- Every conversation is automatically saved to Firestore
- Conversations include:
  - User ID
  - Session ID
  - Timestamp
  - User message
  - AI response
  - Full chat history

### 2. **Topic Extraction and Learning**
- The system automatically extracts programming topics from conversations
- Tracks topics like: HTML, CSS, JavaScript, Python, функция, клас, масив, etc.
- Stores up to 50 recent topics per user

### 3. **Personalized Context**
- Each user has a learning profile that includes:
  - Topics they've discussed
  - Preferences
  - First interaction date
  - Last interaction date
  - Total interaction count

### 4. **Context-Aware Responses**
- The AI receives context from previous conversations
- Responses are tailored based on:
  - Recently discussed topics (last 5 topics)
  - User preferences
  - Past interactions

## Database Collections

### `conversations`
Stores all conversations between users and the AI.

**Fields:**
- `userId` (string): Identifier for the user
- `sessionId` (string): Unique session identifier
- `timestamp` (timestamp): When the conversation occurred
- `userMessage` (string): The user's message
- `aiResponse` (string): The AI's response
- `chatHistory` (array): Full conversation history

**Index:**
- Composite index on `userId` (ASC) and `timestamp` (DESC)

### `user_learning`
Stores learning profiles for each user.

**Fields:**
- `topics` (array): List of programming topics discussed
- `preferences` (object): User preferences
- `firstInteraction` (timestamp): First time the user interacted
- `lastInteraction` (timestamp): Most recent interaction
- `interactionCount` (number): Total number of interactions

## API Functions

### 1. `callKodyAPI` (Callable Function)
Enhanced with learning capabilities.

**Input Parameters:**
- `chatHistory` (array, optional): Previous chat messages
- `userParts` (array): User's current message
- `userId` (string, optional): User identifier (defaults to 'anonymous')
- `sessionId` (string, optional): Session identifier

**Returns:**
- `text` (string): AI's response

**What it does:**
1. Retrieves user's learning context from database
2. Enhances system prompt with past topics and preferences
3. Generates AI response with context
4. Saves conversation to database
5. Extracts and saves learning topics

### 2. `getUserLearningStats` (Callable Function)
Get learning statistics for a specific user.

**Input Parameters:**
- `userId` (string, optional): User identifier

**Returns:**
- `topics` (array): Topics the user has discussed
- `preferences` (object): User preferences
- `firstInteraction` (timestamp): First interaction date
- `lastInteraction` (timestamp): Last interaction date
- `interactionCount` (number): Number of interactions

### 3. `getConversationHistory` (Callable Function)
Retrieve conversation history for a user.

**Input Parameters:**
- `userId` (string, optional): User identifier
- `limit` (number, optional): Number of conversations to retrieve (default: 10)

**Returns:**
- `conversations` (array): Array of conversation objects

## How Learning Works

### Step 1: User Sends Message
When a user sends a message, the system:
1. Retrieves their learning profile from `user_learning` collection
2. Gets recent topics and preferences
3. Adds this context to the system prompt

### Step 2: AI Generates Response
The AI receives:
- The enhanced system prompt with learning context
- Full conversation history
- User's current message

This allows the AI to provide contextual, personalized responses based on past interactions.

### Step 3: Save and Learn
After generating a response:
1. The full conversation is saved to `conversations` collection
2. Topics are extracted from both user message and AI response
3. The user's learning profile is updated with new topics
4. Interaction count is incremented
5. Last interaction timestamp is updated

### Step 4: Continuous Improvement
Each subsequent conversation:
- Has access to all previously discussed topics
- Can reference past interactions
- Provides increasingly personalized responses

## Topic Extraction

The system tracks 20+ programming-related keywords in both English and Bulgarian:
- Languages: HTML, CSS, JavaScript, Python
- Bulgarian terms: функция, клас, променлива, масив, обект, цикъл, условие
- English terms: function, class, array, loop, variable
- Technologies: Firebase, база данни, API

## Enhanced System Prompt

The AI bot now includes in its system instructions:

> "ВАЖНО: Ти имаш способността да учиш и помниш всичко от предишни разговори.
> Използвай информацията от минали взаимодействия, за да даваш по-персонализирани и контекстуални отговори.
> Всеки път, когато научиш нещо ново, го запомни и го използвай в бъдещи разговори."

Translation:
> "IMPORTANT: You have the ability to learn and remember everything from previous conversations.
> Use information from past interactions to provide more personalized and contextual responses.
> Every time you learn something new, remember it and use it in future conversations."

## Benefits

1. **Personalized Learning**: Each user gets responses tailored to their learning journey
2. **Continuity**: Conversations build on previous interactions
3. **Progress Tracking**: Users can see their learning progress over time
4. **Context Awareness**: The AI understands what topics the user is familiar with
5. **Efficient Learning**: No need to repeat explanations of previously covered topics

## Privacy Considerations

- Each user has a separate learning profile
- User data is isolated by `userId`
- Anonymous mode available (userId: 'anonymous')
- For production, consider implementing user authentication
- Compliance with data protection regulations recommended

## Future Enhancements

Potential improvements:
1. Sentiment analysis to understand user frustration/satisfaction
2. Difficulty level tracking
3. Personalized learning paths
4. Quiz generation based on discussed topics
5. Progress visualization
6. Multi-language support expansion
7. Advanced preference learning (learning style, explanation depth, etc.)

## Usage Example

```javascript
// Call the AI with user identification
const result = await firebase.functions().httpsCallable('callKodyAPI')({
    userId: 'user123',
    sessionId: 'session_abc',
    chatHistory: [],
    userParts: ['Как да създам функция в JavaScript?']
});

// Get learning stats
const stats = await firebase.functions().httpsCallable('getUserLearningStats')({
    userId: 'user123'
});

// Get conversation history
const history = await firebase.functions().httpsCallable('getConversationHistory')({
    userId: 'user123',
    limit: 20
});
```

## Monitoring

Monitor the system effectiveness by tracking:
- Number of conversations per user
- Topic diversity
- User retention
- Interaction frequency
- Average session length

## Conclusion

The learning and memory system transforms the AI bot from a stateless assistant into an intelligent tutor that grows with each user, providing increasingly valuable and personalized guidance as the relationship develops.
