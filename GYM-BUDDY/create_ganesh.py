from modules.auth import create_user

result = create_user(
    username="Ganesh",
    email="ganesh@example.com",
    password="Ganesh@08",
    full_name="Ganesh",
    age=25,
    gender="male",
    diet_type="non-vegetarian",
    is_admin=1,
)

print(result)
