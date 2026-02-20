from database import get_connection
def save_user(level, interests, goal):
    conn = get_connection()
    cursor = conn.cursor()

    sql = """
    INSERT INTO users (level, interests, goal)
    VALUES (%s, %s, %s)
    """

    cursor.execute(sql, (level, interests, goal))
    conn.commit()

    cursor.close()
    conn.close()
    print("User preferences saved!")
def recommend_courses(level, interests):
    conn = get_connection()
    cursor = conn.cursor()

    keywords = interests.lower().split(",")

    query = """
    SELECT course_name, organization, rating, difficulty, students_enrolled
    FROM courses
    WHERE difficulty = %s
    """

    cursor.execute(query, (level,))
    courses = cursor.fetchall()

    recommendations = []

    for course in courses:
        course_name = course["course_name"].lower()
        org = course["organization"].lower()

        score = 0
        for kw in keywords:
            if kw.strip() in course_name or kw.strip() in org:
                score += 1

        if score > 0:
            recommendations.append((score, course))

    recommendations.sort(
        key=lambda x: (-x[0], -(x[1]["rating"] or 0))
    )

    cursor.close()
    conn.close()

    return recommendations

level = input("Your level:")
interests = input("Area of Interest:")
goal = input("Your desired Goal:")
save_user(level, interests, goal)
results = recommend_courses(level, interests)
print("\nRecommended Courses:\n")
for score, course in results[:5]:
    print(f"- {course['course_name']} | " f"{course['organization']} | " f"Rating: {course['rating']}")

