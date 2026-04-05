from datetime import datetime, timedelta
from database import get_db_connection
from .habit import get_streak, get_weekly_summary


def calculate_score(habit_data=None):
    if habit_data is None:
        habit_data = get_weekly_summary()

    streak = get_streak()
    workout_rate = habit_data.get("completion_rate", 0)

    streak_score = min(streak * 5, 25)
    consistency_score = workout_rate * 0.5
    engagement_score = 25

    total_score = min(streak_score + consistency_score + engagement_score, 100)

    return int(total_score)


def get_weekly_report():
    summary = get_weekly_summary()
    score = calculate_score(summary)

    days = summary["days"]
    workouts = summary["total_workouts"]

    if workouts >= 5:
        status = "Excellent"
        message = "You're crushing it! Keep up the amazing work!"
    elif workouts >= 3:
        status = "Good"
        message = "Good progress! Try to add 1-2 more workouts this week."
    elif workouts >= 1:
        status = "Needs Improvement"
        message = "Let's get moving! Aim for at least 3 workouts per week."
    else:
        status = "Get Started"
        message = (
            "Every journey starts with a single step. Log your first workout today!"
        )

    trend = get_trend()

    return {
        "score": score,
        "status": status,
        "message": message,
        "workouts_this_week": workouts,
        "completion_rate": summary["completion_rate"],
        "trend": trend,
        "daily_scores": generate_daily_scores(days),
        "recommendations": get_recommendations(score, trend),
    }


def get_trend():
    conn = get_db_connection()
    cursor = conn.cursor()

    weeks = []
    for i in range(4):
        week_start = (datetime.now() - timedelta(days=7 * (i + 1))).strftime("%Y-%m-%d")
        week_end = (datetime.now() - timedelta(days=7 * i + 1)).strftime("%Y-%m-%d")

        cursor.execute(
            """
            SELECT COUNT(*) as count FROM habit_logs 
            WHERE date BETWEEN ? AND ? AND workout_done = 1
        """,
            (week_start, week_end),
        )
        result = cursor.fetchone()
        weeks.append(result["count"] if result else 0)

    conn.close()

    weeks.reverse()

    if len(weeks) >= 2:
        if weeks[-1] > weeks[-2]:
            return "improving"
        elif weeks[-1] < weeks[-2]:
            return "declining"
        else:
            return "stable"

    return "stable"


def generate_daily_scores(days):
    scores = []
    for day in days:
        if day["workout"]:
            base = 70
            if day["mood"] == "positive":
                base += 15
            elif day["mood"] == "negative":
                base += 5
            scores.append(min(base, 100))
        else:
            scores.append(0)
    return scores


def get_recommendations(score, trend):
    recs = []

    if score < 40:
        recs.append("Start with short 15-minute workouts and build up gradually.")
        recs.append("Focus on activities you enjoy to build the habit.")
    elif score < 70:
        recs.append("You're making progress! Try to increase workout intensity.")
        recs.append("Don't forget to track your meals for better results.")
    else:
        recs.append("Excellent performance! Consider trying new workout styles.")
        recs.append("You could help motivate others in the community!")

    if trend == "declining":
        recs.append("Your activity has dropped recently. Set a reminder to workout!")
    elif trend == "stable":
        recs.append("Consistent work! Try increasing duration for more gains.")

    return recs


def update_daily_stats(reps=0, calories=0, duration=0):
    today = datetime.now().strftime("%Y-%m-%d")

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO user_stats (stat_date, reps_completed, calories_burned, workout_duration, performance_score)
        VALUES (?, ?, ?, ?, ?)
        ON CONFLICT(stat_date) DO UPDATE SET
            reps_completed = reps_completed + excluded.reps_completed,
            calories_burned = calories_burned + excluded.calories_burned,
            workout_duration = workout_duration + excluded.workout_duration
    """,
        (today, reps, calories, duration, calculate_score()),
    )

    conn.commit()
    conn.close()

    return {"status": "success", "date": today}
