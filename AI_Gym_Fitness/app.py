from flask import (
    Flask,
    render_template,
    request,
    jsonify,
    Response,
    redirect,
    url_for,
    session,
)
from flask_cors import CORS
from flask_login import (
    LoginManager,
    UserMixin,
    login_user,
    login_required,
    logout_user,
    current_user,
)
from database import init_db
from config import Config
from modules import (
    calculate_bmi,
    get_bmi_category,
    get_diet_plan,
    calculate_daily_calories,
    get_response,
    detect_intent,
    log_workout,
    get_streak,
    get_longest_streak,
    get_weekly_summary,
    get_today_status,
    calculate_score,
    get_weekly_report,
    get_trend,
    get_all_gyms,
    filter_gyms,
    recommend_gym,
    get_locations,
    get_all_amenities,
    get_equipment_status,
    get_recommendations,
    simulate_smart_adjustment,
    get_dashboard_summary,
    get_settings,
    update_settings,
    reset_settings,
)
from modules.auth import (
    create_user,
    authenticate_user,
    get_user_by_id,
    update_user_profile,
)

app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = Config.SECRET_KEY
CORS(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


class User(UserMixin):
    def __init__(self, id, username, email, full_name=None):
        self.id = id
        self.username = username
        self.email = email
        self.full_name = full_name


@login_manager.user_loader
def load_user(user_id):
    user = get_user_by_id(int(user_id))
    if user:
        return User(user["id"], user["username"], user["email"], user.get("full_name"))
    return None


init_db()


def api_response(success=True, data=None, message="", error=None):
    response = {"success": success}
    if data is not None:
        response["data"] = data
    if message:
        response["message"] = message
    if error:
        response["error"] = error
    return jsonify(response)


# ============ PAGE ROUTES ============


@app.route("/")
def index():
    if current_user.is_authenticated:
        streak = get_streak()
        score = calculate_score()
        weekly = get_weekly_summary()
        today = get_today_status()
        return render_template(
            "index.html", streak=streak, score=score, weekly=weekly, today=today
        )
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user = authenticate_user(username, password)
        if user:
            user_obj = User(
                user["id"], user["username"], user["email"], user.get("full_name")
            )
            login_user(user_obj)
            return redirect(url_for("index"))

        return render_template("login.html", error="Invalid username or password")

    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        full_name = request.form.get("full_name")
        age = request.form.get("age")
        gender = request.form.get("gender")
        diet_type = request.form.get("diet_type", "non-vegetarian")

        result = create_user(
            username, email, password, full_name, age, gender, diet_type
        )

        if result["success"]:
            return redirect(url_for("login"))
        else:
            return render_template(
                "register.html", error=result.get("error", "Registration failed")
            )

    return render_template("register.html")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))


@app.route("/diet")
def diet_page():
    return render_template("diet.html")


@app.route("/trainer")
def trainer_page():
    return render_template("trainer.html")


@app.route("/chat")
def chat_page():
    return render_template("chat.html")


@app.route("/habit")
def habit_page():
    streak = get_streak()
    longest = get_longest_streak()
    weekly = get_weekly_summary()
    today = get_today_status()
    return render_template(
        "habit.html", streak=streak, longest_streak=longest, weekly=weekly, today=today
    )


@app.route("/performance")
def performance_page():
    report = get_weekly_report()
    return render_template("performance.html", report=report)


@app.route("/gym")
def gym_page():
    locations = get_locations()
    amenities = get_all_amenities()
    gyms = get_all_gyms()
    return render_template(
        "gym.html", gyms=gyms, locations=locations, amenities=amenities
    )


@app.route("/smartgym")
def smartgym_page():
    summary = get_dashboard_summary()
    return render_template("smartgym.html", summary=summary)


@app.route("/settings")
def settings_page():
    settings = get_settings()
    return render_template("settings.html", settings=settings)


# ============ API ROUTES ============


@app.route("/api/dashboard")
def api_dashboard():
    return api_response(
        data={
            "streak": get_streak(),
            "score": calculate_score(),
            "weekly": get_weekly_summary(),
            "today": get_today_status(),
        }
    )


@app.route("/api/diet", methods=["POST"])
def api_diet():
    data = request.get_json()
    height = float(data.get("height", 170))
    weight = float(data.get("weight", 70))
    age = int(data.get("age", 25))
    goal = data.get("goal", "maintain")
    diet_type = data.get("diet_type", "non-vegetarian")

    if height < 10:
        height = height * 100

    bmi = calculate_bmi(height, weight)
    category = get_bmi_category(bmi)
    plan = get_diet_plan(bmi, goal, diet_type)
    calories = calculate_daily_calories(height, weight, age)

    return api_response(
        data={
            "bmi": bmi,
            "category": category["category"],
            "category_color": category["color"],
            "description": category["description"],
            "plan": plan,
            "recommended_calories": calories,
        }
    )


