"""
This module generates a simple user profile based on age and hobbies.
"""

def generate_profile(age):
    """
    Function to determine the user's life stage based on their age.
    :param age: The user's age. An integer.
    :return: The life stage as a string.
    """
    if 0 <= age <= 12:
        return "Child"
    elif 13 <= age <= 19:
        return "Teenager"
    elif age >= 20:
        return "Adult"


user_name = input("Hello User! Enter your full name, please?")
birth_year_str = input("What is your date of birth?")
birth_year = int(birth_year_str)
current_year = 2025
current_age = current_year - birth_year

hobbies = []
hobby = input("Enter a favorite hobby or type 'stop' to finish")

while hobby != "stop":
    hobbies.append(hobby)
    hobby = input("Enter a favorite hobby or type 'stop' to finish")
size = len(hobbies)

life_stage = generate_profile(current_age)
user_profile = {"name": user_name,
                "age": current_age,
                "stage": life_stage,
                "hobbies": hobbies}

print(
    f"Profile Summary: "
    f"\nName: {user_profile['name']} "
    f"\nCurrent age: {user_profile['age']} "
    f"\nLife stage: {user_profile['stage']}"
)

if hobbies:
    print(f"Favorite Hobbies ({size}): ")
else:
    print("You didn't mention any hobbies.")

for i in hobbies:
    print(f"• {i}")
