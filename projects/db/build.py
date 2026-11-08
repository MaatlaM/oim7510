import marimo

__generated_with = "0.24.2"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import duckdb
    import polars as pl
    import altair as alt

    return duckdb, mo


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## The Tables
    """)
    return


@app.cell
def _():
    create_statements = [
            """CREATE TABLE people (
                person_id   INTEGER PRIMARY KEY,
                first_name  VARCHAR NOT NULL,
                last_name   VARCHAR NOT NULL,
                work_email  VARCHAR NOT NULL UNIQUE,
                title       VARCHAR NOT NULL,
                start_date  DATE NOT NULL,
                manager_id  INTEGER REFERENCES people(person_id),
                CHECK (manager_id IS NULL OR manager_id <> person_id)
            )""",
            """CREATE TABLE projects (
                project_id  INTEGER PRIMARY KEY,
                name        VARCHAR NOT NULL UNIQUE,
                client_name VARCHAR,
                category    VARCHAR NOT NULL CHECK (category IN ('LLM app', 'data pipeline', 'internal tool')),
                budget      DECIMAL(12,2) NOT NULL CHECK (budget > 0),
                start_date  DATE NOT NULL,
                status      VARCHAR NOT NULL DEFAULT 'planned'
                            CHECK (status IN ('planned', 'active', 'paused', 'done'))
            )""",
            """CREATE TABLE assignments (
                person_id      INTEGER NOT NULL REFERENCES people(person_id),
                project_id     INTEGER NOT NULL REFERENCES projects(project_id),
                role           VARCHAR NOT NULL,
                hours_per_week INTEGER NOT NULL CHECK (hours_per_week BETWEEN 1 AND 40),
                joined_date    DATE NOT NULL,
                PRIMARY KEY (person_id, project_id)
            )""",
            """CREATE TABLE tasks (
                task_id        INTEGER PRIMARY KEY,
                project_id     INTEGER NOT NULL REFERENCES projects(project_id),
                description    VARCHAR NOT NULL,
                created_date   DATE NOT NULL,
                assignee_id    INTEGER REFERENCES people(person_id),
                due_date       DATE NOT NULL,
                completed_date DATE,
                CHECK (completed_date IS NULL OR completed_date >= created_date)
            )""",
            """CREATE TABLE expenses (
                expense_id   INTEGER PRIMARY KEY,
                project_id   INTEGER NOT NULL REFERENCES projects(project_id),
                expense_date DATE NOT NULL,
                amount       DECIMAL(12,2) NOT NULL CHECK (amount > 0),
                category     VARCHAR NOT NULL CHECK (category IN ('GPU cloud', 'data labeling', 'software', 'travel')),
                note         VARCHAR
            )""",
        ]
    return (create_statements,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Notes**

    Five tables, one for each kind of thing BabsonAI Labs keeps track of. Each table has a **primary key**, the column that identifies one row, and **foreign keys** that link rows to other tables. The database also refuses any row that breaks a rule about a single column.

    - **people** is keyed by an invented `person_id` (it gives each person an ID number), because work emails change with title so an email can't identify a person; `work_email` is still `UNIQUE` because no two people can share one. `manager_id` points back at `people` as each person may have a manager and may be empty, because the two founders report to nobody.
    - **projects** only accepts one of the three listed categories and one of the four statuses (so it limits `category` and `status` to their fixed lists with `CHECK`), and requires `budget > 0`. `client_name` may be empty for internal projects.
    - **assignments** records who works on which project. A person can work on several projects, and a project can have several people, so a row is identified by the person and the project together, and the same pairing can't appear twice (many to many). The two-column key `(person_id, project_id)` is what allows one row per pairing, and `hours_per_week` must be between 1 and 40.
    - **tasks** each task belongs to exactly one project and at most one person, or to nobody yet, since `assignee_id` may be empty. A task cannot be completed before it was created.
    - **expenses** each belong to one project, with an amount above zero and one of the four listed categories.

    Two rules need information from more than one table, so the database can't enforce them on its own: a task can only be assigned to someone who works on that project, and never before that person started. Both are checked with queries under The Data.
    """)
    return


@app.cell
def _(create_statements, duckdb):
    with duckdb.connect() as _con:
        for _statement in create_statements:
            _con.execute(_statement)
        tables_check = _con.sql("SHOW TABLES").pl()
    tables_check
    return


if __name__ == "__main__":
    app.run()
