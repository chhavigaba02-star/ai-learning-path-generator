from google import genai
from dotenv import load_dotenv
import os
from recommendation import recommend_courses  # only this file

load_dotenv()

# Initialize Gemini
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))


def format_db_results(results):
    """Convert DB recommendation list to text for LLM"""

    if not results:
        return "No recommendations found."

    text = ""
    for score, course in results:
        text += f"""
Course: {course['course_name']}
Organization: {course['organization']}
Difficulty: {course['difficulty']}
Rating: {course['rating']}
Relevance Score: {score}
"""
    return text


def generate_learning_path(level, interests, goal):
    """
    Pipeline:
    1. Get DB recommendations
    2. Send to LLM
    """

    # Get recommendations from recommendation.py
    db_results = recommend_courses(level, interests)

    db_text = format_db_results(db_results)

    prompt = f"""
You are an expert AI learning advisor.

User Profile:
Level: {level}
Interests: {interests}
Goal: {goal}

Recommended Courses:
{db_text}

Create a structured learning path:

1. Best starting courses
2. Intermediate progression
3. Advanced roadmap
4. Why each course is recommended
5. Suggested order

Be clear and structured.
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text


# CLI testing
if __name__ == "__main__":
    level = input("Your level: ")
    interests = input("Area of Interest: ")
    goal = input("Your Goal: ")

    result = generate_learning_path(level, interests, goal)

    print("\nAI Generated Learning Path:\n")
    print(result)
