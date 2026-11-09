import csv
import random
from datetime import date, timedelta
from pathlib import Path


random.seed(7510)

AS_OF = date(2026, 10, 31)
DATA_DIR = Path(__file__).parent / "data"

people_details = [
    ("Maya", "Patel", "Chief Executive Officer", date(2023, 1, 9), None),
    ("Ethan", "Brooks", "Chief Technology Officer", date(2023, 2, 1), None),
    ("Sofia", "Chen", "VP of Product", date(2023, 4, 3), 1),
    ("Noah", "Williams", "Director of Engineering", date(2023, 6, 5), 1),
    ("Isabella", "Garcia", "Machine Learning Engineer", date(2023, 8, 14), 2),
    ("Liam", "Thompson", "Data Engineer", date(2023, 10, 2), 3),
    ("Olivia", "Reed", "Product Manager", date(2023, 12, 4), 4),
    ("Lucas", "Martin", "Full-Stack Engineer", date(2024, 2, 12), 4),
    ("Amara", "Johnson", "UX Designer", date(2024, 4, 1), 5),
    ("Benjamin", "Davis", "Machine Learning Engineer", date(2024, 6, 10), 5),
    ("Chloe", "Wilson", "Data Analyst", date(2024, 8, 5), 6),
    ("Alexander", "Moore", "Software Engineer", date(2024, 10, 7), 7),
    ("Priya", "Singh", "Data Engineer", date(2024, 12, 2), 8),
    ("Daniel", "Clark", "Customer Success Lead", date(2025, 2, 3), 8),
    ("Ava", "Lewis", "Product Designer", date(2025, 4, 7), 9),
    ("James", "Walker", "Software Engineer", date(2025, 6, 2), 10),
    ("Zoe", "Hall", "Solutions Engineer", date(2025, 8, 4), 11),
    ("Henry", "Young", "Data Analyst", date(2025, 10, 6), 12),
    ("Layla", "Allen", "Machine Learning Engineer", date(2025, 11, 17), 13),
    ("Elijah", "Scott", "Software Engineer", date(2025, 12, 8), 14),
    ("Grace", "Adams", "Product Manager", date(2026, 1, 12), 15),
    ("Mateo", "Baker", "Customer Success Specialist", date(2026, 3, 2), 16),
    ("Nora", "Nelson", "Data Engineer", date(2026, 5, 4), 18),
    ("Owen", "Carter", "UX Designer", date(2026, 7, 6), 19),
    ("Aisha", "Mitchell", "Software Engineer", date(2026, 9, 8), 20),
]

people = []
person_start_dates = {}
for person_id, details in enumerate(people_details, start=1):
    first_name, last_name, title, start_date, manager_id = details
    work_email = f"{first_name.lower()}.{last_name.lower()}@babsonai.com"
    people.append(
        [
            person_id,
            first_name,
            last_name,
            work_email,
            title,
            start_date.isoformat(),
            "" if manager_id is None else manager_id,
        ]
    )
    person_start_dates[person_id] = start_date

projects = [
    [1, "Smart Intake Copilot", "Elm Street Dental", "LLM app", 175000, date(2025, 11, 10), "active"],
    [2, "Inventory Forecast Studio", "Harbor & Pine Market", "LLM app", 240000, date(2025, 11, 17), "active"],
    [3, "Service Desk Reply Assistant", "Northstar HVAC", "LLM app", 30000, date(2025, 12, 1), "active"],
    [4, "Invoice Match Pipeline", "Cornerstone Bookkeeping", "data pipeline", 180000, date(2026, 1, 5), "active"],
    [5, "Local SEO Content Planner", "Bloom & Birch Florist", "LLM app", 150000, date(2026, 2, 2), "active"],
    [6, "Appointment No-Show Signals", "Calm Harbor Wellness", "data pipeline", 220000, date(2026, 3, 2), "active"],
    [7, "Vendor Document Hub", "", "internal tool", 280000, date(2026, 4, 6), "active"],
    [8, "Support Metrics Warehouse", "", "internal tool", 95000, date(2025, 11, 3), "done"],
    [9, "Returns Triage Workflow", "Maple & Main Outfitters", "LLM app", 130000, date(2026, 1, 12), "done"],
    [10, "Sales Call Notes Search", "", "internal tool", 160000, date(2026, 5, 4), "paused"],
    [11, "Quick Quote Builder Pilot", "Cedar & Stone Renovation", "LLM app", 80000, date(2026, 10, 15), "planned"],
    [12, "Team Knowledge Base Refresh", "", "internal tool", 60000, date(2026, 10, 20), "planned"],
]

