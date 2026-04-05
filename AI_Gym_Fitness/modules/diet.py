def calculate_bmi(height_cm, weight_kg):
    height_m = height_cm / 100
    bmi = weight_kg / (height_m**2)
    return round(bmi, 1)


def get_bmi_category(bmi):
    if bmi < 18.5:
        return {
            "category": "Underweight",
            "color": "warning",
            "description": "You are underweight. Consider a balanced diet with more calories and nutrients.",
        }
    elif bmi < 25:
        return {
            "category": "Normal",
            "color": "success",
            "description": "You have a healthy weight. Maintain your current lifestyle!",
        }
    elif bmi < 30:
        return {
            "category": "Overweight",
            "color": "warning",
            "description": "You are slightly overweight. Consider increasing physical activity.",
        }
    else:
        return {
            "category": "Obese",
            "color": "danger",
            "description": "Your weight may pose health risks. Please consult a healthcare professional.",
        }


def calculate_daily_calories(height, weight, age=25, activity_level="moderate"):
    if activity_level == "sedentary":
        multiplier = 1.2
    elif activity_level == "light":
        multiplier = 1.375
    elif activity_level == "moderate":
        multiplier = 1.55
    elif activity_level == "active":
        multiplier = 1.725
    else:
        multiplier = 1.9

    bmr = 10 * weight + 6.25 * height - 5 * age + 5
    tdee = bmr * multiplier
    return int(tdee)