@app.route("/api/chat", methods=["POST"])
def api_chat():
    data = request.get_json()
    message = data.get("message", "")
    response = get_response(message)
    intent = detect_intent(message)
    return api_response(data={"response": response, "intent": intent})


@app.route("/api/habit/stats")
def api_habit_stats():
    return api_response(
        data={
            "streak": get_streak(),
            "longest": get_longest_streak(),
            "weekly": get_weekly_summary(),
        }
    )


@app.route("/api/habit/checkin", methods=["POST"])
def api_habit_checkin():
    data = request.get_json()
    completed = data.get("completed", True)
    mood = data.get("mood", "neutral")
    notes = data.get("notes", "")
    result = log_workout(completed=completed, mood=mood, notes=notes)
    return api_response(
        data={"streak": result["streak"]},
        message=f"Great job! Your streak is now {result['streak']} days!",
    )


@app.route("/api/performance")
def api_performance():
    return api_response(data=get_weekly_report())


@app.route("/api/gym")
def api_gym():
    location = request.args.get("location")
    amenities = request.args.getlist("amenities")
    price = request.args.get("price")
    lat = request.args.get("lat", type=float)
    lon = request.args.get("lon", type=float)
    radius = request.args.get("radius", default=10, type=float)

    if lat and lon:
        gyms = filter_gyms(
            location,
            amenities,
            price if isinstance(price, list) else [price] if price else None,
            lat,
            lon,
            radius,
        )
    elif location or amenities or price:
        gyms = filter_gyms(
            location,
            amenities,
            price if isinstance(price, list) else [price] if price else None,
        )
    else:
        gyms = get_all_gyms()

    return api_response(data={"gyms": gyms})


@app.route("/api/gym/locations")
def api_gym_locations():
    return api_response(data={"locations": get_locations()})


@app.route("/api/gym/amenities")
def api_gym_amenities():
    return api_response(data={"amenities": get_all_amenities()})


@app.route("/api/smartgym/dashboard")
def api_smartgym_dashboard():
    return api_response(data=get_dashboard_summary())


@app.route("/api/smartgym/status")
def api_smartgym_status():
    equipment_id = request.args.get("equipment_id", "treadmill")
    return api_response(data=get_equipment_status(equipment_id))


@app.route("/api/smartgym/adjust", methods=["POST"])
def api_smartgym_adjust():
    data = request.get_json()
    equipment_id = data.get("equipment_id", "treadmill")
    return api_response(data=simulate_smart_adjustment(equipment_id))


@app.route("/api/trainer/start")
def api_trainer_start():
    return api_response(data={"status": "ready", "message": "Camera ready"})


@app.route("/api/trainer/stats")
def api_trainer_stats():
    from modules.workout import detector

    return api_response(data=detector.get_stats())


@app.route("/api/trainer/exercise", methods=["POST"])
def api_trainer_exercise():
    from modules.workout import detector

    data = request.get_json()
    detector.set_exercise(data.get("exercise", "squat"))
    return api_response(data={"exercise": data.get("exercise", "squat")})


@app.route("/api/trainer/reset", methods=["POST"])
def api_trainer_reset():
    from modules.workout import detector

    detector.reset()
    return api_response(message="Workout reset successfully")


@app.route("/video_feed")
def video_feed():
    try:
        import cv2
        from modules.workout import detector

        def generate_frames():
            cap = cv2.VideoCapture(0)
            while True:
                success, frame = cap.read()
                if not success:
                    break
                frame = detector.process_frame(frame)
                stats = detector.get_stats()
                cv2.putText(
                    frame,
                    f"Reps: {stats['rep_count']}",
                    (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 255, 0),
                    2,
                )
                ret, buffer = cv2.imencode(".jpg", frame)
                frame = buffer.tobytes()
                yield (b"--frame\r\nContent-Type: image/jpeg\r\n\r\n" + frame + b"\r\n")
            cap.release()

        return Response(
            generate_frames(), mimetype="multipart/x-mixed-replace; boundary=frame"
        )
    except Exception as e:
        return api_response(success=False, error=str(e)), 500


@app.route("/api/settings")
def api_settings_get():
    return api_response(data=get_settings())


@app.route("/api/settings", methods=["POST"])
def api_settings_update():
    data = request.get_json()
    result = update_settings(data)
    if result:
        return api_response(data=result, message="Settings updated successfully")
    return api_response(success=False, error="Failed to save settings")


@app.route("/api/health")
def api_health():
    return api_response(data={"status": "healthy", "version": "1.0.0"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
