
from task_agent import check_exam_eligibility

for n in [82, 70, 50, 120]:
    result = check_exam_eligibility.invoke(
        {"attendance_percent": n}
    )
    print(f"{n}% -> {result}")
