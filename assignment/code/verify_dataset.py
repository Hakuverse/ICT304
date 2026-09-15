import csv
from pathlib import Path

data_file = (
    Path(__file__).resolve().parents[1]
    / "data"
    / "student-mat.csv"
)

with data_file.open(newline="", encoding="utf-8") as file:
    students = list(csv.DictReader(file, delimiter=";"))

high_risk = sum(int(student["G3"]) < 10 for student in students)
low_risk = sum(int(student["G3"]) >= 10 for student in students)

print("Total students:", len(students))
print("High Risk:", high_risk)
print("Low Risk:", low_risk)
print("Number of columns:", len(students[0]))


print("Dataset verification passed!")
