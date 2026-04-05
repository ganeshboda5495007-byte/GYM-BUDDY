import json
import os
import math


def load_gym_data():
    data_path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)), "data", "gym_data.json"
    )
    try:
        with open(data_path, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {"gyms": get_default_gyms()}


def get_default_gyms():
    return [
        {
            "id": 1,
            "name": "FitZone Pro",
            "location": "Downtown",
            "address": "123 Main Street, Downtown",
            "latitude": 13.0827,
            "longitude": 80.2707,
            "amenities": ["pool", "sauna", "yoga", "spinning"],
            "price_range": "$$",
            "price_monthly": 49.99,
            "rating": 4.5,
            "hours": "6:00 AM - 10:00 PM",
            "phone": "+1 (555) 123-4567",
            "image": "https://images.unsplash.com/photo-1534438327276-14e5300c3a48?w=400",
            "features": [
                "Personal Training",
                "Group Classes",
                "Locker Rooms",
                "Parking",
            ],
        },
        {
            "id": 2,
            "name": "Muscle Factory",
            "location": "Midtown",
            "address": "456 Oak Avenue, Midtown",
            "latitude": 13.0850,
            "longitude": 80.2750,
            "amenities": ["weights", "cardio", "boxing"],
            "price_range": "$",
            "price_monthly": 29.99,
            "rating": 4.2,
            "hours": "5:00 AM - 11:00 PM",
            "phone": "+1 (555) 234-5678",
            "image": "https://images.unsplash.com/photo-1571902943202-507ec2618e8f?w=400",
            "features": [
                "Free Weights",
                "Powerlifting Zone",
                "Boxing Ring",
                "24/7 Access",
            ],
        },
        {
            "id": 3,
            "name": "Zen Fitness Studio",
            "location": "Uptown",
            "address": "789 Peace Boulevard, Uptown",
            "latitude": 13.0900,
            "longitude": 80.2800,
            "amenities": ["yoga", "pilates", "meditation", "spa"],
            "price_range": "$$$",
            "price_monthly": 79.99,
            "rating": 4.8,
            "hours": "7:00 AM - 9:00 PM",
            "phone": "+1 (555) 345-6789",
            "image": "https://images.unsplash.com/photo-1540497077202-7c8a3999166f?w=400",
            "features": [
                "Premium Spa",
                "Meditation Room",
                "Nutrition Counseling",
                "Spa Services",
            ],
        },
        {
            "id": 4,
            "name": "CrossFit Elite",
            "location": "West Side",
            "address": "321 Athlete Way, West Side",
            "latitude": 13.0750,
            "longitude": 80.2650,
            "amenities": ["crossfit", "hiit", "weights"],
            "price_range": "$$",
            "price_monthly": 59.99,
            "rating": 4.6,
            "hours": "6:00 AM - 9:00 PM",
            "phone": "+1 (555) 456-7890",
            "image": "https://images.unsplash.com/photo-1517836357463-d25dfeac3438?w=400",
            "features": [
                "CrossFit Boxes",
                "Olympic Lifting",
                "HIIT Classes",
                "Nutrition Plans",
            ],
        },
        {
            "id": 5,
            "name": "Budget Gym",
            "location": "East Side",
            "address": "555 Basic Street, East Side",
            "latitude": 13.0800,
            "longitude": 80.2850,
            "amenities": ["cardio", "weights"],
            "price_range": "$",
            "price_monthly": 19.99,
            "rating": 3.8,
            "hours": "6:00 AM - 10:00 PM",
            "phone": "+1 (555) 567-8901",
            "image": "https://images.unsplash.com/photo-1576678927484-cc907957088c?w=400",
            "features": ["Basic Equipment", "Locker Rental", "Showers"],
        },
        {
            "id": 6,
            "name": "Aqua Sports Center",
            "location": "Downtown",
            "address": "888 Wave Road, Downtown",
            "latitude": 13.0780,
            "longitude": 80.2720,
            "amenities": ["pool", "aquaerobics", "spa", "steam"],
            "price_range": "$$$",
            "price_monthly": 89.99,
            "rating": 4.7,
            "hours": "5:30 AM - 9:30 PM",
            "phone": "+1 (555) 678-9012",
            "image": "https://images.unsplash.com/photo-1575429198097-0414ec08e8cd?w=400",
            "features": ["Olympic Pool", "Aqua Classes", "Steam Room", "Swim Lessons"],
        },
    ]


def haversine_distance(lat1, lon1, lat2, lon2):
    R = 6371
    lat1_rad = math.radians(lat1)
    lat2_rad = math.radians(lat2)
    delta_lat = math.radians(lat2 - lat1)
    delta_lon = math.radians(lon2 - lon1)

    a = (
        math.sin(delta_lat / 2) ** 2
        + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(delta_lon / 2) ** 2
    )
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c


def get_all_gyms():
    data = load_gym_data()
    return data.get("gyms", get_default_gyms())


def get_nearby_gyms(user_lat, user_lon, radius_km=10):
    gyms = get_all_gyms()

    nearby = []
    for gym in gyms:
        distance = haversine_distance(
            user_lat, user_lon, gym.get("latitude", 0), gym.get("longitude", 0)
        )
        if distance <= radius_km:
            nearby.append({**gym, "distance_km": round(distance, 2)})

    nearby.sort(key=lambda x: x["distance_km"])
    return nearby


def filter_gyms(
    location=None,
    amenities=None,
    price_range=None,
    user_lat=None,
    user_lon=None,
    radius_km=10,
):
    gyms = get_all_gyms()

    if user_lat and user_lon:
        filtered = []
        for gym in gyms:
            distance = haversine_distance(
                user_lat, user_lon, gym.get("latitude", 0), gym.get("longitude", 0)
            )
            if distance <= radius_km:
                filtered.append({**gym, "distance_km": round(distance, 2)})
        gyms = filtered

    filtered = gyms

    if location:
        filtered = [g for g in filtered if location.lower() in g["location"].lower()]

    if amenities:
        if isinstance(amenities, str):
            amenities = [amenities]
        filtered = [g for g in filtered if any(a in g["amenities"] for a in amenities)]

    if price_range:
        if isinstance(price_range, str):
            price_range = [price_range]
        filtered = [g for g in filtered if g["price_range"] in price_range]

    if user_lat and user_lon:
        filtered.sort(key=lambda x: x.get("distance_km", 999))

    return filtered


def recommend_gym(user_preferences):
    gyms = get_all_gyms()
    user_lat = user_preferences.get("latitude")
    user_lon = user_preferences.get("longitude")

    scored_gyms = []

    for gym in gyms:
        score = 50

        if user_lat and user_lon:
            distance = haversine_distance(
                user_lat, user_lon, gym.get("latitude", 0), gym.get("longitude", 0)
            )
            if distance < 2:
                score += 30
            elif distance < 5:
                score += 20
            elif distance < 10:
                score += 10

        if (
            user_preferences.get("location")
            and user_preferences["location"].lower() in gym["location"].lower()
        ):
            score += 20

        if user_preferences.get("amenities"):
            if isinstance(user_preferences["amenities"], str):
                prefs = [user_preferences["amenities"]]
            else:
                prefs = user_preferences["amenities"]
            match_count = sum(1 for a in prefs if a in gym["amenities"])
            score += match_count * 10

        if user_preferences.get("price_range") == gym["price_range"]:
            score += 15

        score += gym["rating"] * 2

        if user_lat and user_lon:
            distance = haversine_distance(
                user_lat, user_lon, gym.get("latitude", 0), gym.get("longitude", 0)
            )
            scored_gyms.append(
                {
                    **gym,
                    "match_score": min(score, 100),
                    "distance_km": round(distance, 2),
                }
            )
        else:
            scored_gyms.append({**gym, "match_score": min(score, 100)})

    scored_gyms.sort(key=lambda x: x["match_score"], reverse=True)

    return scored_gyms[:5]


def get_locations():
    gyms = get_all_gyms()
    return list(set(g["location"] for g in gyms))


def get_all_amenities():
    gyms = get_all_gyms()
    amenities = set()
    for gym in gyms:
        amenities.update(gym["amenities"])
    return sorted(list(amenities))
