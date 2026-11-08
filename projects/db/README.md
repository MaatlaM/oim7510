# Database Project · BabsonAI Labs

## 1. The Scenario

Scenario A. BabsonAI Labs: a startup founded by Babson students that builds AI tools for small businesses. It tracks its people, projects, staffing, tasks and spending in spreadsheets and chat threads. Its founders want to see who works on what, where the money goes, and who is overloaded. The as_of date is 2026-10-31, and the data covers the 12 months up to it.

## 2. The ERD

```mermaid
erDiagram
  PEOPLE |o--o{ PEOPLE : "manages"
  PEOPLE ||--o{ ASSIGNMENTS : "is assigned"
  PROJECTS ||--o{ ASSIGNMENTS : "is staffed by"
  PROJECTS ||--o{ TASKS : "contains"
  PEOPLE |o--o{ TASKS : "is assigned"
  PROJECTS ||--o{ EXPENSES : "incurs"

  PEOPLE {
    int person_id PK
    string first_name
    string last_name
    string work_email
    string title
    date start_date
    int manager_id FK
  }
  PROJECTS {
    int project_id PK
    string name
    string client_name
    string category
    decimal budget
    date start_date
    string status
  }
  ASSIGNMENTS {
    int person_id PK, FK
    int project_id PK, FK
    string role
    int hours_per_week
    date joined_date
  }
  TASKS {
    int task_id PK
    int project_id FK
    string description
    date created_date
    int assignee_id FK
    date due_date
    date completed_date
  }
  EXPENSES {
    int expense_id PK
    int project_id FK
    date expense_date
    decimal amount
    string category
    string note
  }
```

## 3. What One Row Means

- One row of `people` is one person who works at BabsonAI Labs.
- One row of `projects` is one project the company has planned, is running, has paused or has finished.
- One row of `assignments` is one person's commitment to one project: their role on it, the hours a week they give it, and the date they joined it.
- One row of `tasks` is one piece of work belonging to one project, assigned to at most one person.
- One row of `expenses` is one amount spent on one project.

## 4. Design Choices