import os


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "ai-gym-fitness-secret-key-2024"
    DATABASE = "ai_gym_fitness.db"
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    DB_PATH = os.path.join(BASE_DIR, DATABASE)

    CAMERA_INDEX = 0
    VIDEO_WIDTH = 640
    VIDEO_HEIGHT = 480

    SITECONFIG = {
        "site_name": "AI Gym & Fitness Assistant",
        "version": "1.0.0",
        "author": "Trivion",
    }
