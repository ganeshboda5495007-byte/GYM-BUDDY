import random

INTENTS = {
    "greeting": {
        "patterns": [
            "hello",
            "hi",
            "hey",
            "good morning",
            "good evening",
            "howdy",
            "greetings",
        ],
        "responses": [
            "Hello! Great to see you! Ready for today's workout? 💪",
            "Hey there! How are you feeling today? Let's crush some fitness goals!",
            "Hi! Welcome back! What's on your fitness agenda today?",
            "Good to see you! Are you ready to sweat?",
        ],
    },
    "workout": {
        "patterns": [
            "workout",
            "exercise",
            "training",
            "gym",
            "run",
            "cardio",
            "weights",
        ],
        "responses": [
            "Awesome! What type of workout are you planning? We have cardio, strength, and flexibility options!",
            "Let's get moving! Remember: consistency beats intensity. What's your target for today?",
            "Workout time! I recommend mixing cardio and strength training. What's your preference?",
            "Great choice! Don't forget to warm up before and cool down after your workout!",
        ],
    },
    "motivation": {
        "patterns": [
            "motivate",
            "inspire",
            "encourage",
            "motivation",
            "help",
            "support",
            "motivate me",
        ],
        "responses": [
            "You are stronger than you think! Every rep counts, every step brings you closer! 🔥",
            "Remember: It's not about being the best. It's about being better than you were yesterday!",
            "Success is the sum of small efforts repeated day in and day out. Keep going! 💪",
            "Your body can do it. It's your mind you need to convince. You've got this!",
            "The only bad workout is the one that didn't happen. Get out there and move!",
            "You're doing amazing! Keep pushing yourself every single day! 🌟",
            "Believe in yourself! You've already taken the first step by being here!",
        ],
    },
    "diet": {
        "patterns": [
            "diet",
            "nutrition",
            "food",
            "eat",
            "meal",
            "calories",
            "protein",
            "weight loss",
            "healthy eating",
        ],
        "responses": [
            "For optimal results, focus on protein intake (1.6-2g per kg body weight) and stay hydrated!",
            "Remember: abs are made in the kitchen! What are your nutrition goals?",
            "Eat whole foods, avoid processed stuff, and don't skip breakfast! Need specific diet tips?",
            "Fuel your body right! Proteins, complex carbs, and healthy fats. Need a personalized plan?",
            "Stay hydrated! Aim for at least 2-3 liters of water per day! 💧",
        ],
    },
    "rest": {
        "patterns": [
            "rest",
            "recovery",
            "sleep",
            "tired",
            "sore",
            "muscle",
            "recovery",
        ],
        "responses": [
            "Rest is crucial for muscle growth! Make sure you're sleeping 7-9 hours per night.",
            "Listen to your body. If you're sore, active recovery like stretching or walking helps!",
            "Recovery is where the magic happens! Don't underestimate rest days.",
            "Sleep is your best recovery tool. Aim for 8 hours and watch your performance soar!",
        ],
    },
    "progress": {
        "patterns": [
            "progress",
            "improvement",
            "results",
            "better",
            "tracking",
            "score",
        ],
        "responses": [
            "Tracking your progress is key! Check your performance score on the dashboard!",
            "Consistency over time = amazing results. Keep logging your workouts!",
            "Your streak shows dedication! Keep that fire burning! 🔥",
            "Every workout builds on the last. You're making great progress!",
        ],
    },
    "goodbye": {
        "patterns": ["bye", "goodbye", "see you", "later", "thanks", "thank you"],
        "responses": [
            "Keep pushing! See you next workout! 💪",
            "Remember: the only way to fail is to stop trying. See you soon!",
            "Great chatting with you! Now go crush your goals!",
            "Stay strong! Remember: consistency is key. Talk to you later!",
        ],
    },
    "feeling": {
        "patterns": [
            "feel",
            "feeling",
            "emotion",
            "sad",
            "happy",
            "excited",
            "stressed",
        ],
        "responses": [
            "Your feelings are valid! Exercise is a great way to boost your mood!",
            "I hear you! Sometimes a good workout can turn a bad day around.",
            "Whatever you're feeling, remember: movement is medicine. Let's get you moving!",
            "Emotions are part of the journey. How about some stretching or a walk to feel better?",
        ],
    },
    "question": {
        "patterns": ["how", "what", "why", "when", "can i", "should i", "?"],
        "responses": [
            "That's a great question! Let me help you with that. Try the Diet page for personalized advice!",
            "Interesting thought! For specific guidance, check our Habit Tracker and Performance pages.",
            "I'd love to help! Based on your goals, let me recommend the AI Trainer for workout guidance.",
            "Great thinking! Our modules can give you detailed insights. Which area interests you most?",
        ],
    },
    "weights": {
        "patterns": [
            "weight",
            "lose weight",
            "gain weight",
            "bulk",
            "cut",
            "bodybuilding",
        ],
        "responses": [
            "For weight loss: Create a calorie deficit of 500 calories per day through diet and exercise!",
            "For muscle gain: Aim for a calorie surplus of 250-500 calories with high protein intake!",
            "Remember: sustainable progress takes time. Aim for 0.5-1kg per week for healthy weight changes!",
            "Track your macros: Protein (1.6-2.2g/kg), Carbs (3-5g/kg), Fats (0.5-1g/kg)",
        ],
    },
    "cardio": {
        "patterns": [
            "cardio",
            "running",
            "jogging",
            "cycling",
            "swimming",
            "endurance",
        ],
        "responses": [
            "Great for cardio! Try 30 minutes at moderate intensity, 3-5 times per week!",
            "Mix it up! Alternate between steady-state and HIIT for best results!",
            "Remember: Start slow and gradually increase intensity to avoid injury!",
            "Cardio is essential for heart health and burning calories! Keep it consistent!",
        ],
    },
}


def detect_intent(message):
    message = message.lower()
    for intent, data in INTENTS.items():
        for pattern in data["patterns"]:
            if pattern in message:
                return intent
    return "unknown"


def get_response(message):
    intent = detect_intent(message)

    if intent in INTENTS:
        return random.choice(INTENTS[intent]["responses"])

    default_responses = [
        "I'm here to help with your fitness journey! Try asking about workouts, diet, or motivation! 💪",
        "That's interesting! I can help with fitness advice. What would you like to know?",
        "I'd love to assist! Ask me about exercise, nutrition, or tracking your progress!",
        "Let me help you stay on track! What's your fitness goal for today?",
        "Great question! I'm your AI fitness assistant. Ask me anything about workouts, diet, or motivation!",
    ]

    return random.choice(default_responses)


def get_motivational_response(mood="neutral"):
    positive_moods = [
        "Your energy is amazing! Channel it into your workout!",
        "I can feel your enthusiasm! Let's make it count!",
        "High vibes today! Perfect for a challenging session!",
    ]
    negative_moods = [
        "Even on tough days, showing up is half the battle!",
        "It's okay to have off days. A light workout might help!",
        "Remember: the hard days make you stronger!",
    ]
    neutral_moods = [
        "Ready when you are! Let's do this together!",
        "Every workout is a step forward. Let's go!",
        "Time to sweat! What's your plan for today?",
    ]

    if mood == "positive":
        return random.choice(positive_moods)
    elif mood == "negative":
        return random.choice(negative_moods)
    return random.choice(neutral_moods)
