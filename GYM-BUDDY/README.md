# AI Gym & Fitness Assistant

An intelligent fitness management system powered by Artificial Intelligence, integrating workout detection, diet planning, behavior tracking, IoT-based smart gym assistance, and conversational AI.

## Features

### 1. AI Gym Trainer
- Real-time pose detection using MediaPipe
- Automatic rep counting (squats, pushups)
- Form correction feedback
- Calorie tracking

### 2. AI Dietician & Calorie Coach
- BMI calculation
- Personalized diet plans based on weight goals
- Meal suggestions with calorie breakdowns
- Nutritional tips

### 3. Smart Gym Assistant
- Equipment status monitoring
- AI-powered recommendations
- Smart adjustment suggestions
- Usage tracking

### 4. Habit Tracker
- Daily workout logging
- Streak tracking
- Mood tracking
- Weekly activity summaries

### 5. Virtual Gym Buddy (Chatbot)
- Rule-based conversational AI
- Motivation and encouragement
- Workout and diet advice
- Fitness FAQ

### 6. Performance Analyzer
- Performance scoring (0-100)
- Weekly progress reports
- Trend analysis
- Personalized recommendations

### 7. Gym Recommender
- Filter by location, price, amenities
- Gym ratings and reviews
- Contact information

## Tech Stack

| Component | Technology |
|-----------|------------|
| Backend | Flask 3.0+ |
| AI/ML | MediaPipe, OpenCV |
| Database | SQLite |
| Frontend | Jinja2 Templates + Bootstrap 5 |
| Language | Python 3.10+ |

## Installation

### Prerequisites
- Python 3.10 or higher
- pip (Python package manager)
- Webcam (for AI Trainer)

### Steps

1. **Clone or navigate to the project directory:**
```bash
cd AI_Gym_Fitness
```

2. **Create a virtual environment (recommended):**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Initialize the database:**
```bash
python database.py
```

5. **Run the application:**
```bash
python app.py
```

6. **Open your browser:**
Navigate to `http://localhost:5000`

## Project Structure

```
AI_Gym_Fitness/
├── app.py                 # Main Flask application
├── config.py             # Configuration settings
├── database.py           # SQLite database setup
├── requirements.txt      # Python dependencies
├── modules/              # Backend modules
│   ├── diet.py          # BMI & diet logic
│   ├── chatbot.py        # Rule-based chatbot
│   ├── habit.py         # Habit tracking
│   ├── performance.py   # Performance scoring
│   ├── gym.py           # Gym recommendations
│   ├── smartgym.py      # Smart gym simulation
│   └── workout.py       # AI Trainer (pose detection)
├── templates/            # HTML templates
│   ├── base.html        # Base template
│   ├── index.html       # Dashboard
│   ├── diet.html        # Diet page
│   ├── trainer.html      # AI Trainer page
│   ├── chat.html        # Chatbot page
│   ├── habit.html       # Habit tracker
│   ├── performance.html # Performance page
│   ├── gym.html         # Gym finder
│   └── smartgym.html    # Smart gym page
├── static/
│   ├── css/
│   │   └── style.css    # Custom styles
│   └── js/
│       └── main.js       # Frontend JavaScript
└── data/
    └── gym_data.json     # Gym database
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/diet` | Get BMI and diet plan |
| POST | `/api/chat` | Get chatbot response |
| POST | `/api/habit/checkin` | Log daily workout |
| GET | `/api/habit/stats` | Get habit statistics |
| GET | `/api/performance` | Get performance report |
| GET | `/api/gym` | Get gym list (with filters) |
| GET | `/api/smartgym/status` | Get equipment status |
| POST | `/api/smartgym/adjust` | Get smart adjustments |
| GET | `/api/trainer/stats` | Get workout stats |
| POST | `/api/trainer/exercise` | Set exercise type |

## Usage Guide

### Dashboard
The main dashboard provides an overview of all modules with quick access links.

### AI Trainer
1. Navigate to the Trainer page
2. Grant camera permissions
3. Select exercise type (Squats/Pushups)
4. Click "Start Workout" to begin
5. The AI will detect your pose and count reps

### Dietician
1. Enter your height and weight
2. Select your goal (maintain/lose/gain)
3. Click "Get Personalized Diet Plan"
4. View your BMI and meal recommendations

### Habit Tracker
1. Log your daily workout
2. Select your mood
3. View your streak and weekly progress

### Chatbot
Type any fitness-related message to get AI-powered responses and motivation.

## Future Enhancements

- [ ] User authentication system
- [ ] Real IoT integration with MQTT
- [ ] Advanced chatbot with OpenAI/Hugging Face
- [ ] React frontend migration
- [ ] Cloud storage for data
- [ ] Mobile app (React Native)
- [ ] Push notifications
- [ ] Social features

## License

This project is for educational purposes. Created as part of Trivion AI Fitness Project.

## Author

Trivion Team

## Acknowledgments

- MediaPipe for pose detection
- Bootstrap for responsive UI
- Flask for the backend framework
