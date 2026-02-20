import pandas as pd
import csv
import os
from database import get_connection

EXCEL_FILE = "courses1.xlsx"
CSV_FILE = "courses1.csv"


def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        level VARCHAR(50),
        interests TEXT,
        goal TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS courses (
        id INT AUTO_INCREMENT PRIMARY KEY,
        course_id VARCHAR(50),
        course_name VARCHAR(255),
        organization VARCHAR(255),
        certificate_type VARCHAR(100),
        rating FLOAT,
        difficulty VARCHAR(50),
        students_enrolled BIGINT UNSIGNED
    )
    """)

    cursor.close()
    conn.close()
    print("Tables created / verified!")


def convert_excel_to_csv(excel_file, csv_file):
    if not os.path.exists(csv_file):
        df = pd.read_excel(excel_file)
        df.to_csv(csv_file, index=False)
        print("Excel successfully converted to CSV")
    else:
        print("CSV already exists, skipping conversion")


def load_csv_to_courses(csv_file):
    conn = get_connection()
    cursor = conn.cursor()

    sql = """
    INSERT INTO courses (
        course_id,
        course_name,
        organization,
        certificate_type,
        rating,
        difficulty,
        students_enrolled
    )
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    """

    with open(csv_file, newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        print("CSV headers:", reader.fieldnames)

        for row in reader:
            rating = float(row["Course_rating"]) if row["Course_rating"] else None
            students = int(float(row["Course_students_enrolled"].replace(",", ""))) if row["Course_students_enrolled"] else 0

            cursor.execute(sql, (
                row["Course_id"].strip(),
                row["Course"].strip(),
                row["Course_organization"].strip(),
                row["Course_Certificate_type"].strip(),
                rating,
                row["Course_difficulty"].strip(),
                students
            ))

    conn.commit()
    cursor.close()
    conn.close()
    print("CSV data successfully inserted into courses table")


if __name__ == "__main__":
    create_tables()
    convert_excel_to_csv(EXCEL_FILE, CSV_FILE)
    load_csv_to_courses(CSV_FILE)





