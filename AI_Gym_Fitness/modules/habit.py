from datetime import datetime, timedelta
from database import get_db_connection


def log_workout(date=None, completed=True, mood="neutral", notes=""):
    if date is None:
        date = datetime.now().strftime("%Y-%m-%d")

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO habit_logs (date, workout_done, mood, notes)
        VALUES (?, ?, ?, ?)
        ON CONFLICT(date) DO UPDATE SET
            workout_done = excluded.workout_done,
            mood = excluded.mood,
            notes = excluded.notes
    """,
        (date, completed, mood, notes),
    )

    conn.commit()
    conn.close()

    return {"status": "success", "date": date, "streak": get_streak()}


def get_streak():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT date, workout_done FROM habit_logs ORDER BY date DESC")
    logs = cursor.fetchall()
    conn.close()

    if not logs:
        return 0

    streak = 0
    today = datetime.now().date()

    for i in range(365):
        check_date = (today - timedelta(days=i)).strftime("%Y-%m-%d")

        found = False
        for log in logs:
            if log["date"] == check_date:
                found = True
                if log["workout_done"]:
                    streak += 1
                else:
                    if i == 0:
                        continue
                    return streak
                break

        if not found and i > 0:
            return streak

    return streak


def get_longest_streak():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT date, workout_done FROM habit_logs ORDER BY date ASC")
    logs = cursor.fetchall()
    conn.close()

    if not logs:
        return 0

    longest = 0
    current = 0
    prev_date = None

    for log in logs:
        if log["workout_done"]:
            if prev_date is None:
                current = 1
            else:
                prev = datetime.strptime(prev_date, "%Y-%m-%d").date()
                curr = datetime.strptime(log["date"], "%Y-%m-%d").date()
                if (curr - prev).days == 1:
                    current += 1
                else:
                    current = 1

            if current > longest:
                longest = current

        prev_date = log["date"]

    return longest


def get_weekly_summary():
    conn = get_db_connection()
    cursor = conn.cursor()

    days = []
    today = datetime.now()

    for i in range(7):
        day = (today - timedelta(days=6 - i)).strftime("%Y-%m-%d")
        day_name = (today - timedelta(days=6 - i)).strftime("%a")

        cursor.execute(
            "SELECT workout_done, mood FROM habit_logs WHERE date = ?", (day,)
        )
        log = cursor.fetchone()

        days.append(
            {
                "date": day,
                "day": day_name,
                "workout": bool(log["workout_done"]) if log else False,
                "mood": log["mood"] if log else None,
            }
        )

    conn.close()

    total_workouts = sum(1 for d in days if d["workout"])

    return {
        "days": days,
        "total_workouts": total_workouts,
        "completion_rate": round(total_workouts / 7 * 100, 1),
    }


def get_today_status():
    today = datetime.now().strftime("%Y-%m-%d")

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM habit_logs WHERE date = ?", (today,))
    log = cursor.fetchone()
    conn.close()

    if log:
        return {
            "checked_in": True,
            "workout_done": bool(log["workout_done"]),
            "mood": log["mood"],
            "notes": log["notes"],
        }

    return {"checked_in": False, "workout_done": False, "mood": None, "notes": None}