project_teams = {
    1: [3, 4, 5, 6],
    2: [3, 4, 7, 8],
    3: [3, 5, 8, 9],
    4: [4, 6, 9, 10, 11],
    5: [4, 5, 10, 12],
    6: [3, 6, 11, 13, 14],
    7: [5, 7, 12, 15],
    8: [8, 9, 10, 13],
    9: [9, 11, 14, 16],
    10: [12, 15, 17, 18],
    11: [19, 20, 21, 22],
    12: [22, 23, 24, 25],
}

role_by_person = {
    3: "Product lead",
    4: "Engineering lead",
    5: "Machine learning engineer",
    6: "Data engineer",
    7: "Product manager",
    8: "Software engineer",
    9: "UX designer",
    10: "Machine learning engineer",
    11: "Data analyst",
    12: "Software engineer",
    13: "Data engineer",
    14: "Customer success lead",
    15: "Product designer",
    16: "Software engineer",
    17: "Solutions engineer",
    18: "Data analyst",
    19: "Machine learning engineer",
    20: "Software engineer",
    21: "Product manager",
    22: "Customer success specialist",
    23: "Data engineer",
    24: "UX designer",
    25: "Software engineer",
}

hours_by_pair = {
    (3, 1): 12,
    (3, 2): 12,
    (3, 3): 11,
    (3, 6): 11,
    (4, 1): 13,
    (4, 2): 13,
    (4, 4): 12,
    (4, 5): 12,
    (5, 1): 13,
    (5, 3): 13,
    (5, 5): 15,
    (5, 7): 12,
    (6, 1): 10,
    (6, 4): 10,
    (6, 6): 10,
}

assignments = []
joined_dates = {}
project_start_dates = {}
for project in projects:
    project_id = project[0]
    project_start = project[5]
    project_start_dates[project_id] = project_start
    for person_id in project_teams[project_id]:
        earliest_join_date = max(person_start_dates[person_id], project_start)
        latest_join_date = min(earliest_join_date + timedelta(days=14), AS_OF)
        joined_date = earliest_join_date + timedelta(
            days=random.randint(0, (latest_join_date - earliest_join_date).days)
        )
        joined_dates[(person_id, project_id)] = joined_date
        hours = hours_by_pair.get((person_id, project_id), random.randint(8, 24))
        assignments.append(
            [
                person_id,
                project_id,
                role_by_person[person_id],
                hours,
                joined_date.isoformat(),
            ]
        )


def random_weekday(start_date, end_date):
    chosen_date = start_date + timedelta(
        days=random.randint(0, (end_date - start_date).days)
    )
    if chosen_date.weekday() >= 5:
        if chosen_date + timedelta(days=2) <= end_date:
            chosen_date += timedelta(days=2)
        else:
            chosen_date -= timedelta(days=1)
    return chosen_date


task_phrases = [
    "Review sample records and document edge cases",
    "Test the latest workflow with a customer",
    "Refine the prompt and compare response quality",
    "Build validation checks for incoming data",
    "Prepare a short product feedback summary",
    "Fix an issue found during user acceptance testing",
    "Update the onboarding guide and example files",
    "Measure processing time on a representative dataset",
    "Review access permissions and audit events",
    "Share a progress update with the project team",
]

task_counts = {
    1: 38,
    2: 36,
    3: 35,
    4: 34,
    5: 32,
    6: 31,
    7: 28,
    8: 18,
    9: 16,
    10: 14,
    11: 2,
    12: 1,
}

tasks = []
rule_breaking_task_ids = []
task_id = 1
for project in projects:
    project_id = project[0]
    project_start = project[5]
    team = project_teams[project_id]
    earliest_team_join = min(joined_dates[(person_id, project_id)] for person_id in team)
    task_start = max(project_start, earliest_team_join)

    for project_task_number in range(task_counts[project_id]):
        if project_task_number < 2 and project_id in (1, 2):
            created_date = random_weekday(date(2026, 6, 1), AS_OF)
        elif project_task_number == 0 and project_id <= 10:
            created_date = random_weekday(max(task_start, AS_OF - timedelta(days=90)), AS_OF)
        else:
            created_date = random_weekday(task_start, AS_OF)

        due_date = created_date + timedelta(days=random.randint(3, 45))
        is_rule_breaking_task = project_id in (1, 2) and project_task_number == 0
        if is_rule_breaking_task:
            outsider_ids = [
                person_id
                for person_id in person_start_dates
                if person_id not in team and person_start_dates[person_id] <= created_date
            ]
            assignee_id = random.choice(outsider_ids)
            rule_breaking_task_ids.append(task_id)
        elif random.random() < 0.10:
            assignee_id = ""
        else:
            eligible_people = [
                person_id
                for person_id in team
                if joined_dates[(person_id, project_id)] <= created_date
            ]
            assignee_id = random.choice(eligible_people)

        if project_task_number == 0 and project_id <= 10:
            completed_date = ""
        elif random.random() < 0.68:
            completed_date = random_weekday(created_date, AS_OF).isoformat()
        else:
            completed_date = ""

        description = f"{random.choice(task_phrases)} for {project[1].lower()}"
        tasks.append(
            [
                task_id,
                project_id,
                description,
                created_date.isoformat(),
                assignee_id,
                due_date.isoformat(),
                completed_date,
            ]
        )
        task_id += 1