def get_diet_plan(bmi, goal="maintain", diet_type="non-vegetarian"):
    category = get_bmi_category(bmi)["category"]

    veg_plans = {
        "Underweight": {
            "maintain": {
                "name": "Vegetarian Weight Gain Diet",
                "calories": 2800,
                "meals": {
                    "breakfast": "Oatmeal with banana, nuts, honey +Paneer sandwich",
                    "lunch": "Brown rice, paneer curry, mixed vegetables, curd",
                    "snack": "Peanut butter banana shake",
                    "dinner": "Rajma chawal, salad, tofu",
                    "before_bed": "Milk with almonds and banana",
                },
                "tips": [
                    "Eat frequent meals",
                    "Include paneer and tofu",
                    "Add nuts to everything",
                ],
            },
            "gain": {
                "name": "Vegetarian High Calorie Diet",
                "calories": 3200,
                "meals": {
                    "breakfast": "Paratha with butter, mango lassi, banana",
                    "lunch": "Pasta with cheese, garlic bread, fruit chat",
                    "snack": "Cheese sandwich, nuts, dried fruits",
                    "dinner": "Paneer tikka, naan, jeera rice, pudding",
                    "before_bed": "Protein shake with peanut butter",
                },
                "tips": ["Extra ghee in dal", "Full fat dairy", "Nuts and seeds"],
            },
            "lose": {
                "name": "Vegetarian Healthy Weight",
                "calories": 2500,
                "meals": {
                    "breakfast": "Smoothie with oats, banana, protein powder, milk",
                    "lunch": "Quinoa bowl with chickpeas, veggies, tahini",
                    "snack": "Trail mix with nuts and dark chocolate",
                    "dinner": "Vegetable pulao, dal, salad",
                    "before_bed": "Cottage cheese with fruit",
                },
                "tips": ["Focus on protein", "Include tofu", "Light cardio"],
            },
        },
        "Normal": {
            "maintain": {
                "name": "Vegetarian Balanced Diet",
                "calories": 2200,
                "meals": {
                    "breakfast": "Greek yogurt parfait with granola and fruits",
                    "lunch": "Paneer salad with mixed greens and vinaigrette",
                    "snack": "Apple with almond butter",
                    "dinner": "Vegetable stir-fry, brown rice, dal",
                    "before_bed": "Handful of mixed nuts",
                },
                "tips": ["Balanced macros", "Include dairy", "Stay active"],
            },
            "gain": {
                "name": "Vegetarian Muscle Building",
                "calories": 2700,
                "meals": {
                    "breakfast": "Paneer omelette with spinach, whole grain toast",
                    "lunch": "Vegetable wrap with avocado, brown rice, beans",
                    "snack": "Protein bar and banana",
                    "dinner": "Soya chunks curry, quinoa, mixed vegetables",
                    "before_bed": "Cottage cheese with nuts",
                },
                "tips": [
                    "High protein tofu/paneer",
                    "Complex carbs",
                    "Post-workout nutrition",
                ],
            },
            "lose": {
                "name": "Vegetarian Lean Diet",
                "calories": 1800,
                "meals": {
                    "breakfast": "Oats with chia seeds and berries",
                    "lunch": "Tofu salad with cucumber and lemon",
                    "snack": "Greek yogurt with cucumber",
                    "dinner": "Grilled paneer, steamed broccoli, quinoa",
                    "before_bed": "Warm milk with turmeric",
                },
                "tips": ["500 calorie deficit", "High protein", "Fiber-rich foods"],
            },
        },
        "Overweight": {
            "maintain": {
                "name": "Vegetarian Weight Loss",
                "calories": 1900,
                "meals": {
                    "breakfast": "Vegetable poha with peanuts",
                    "lunch": "Lentil soup with whole wheat roti",
                    "snack": "Carrot sticks with hummus",
                    "dinner": "Vegetable soup, salad, tofu",
                    "before_bed": "Green tea",
                },
                "tips": ["Reduce oils", "Increase vegetables", "Regular exercise"],
            },
            "gain": {
                "name": "Vegetarian Muscle Gain",
                "calories": 2100,
                "meals": {
                    "breakfast": "Protein oatmeal with berries and nuts",
                    "lunch": "Paneer curry, brown rice, steamed broccoli",
                    "snack": "Protein shake with banana",
                    "dinner": "Soya nuggets, quinoa, mixed vegetables",
                    "before_bed": "Greek yogurt with almonds",
                },
                "tips": ["Tofu and paneer", "Controlled carbs", "Strength training"],
            },
            "lose": {
                "name": "Vegetarian Fat Loss",
                "calories": 1500,
                "meals": {
                    "breakfast": "Green smoothie with spinach and apple",
                    "lunch": "Large salad with tofu and olive oil",
                    "snack": "Handful of almonds (15 pieces)",
                    "dinner": "Grilled paneer, steamed vegetables",
                    "before_bed": "Herbal tea",
                },
                "tips": ["Calorie deficit", "No sugar", "Cardio 3-4x weekly"],
            },
        },
        "Obese": {
            "maintain": {
                "name": "Vegetarian Supervised Diet",
                "calories": 1600,
                "meals": {
                    "breakfast": "Two egg whites (or tofu), spinach, whole grain toast",
                    "lunch": "Tofu breast, large mixed salad, no dressing",
                    "snack": "Cucumber and celery sticks",
                    "dinner": "Paneer breast, steamed vegetables",
                    "before_bed": "Herbal tea",
                },
                "tips": ["Consult doctor first", "Start slow", "Walking exercise"],
            },
            "gain": {
                "name": "Vegetarian Controlled Gain",
                "calories": 1800,
                "meals": {
                    "breakfast": "Tofu omelette, oatmeal with berries",
                    "lunch": "Paneer, brown rice, green beans",
                    "snack": "Protein shake",
                    "dinner": "Tofu, sweet potato, salad",
                    "before_bed": "Greek yogurt",
                },
                "tips": [
                    "Medical supervision",
                    "Light resistance",
                    "Progress monitoring",
                ],
            },
            "lose": {
                "name": "Vegetarian Aggressive Loss",
                "calories": 1200,
                "meals": {
                    "breakfast": "Protein shake only",
                    "lunch": "Tofu salad, no croutons",
                    "snack": "Handful of raw almonds",
                    "dinner": "Steamed vegetables, tofu",
                    "before_bed": "Green tea",
                },
                "tips": [
                    "Medical supervision",
                    "Very low calorie",
                    "Regular check-ups",
                ],
            },
        },
    }

    non_veg_plans = {
        "Underweight": {
            "maintain": {
                "name": "Non-Veg Weight Gain Diet",
                "calories": 2800,
                "meals": {
                    "breakfast": "Oatmeal with banana, nuts, honey + 2 eggs + glass of milk",
                    "lunch": "Brown rice, grilled chicken, mixed vegetables, avocado",
                    "snack": "Protein shake with peanut butter and banana",
                    "dinner": "Sweet potato, salmon, broccoli, quinoa",
                    "before_bed": "Greek yogurt with berries",
                },
                "tips": [
                    "Eat more frequent meals",
                    "Include chicken/fish",
                    "Strength training",
                ],
            },
            "gain": {
                "name": "Non-Veg Calorie Surplus",
                "calories": 3200,
                "meals": {
                    "breakfast": "Pancakes with maple syrup, bacon, orange juice",
                    "lunch": "Chicken biryani, garlic bread, salad",
                    "snack": "Cheese, crackers, almonds, dried fruits",
                    "dinner": "Chicken steak, mashed potatoes, green beans",
                    "before_bed": "Casein protein shake with oats",
                },
                "tips": ["500 calorie surplus", "Heavy protein", "Sleep 8+ hours"],
            },
            "lose": {
                "name": "Non-Veg Healthy Weight",
                "calories": 2500,
                "meals": {
                    "breakfast": "Smoothie with oats, banana, protein powder, milk",
                    "lunch": "Grilled chicken bowl with chickpeas, veggies, tahini",
                    "snack": "Trail mix with nuts and dark chocolate",
                    "dinner": "Turkey meatballs, whole grain pasta, marinara",
                    "before_bed": "Cottage cheese with fruit",
                },
                "tips": ["Moderate calories", "Lean chicken/fish", "Light cardio"],
            },
        },
        "Normal": {
            "maintain": {
                "name": "Non-Veg Balanced Diet",
                "calories": 2200,
                "meals": {
                    "breakfast": "Greek yogurt parfait with granola and berries",
                    "lunch": "Grilled chicken salad with mixed greens and vinaigrette",
                    "snack": "Apple with almond butter",
                    "dinner": "Baked salmon, roasted vegetables, quinoa",
                    "before_bed": "Small handful of walnuts",
                },
                "tips": ["Maintain weight", "Balanced macros", "Stay active"],
            },
            "gain": {
                "name": "Non-Veg Muscle Building",
                "calories": 2700,
                "meals": {
                    "breakfast": "Egg white omelette with spinach, whole grain toast",
                    "lunch": "Chicken wrap with avocado, brown rice, black beans",
                    "snack": "Protein bar and banana",
                    "dinner": "Lean beef stir-fry with vegetables, brown rice",
                    "before_bed": "Casein protein with cottage cheese",
                },
                "tips": [
                    "Protein: 1.6g per kg",
                    "Complex carbs",
                    "Post-workout nutrition",
                ],
            },
            "lose": {
                "name": "Non-Veg Lean Cut",
                "calories": 1800,
                "meals": {
                    "breakfast": "Eggs with spinach, tomato, whole grain toast",
                    "lunch": "Grilled fish tacos with cabbage slaw",
                    "snack": "Greek yogurt with cucumber and dill",
                    "dinner": "Grilled chicken breast, asparagus, small potato",
                    "before_bed": "Casein protein shake",
                },
                "tips": ["500 calorie deficit", "High protein", "Light cardio"],
            },
        },
        "Overweight": {
            "maintain": {
                "name": "Non-Veg Weight Reduction",
                "calories": 1900,
                "meals": {
                    "breakfast": "Vegetable egg scramble with whole grain toast",
                    "lunch": "Turkey and avocado lettuce wraps",
                    "snack": "Carrot sticks with hummus",
                    "dinner": "Grilled chicken, large salad, vegetable soup",
                    "before_bed": "Green smoothie with spinach",
                },
                "tips": ["Reduce processed foods", "Lean chicken", "Regular exercise"],
            },
            "gain": {
                "name": "Non-Veg Muscle Building",
                "calories": 2100,
                "meals": {
                    "breakfast": "Protein oatmeal with berries and nuts",
                    "lunch": "Grilled chicken, brown rice, steamed broccoli",
                    "snack": "Protein shake with banana",
                    "dinner": "Fish, quinoa, mixed vegetables",
                    "before_bed": "Greek yogurt with almonds",
                },
                "tips": ["Lean protein", "Controlled carbs", "Consistent training"],
            },
            "lose": {
                "name": "Non-Veg Fat Loss",
                "calories": 1500,
                "meals": {
                    "breakfast": "Protein smoothie with spinach and half banana",
                    "lunch": "Large chicken salad with olive oil dressing",
                    "snack": "Handful of almonds (15 pieces)",
                    "dinner": "Grilled fish, steamed vegetables, no starch",
                    "before_bed": "Warm milk with turmeric",
                },
                "tips": ["Calorie deficit", "No sugar", "Cardio 3-4x weekly"],
            },
        },
        "Obese": {
            "maintain": {
                "name": "Non-Veg Doctor Supervised",
                "calories": 1600,
                "meals": {
                    "breakfast": "Two egg whites, spinach, one slice whole grain toast",
                    "lunch": "Turkey breast, large mixed salad, no dressing",
                    "snack": "Cucumber and celery sticks",
                    "dinner": "Grilled chicken breast, steamed vegetables",
                    "before_bed": "Herbal tea",
                },
                "tips": ["Consult doctor first", "Start slow", "Walking exercise"],
            },
            "gain": {
                "name": "Non-Veg Controlled Gain",
                "calories": 1800,
                "meals": {
                    "breakfast": "Egg white omelette, oatmeal with berries",
                    "lunch": "Grilled chicken, brown rice, green beans",
                    "snack": "Protein shake",
                    "dinner": "Baked fish, sweet potato, salad",
                    "before_bed": "Greek yogurt",
                },
                "tips": [
                    "Medical supervision",
                    "Light resistance",
                    "Progress monitoring",
                ],
            },
            "lose": {
                "name": "Non-Veg Aggressive Loss",
                "calories": 1200,
                "meals": {
                    "breakfast": "Protein shake only",
                    "lunch": "Grilled chicken salad, no croutons",
                    "snack": "Handful of raw almonds",
                    "dinner": "Grilled fish, steamed broccoli",
                    "before_bed": "Green tea",
                },
                "tips": [
                    "Medical supervision",
                    "Very low calorie",
                    "Regular check-ups",
                ],
            },
        },
    }

    plans = veg_plans if diet_type == "vegetarian" else non_veg_plans
    return plans.get(category, plans["Normal"]).get(goal, plans["Normal"]["maintain"])
