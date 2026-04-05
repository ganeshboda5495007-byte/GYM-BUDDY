# AI Gym & Fitness - Frontend Developer Guide

## API Base URL
```
http://localhost:5000/api
```

---

## 📡 API ENDPOINTS

### 1. Dashboard
```
GET /api/dashboard
```
**Response:**
```json
{
  "streak": 5,
  "score": 75,
  "weekly": {
    "total_workouts": 3,
    "completion_rate": 42.8,
    "days": [
      {"date": "2026-03-17", "day": "Mon", "workout": true, "mood": "positive"},
      ...
    ]
  },
  "today": {
    "checked_in": true,
    "workout_done": true,
    "mood": "positive"
  }
}
```

---

### 2. Diet / BMI Calculator
```
POST /api/diet
```
**Request Body:**
```json
{
  "height": 170,
  "weight": 70,
  "goal": "maintain"  // "maintain" | "lose" | "gain"
}
```
**Response:**
```json
{
  "bmi": 24.2,
  "category": "Normal",
  "category_color": "success",
  "description": "You have a healthy weight...",
  "recommended_calories": 2545,
  "plan": {
    "name": "Balanced Maintenance Diet",
    "calories": 2200,
    "meals": {
      "breakfast": "Greek yogurt parfait...",
      "lunch": "Grilled chicken salad...",
      "snack": "Apple with almond butter",
      "dinner": "Baked salmon, roasted vegetables...",
      "before_bed": "Small handful of walnuts"
    },
    "tips": ["Maintain current weight", "Balanced macronutrients", "Stay active"]
  }
}
```

---

### 3. Chatbot
```
POST /api/chat
```
**Request Body:**
```json
{
  "message": "Give me workout motivation"
}
```
**Response:**
```json
{
  "response": "You are stronger than you think! Every rep counts...",
  "intent": "motivation"
}
```

---

### 4. Habit Tracker

#### Get Stats
```
GET /api/habit/stats
```
**Response:**
```json
{
  "streak": 5,
  "longest": 10,
  "weekly": {
    "total_workouts": 3,
    "completion_rate": 42.8,
    "days": [...]
  }
}
```

#### Check-in
```
POST /api/habit/checkin
```
**Request Body:**
```json
{
  "completed": true,
  "mood": "positive",  // "positive" | "neutral" | "negative"
  "notes": "Great workout today!"
}
```
**Response:**
```json
{
  "status": "success",
  "streak": 6,
  "message": "Great job! Your streak is now 6 days!"
}
```

---

### 5. Performance
```
GET /api/performance
```
**Response:**
```json
{
  "score": 75,
  "status": "Good",
  "message": "You're making progress!",
  "workouts_this_week": 3,
  "completion_rate": 42.8,
  "trend": "improving",  // "improving" | "stable" | "declining"
  "daily_scores": [0, 0, 85, 0, 0, 0, 70],
  "recommendations": [
    "Start with short 15-minute workouts...",
    "Focus on activities you enjoy..."
  ]
}
```

---

### 6. Gym Recommender

#### Get All Gyms
```
GET /api/gym
Query params: ?location=Downtown&price=$$&amenities=yoga
```

**Response:**
```json
{
  "gyms": [
    {
      "id": 1,
      "name": "FitZone Pro",
      "location": "Downtown",
      "address": "123 Main Street, Downtown",
      "amenities": ["pool", "sauna", "yoga", "spinning"],
      "price_range": "$$",
      "price_monthly": 49.99,
      "rating": 4.5,
      "hours": "6:00 AM - 10:00 PM",
      "phone": "+1 (555) 123-4567",
      "image": "https://...",
      "features": ["Personal Training", "Group Classes"]
    }
  ]
}
```

#### Get Locations
```
GET /api/gym/locations
```
**Response:** `["Downtown", "Midtown", "Uptown", "West Side", "East Side"]`

#### Get Amenities
```
GET /api/gym/amenities
```
**Response:** `["pool", "sauna", "yoga", "spinning", "weights", "cardio", ...]`

---

### 7. Smart Gym

#### Dashboard
```
GET /api/smartgym/dashboard
```
**Response:**
```json
{
  "total_equipment": 5,
  "available": 2,
  "in_use": 3,
  "maintenance": 0,
  "equipment": [
    {
      "equipment_id": "treadmill",
      "name": "Smart Treadmill Pro",
      "status": "available",
      "usage_hours": 376,
      "last_maintenance": "2026-03-24",
      "current_settings": {"speed": 5.5, "incline": 0.2},
      "smart_features": ["Auto-adjust speed", "Heart rate monitoring"],
      "suggestions": ["Try interval training...", "For weight loss..."]
    }
  ]
}
```

#### Get Equipment Status
```
GET /api/smartgym/status?equipment_id=treadmill
```

#### Smart Adjust
```
POST /api/smartgym/adjust
```
**Request Body:**
```json
{
  "equipment_id": "treadmill"
}
```
**Response:**
```json
{
  "equipment_id": "treadmill",
  "adjustments": {"speed": 6.5, "speed_change": "+1.0"},
  "reason": "Optimizing for calorie burn",
  "estimated_benefit": "+15% efficiency"
}
```