expense_notes = {
    "GPU cloud": [
        "Model evaluation compute",
        "Prototype inference usage",
        "GPU training run",
        "Embedding index refresh",
    ],
    "data labeling": [
        "Labeled support examples",
        "Invoice review batch",
        "Quality check for annotations",
        "Customer ticket classification",
    ],
    "software": [
        "Design collaboration seats",
        "Monitoring subscription",
        "Test environment license",
        "Workflow automation plan",
    ],
    "travel": [
        "Customer discovery visit",
        "Pilot kickoff transit",
        "On-site workflow review",
        "Regional client workshop",
    ],
}

expense_categories = ["GPU cloud", "data labeling", "software", "travel"]
expenses = []
expense_id = 1
projects_without_expenses = [11, 12]
for project in projects:
    project_id = project[0]
    if project_id in projects_without_expenses:
        continue

    project_start = project[5]
    for expense_number in range(18):
        category = random.choice(expense_categories)
        if project_id == 3 and category in ("GPU cloud", "data labeling"):
            low, high = (4000, 9000) if category == "GPU cloud" else (3000, 7000)
        elif category == "GPU cloud":
            low, high = 500, 3000
        elif category == "data labeling":
            low, high = 800, 4000
        elif category == "software":
            low, high = 100, 1600
        else:
            low, high = 150, 1800

        if expense_number < 8:
            earliest_date = max(project_start, AS_OF - timedelta(days=89))
        else:
            earliest_date = project_start
        expense_date = random_weekday(earliest_date, AS_OF)
        amount = random.randint(low, high)
        note = random.choice(expense_notes[category])
        expenses.append(
            [
                expense_id,
                project_id,
                expense_date.isoformat(),
                f"{amount:.2f}",
                category,
                note,
            ]
        )
        expense_id += 1


def write_csv(file_name, columns, rows):
    with (DATA_DIR / file_name).open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(columns)
        writer.writerows(rows)


DATA_DIR.mkdir(parents=True, exist_ok=True)
write_csv(
    "people.csv",
    ["person_id", "first_name", "last_name", "work_email", "title", "start_date", "manager_id"],
    people,
)
write_csv(
    "projects.csv",
    ["project_id", "name", "client_name", "category", "budget", "start_date", "status"],
    [
        [*project[:4], f"{project[4]:.2f}", project[5].isoformat(), project[6]]
        for project in projects
    ],
)
write_csv(
    "assignments.csv",
    ["person_id", "project_id", "role", "hours_per_week", "joined_date"],
    assignments,
)
write_csv(
    "tasks.csv",
    ["task_id", "project_id", "description", "created_date", "assignee_id", "due_date", "completed_date"],
    tasks,
)
write_csv(
    "expenses.csv",
    ["expense_id", "project_id", "expense_date", "amount", "category", "note"],
    expenses,
)

active_project_ids = {
    project[0] for project in projects if project[6] == "active"
}
active_hours_by_person = {}
for assignment in assignments:
    person_id, project_id, _, hours, _ = assignment
    if project_id in active_project_ids:
        active_hours_by_person[person_id] = active_hours_by_person.get(person_id, 0) + hours

unassigned_task_count = sum(1 for task in tasks if task[4] == "")
print(f"people: {len(people)} rows")
print(f"projects: {len(projects)} rows")
print(f"assignments: {len(assignments)} rows")
print(f"tasks: {len(tasks)} rows")
print(f"expenses: {len(expenses)} rows")
print(f"Rule-breaking task_ids: {rule_breaking_task_ids}")
print(f"Unassigned tasks: {unassigned_task_count}")
print(f"Project_ids with no expenses: {projects_without_expenses}")
print("People over 40 hours per week on active projects:")
for person_id, hours in sorted(active_hours_by_person.items()):
    if hours > 40:
        print(f"  person_id {person_id}: {hours} hours")
