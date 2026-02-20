from database import get_connection
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
def load_courses():
    conn = get_connection()
    query = """
    SELECT course_name,Course_organization,difficulty, rating, students_enrolled
    FROM courses
    """
    df = pd.read_sql(query, conn)
    conn.close()
    return df
def recommend_ml(level, interests, top_n=5):
    df = load_courses()
    df["content"] = (df["course_name"] + " " +df["organization"] + " " +df["difficulty"])
    df = df[df["difficulty"].str.lower() == level.lower()]
    if df.empty:
        return []
    vectorizer = TfidfVectorizer(stop_words="english")
    course_vectors = vectorizer.fit_transform(df["content"])
    user_vector = vectorizer.transform([interests])
    similarities = cosine_similarity(user_vector, course_vectors).flatten()
    df["score"] = similarities
    recommendations = df.sort_values( by=["score", "rating", "students_enrolled"],ascending=False).head(top_n)
    return recommendations

if __name__ == "__main__":
    level = input("Your level: ")
    interests = input("Area of Interest: ")
    results = recommend_ml(level, interests)
    print("\nRecommended Courses:\n")
    for _, row in results.iterrows():
        print(f"{row['course_name']} | "f"{row['organization']} | "f"Rating: {row['rating']} | "f"Students: {int(row['students_enrolled'])}")