---

### 8. AI Trainer

#### Get Stats
```
GET /api/trainer/stats
```
**Response:**
```json
{
  "rep_count": 15,
  "exercise": "squat",
  "calories_burned": 7.5,
  "form_feedback": ["Keep your chest up!", "Good form!"]
}
```

#### Set Exercise
```
POST /api/trainer/exercise
```
**Request Body:**
```json
{
  "exercise": "squat"  // "squat" | "pushup"
}
```

#### Reset
```
POST /api/trainer/reset
```

#### Video Feed
```
GET /video_feed
```
Returns MJPEG stream for camera feed.

---

### 9. Settings
```
GET /api/settings
POST /api/settings
```
**Request Body:**
```json
{
  "username": "John",
  "height": 170,
  "weight": 70,
  "age": 25,
  "activity_level": "moderate",
  "theme": "light",
  "notifications": true,
  "units": "metric"
}
```

---

## 🎨 PAGES REQUIRED

### 1. Dashboard (`/`)
- Welcome message
- Stats cards: Score, Streak, Weekly Workouts
- Quick navigation to all modules
- Today's check-in status

### 2. Diet Page (`/diet`)
- Height/Weight input form
- Goal selector (maintain/lose/gain)
- BMI result display
- Diet plan with meals
- Calorie recommendations

### 3. AI Trainer Page (`/trainer`)
- Video feed area
- Exercise selector (squat/pushup)
- Start/Reset buttons
- Rep counter display
- Form feedback
- Calorie burned counter

### 4. Chat Page (`/chat`)
- Chat message history
- Input field + Send button
- Quick reply buttons
- Typing indicator

### 5. Habit Tracker Page (`/habit`)
- Current streak display
- Longest streak
- Weekly calendar view
- Check-in button
- Mood selector
- Success message

### 6. Performance Page (`/performance`)
- Score circle (0-100)
- Trend indicator
- Weekly bar chart
- Recommendations list

### 7. Gym Finder Page (`/gym`)
- Filter form (location, price, amenities)
- Gym cards grid
- Gym details (rating, hours, features)

### 8. Smart Gym Page (`/smartgym`)
- Equipment status cards
- Dashboard stats
- Smart adjust buttons
- Recommendations

### 9. Settings Page (`/settings`)
- User profile form
- Unit preferences (metric/imperial)
- Theme toggle
- Notification settings

---

## 📁 COMPONENT STRUCTURE

```
src/
├── components/
│   ├── layout/
│   │   ├── Navbar.jsx
│   │   ├── Sidebar.jsx
│   │   └── Footer.jsx
│   ├── common/
│   │   ├── Button.jsx
│   │   ├── Card.jsx
│   │   ├── Input.jsx
│   │   ├── Modal.jsx
│   │   └── Loading.jsx
│   ├── dashboard/
│   │   ├── StatCard.jsx
│   │   └── QuickAccess.jsx
│   ├── diet/
│   │   ├── DietForm.jsx
│   │   ├── BMIResult.jsx
│   │   └── MealPlan.jsx
│   ├── trainer/
│   │   ├── CameraFeed.jsx
│   │   ├── RepCounter.jsx
│   │   └── FormFeedback.jsx
│   ├── chat/
│   │   ├── ChatMessage.jsx
│   │   ├── ChatInput.jsx
│   │   └── QuickReplies.jsx
│   ├── habit/
│   │   ├── StreakDisplay.jsx
│   │   ├── WeekCalendar.jsx
│   │   └── MoodSelector.jsx
│   ├── performance/
│   │   ├── ScoreCircle.jsx
│   │   ├── WeeklyChart.jsx
│   │   └── Recommendations.jsx
│   ├── gym/
│   │   ├── GymFilter.jsx
│   │   └── GymCard.jsx
│   ├── smartgym/
│   │   ├── EquipmentCard.jsx
│   │   └── SmartAdjust.jsx
│   └── settings/
│       └── SettingsForm.jsx
├── pages/
│   ├── Dashboard.jsx
│   ├── Diet.jsx
│   ├── Trainer.jsx
│   ├── Chat.jsx
│   ├── Habit.jsx
│   ├── Performance.jsx
│   ├── Gym.jsx
│   ├── SmartGym.jsx
│   └── Settings.jsx
├── hooks/
│   └── useApi.js
├── context/
│   └── AppContext.jsx
├── services/
│   └── api.js
└── utils/
    └── helpers.js
```

---

## 🎯 DESIGN GUIDELINES

### Color Palette
- Primary: `#667eea` (Purple-Blue gradient)
- Secondary: `#764ba2`
- Success: `#198754`
- Warning: `#ffc107`
- Danger: `#dc3545`
- Info: `#0dcaf0`
- Dark: `#343a40`

### Typography
- Font Family: System fonts (Inter, Roboto)
- Headings: 600-800 weight
- Body: 400-500 weight

### Spacing
- Base: 1rem (16px)
- Card padding: 1.5rem
- Section gaps: 2rem

### Components
- Border radius: 1rem (16px)
- Shadows: Subtle, layered
- Animations: Smooth transitions
