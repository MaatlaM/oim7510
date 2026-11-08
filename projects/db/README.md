# Database Project · BabsonAI Labs

## 1. The Scenario

Scenario A, BabsonAI Labs. The as_of date is 2026-10-31; the data covers the 12 months up to it.

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

## 4. Design Choices