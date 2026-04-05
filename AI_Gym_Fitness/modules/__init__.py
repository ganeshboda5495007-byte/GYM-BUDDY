from .diet import (
    calculate_bmi,
    get_bmi_category,
    get_diet_plan,
    calculate_daily_calories,
)
from .chatbot import get_response, detect_intent
from .habit import (
    log_workout,
    get_streak,
    get_longest_streak,
    get_weekly_summary,
    get_today_status,
)
from .performance import calculate_score, get_weekly_report, get_trend
from .gym import (
    get_all_gyms,
    filter_gyms,
    recommend_gym,
    get_locations,
    get_all_amenities,
)
from .smartgym import (
    get_equipment_status,
    get_recommendations,
    simulate_smart_adjustment,
    get_dashboard_summary,
)
from .settings import get_settings, update_settings, reset_settings

__all__ = [
    "calculate_bmi",
    "get_bmi_category",
    "get_diet_plan",
    "calculate_daily_calories",
    "get_response",
    "detect_intent",
    "log_workout",
    "get_streak",
    "get_longest_streak",
    "get_weekly_summary",
    "get_today_status",
    "calculate_score",
    "get_weekly_report",
    "get_trend",
    "get_all_gyms",
    "filter_gyms",
    "recommend_gym",
    "get_locations",
    "get_all_amenities",
    "get_equipment_status",
    "get_recommendations",
    "simulate_smart_adjustment",
    "get_dashboard_summary",
    "get_settings",
    "update_settings",
    "reset_settings",
]
