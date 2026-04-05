import random
from datetime import datetime

EQUIPMENT_TYPES = {
    "treadmill": {
        "name": "Smart Treadmill Pro",
        "base_settings": {"speed": 5.0, "incline": 0},
        "smart_features": [
            "Auto-adjust speed",
            "Heart rate monitoring",
            "Calorie tracking",
        ],
    },
    "bike": {
        "name": "AI Spinning Bike",
        "base_settings": {"resistance": 5, "cadence": 80},
        "smart_features": ["Auto-resistance", "Virtual routes", "Power tracking"],
    },
    "weights": {
        "name": "Smart Weight Station",
        "base_settings": {"weight": 20, "reps": 10},
        "smart_features": ["Auto-weight adjustment", "Form correction", "Rep counting"],
    },
    "rower": {
        "name": "Connected Rower",
        "base_settings": {"resistance": 4, "strokes": 20},
        "smart_features": ["Stroke analysis", "Power zones", "Recovery tracking"],
    },
    "elliptical": {
        "name": "AI Elliptical Trainer",
        "base_settings": {"resistance": 5, "stride": "auto"},
        "smart_features": [
            "Adaptive resistance",
            "Low-impact mode",
            "Muscle targeting",
        ],
    },
}


def get_equipment_status(equipment_id="treadmill"):
    equipment = EQUIPMENT_TYPES.get(equipment_id, EQUIPMENT_TYPES["treadmill"])

    return {
        "equipment_id": equipment_id,
        "name": equipment["name"],
        "status": random.choice(["available", "in_use", "maintenance"]),
        "usage_hours": random.randint(50, 500),
        "last_maintenance": (
            datetime.now().replace(day=random.randint(1, 28))
        ).strftime("%Y-%m-%d"),
        "current_settings": {
            k: v + random.uniform(-0.5, 0.5) if isinstance(v, (int, float)) else v
            for k, v in equipment["base_settings"].items()
        },
        "smart_features": equipment["smart_features"],
        "suggestions": get_recommendations(equipment_id),
    }


def get_recommendations(equipment_id):
    recommendations = {
        "treadmill": [
            "Try interval training: 1 min sprint, 2 min walk, repeat 10x",
            "For weight loss: Maintain 65% max heart rate for 30+ mins",
            "Add incline (2-5%) to increase intensity without impact",
        ],
        "bike": [
            "Perfect for HIIT: 30 sec max effort, 90 sec recovery",
            "Keep cadence between 80-100 RPM for optimal efficiency",
            "Adjust seat height so leg is slightly bent at bottom",
        ],
        "weights": [
            "Focus on compound movements: squats, deadlifts, bench press",
            "Rest 60-90 seconds between sets for strength",
            "For hypertrophy: 8-12 reps, 3-4 sets per exercise",
        ],
        "rower": [
            "Drive with legs first, then pull with arms",
            "Keep core tight and back straight throughout",
            "Aim for 24-28 strokes per minute for cardio benefits",
        ],
        "elliptical": [
            "Use handlebars for balance, not for support",
            "Pedal backward occasionally to target different muscles",
            "Keep upper body movement natural and relaxed",
        ],
    }

    return recommendations.get(
        equipment_id, ["Maintain proper form", "Stay hydrated", "Listen to your body"]
    )


def simulate_smart_adjustment(equipment_id):
    equipment = EQUIPMENT_TYPES.get(equipment_id, EQUIPMENT_TYPES["treadmill"])
    settings = equipment["base_settings"]

    adjustments = {}

    for key, value in settings.items():
        if isinstance(value, (int, float)):
            change = random.uniform(-2, 2)
            new_value = max(0, value + change)
            adjustments[key] = round(new_value, 1)
            adjustments[f"{key}_change"] = (
                f"+{round(change, 1)}" if change >= 0 else str(round(change, 1))
            )
        else:
            adjustments[key] = value

    return {
        "equipment_id": equipment_id,
        "adjustments": adjustments,
        "reason": random.choice(
            [
                "Optimizing for calorie burn",
                "Adjusting for better cardio zone",
                "Matching your current fitness level",
                "Preventing workout plateau",
            ]
        ),
        "estimated_benefit": f"+{random.randint(5, 20)}% efficiency",
    }


def get_all_equipment():
    return [
        {
            "id": eq_id,
            "name": eq_data["name"],
            "status": get_equipment_status(eq_id)["status"],
        }
        for eq_id, eq_data in EQUIPMENT_TYPES.items()
    ]


def get_dashboard_summary():
    equipment = get_all_equipment()

    return {
        "total_equipment": len(equipment),
        "available": sum(1 for e in equipment if e["status"] == "available"),
        "in_use": sum(1 for e in equipment if e["status"] == "in_use"),
        "maintenance": sum(1 for e in equipment if e["status"] == "maintenance"),
        "equipment": [get_equipment_status(e["id"]) for e in equipment],
    }
