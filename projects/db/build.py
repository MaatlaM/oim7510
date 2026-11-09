import marimo

__generated_with = "0.24.2"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import duckdb
    import polars as pl
    import altair as alt

    return alt, duckdb, mo, pl


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


@app.cell
def _(database, duckdb):
    def ask(sql):
        with duckdb.connect(database, read_only=True) as _con:
            return _con.sql(sql).pl()

    return (ask,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## The Data
    """)
    return


@app.cell
def _(create_statements, duckdb, mo, pl, view_sql):
    database = mo.notebook_dir() / "database.duckdb"
    _data = mo.notebook_dir() / "data"
    database.unlink(missing_ok=True)

    with duckdb.connect(database) as _con:
        for _statement in create_statements:
            _con.execute(_statement)
        # people one row at a time, managers first: manager_id points at people itself
        _people = pl.read_csv(_data / "people.csv", try_parse_dates=True).sort("person_id")
        for _row in _people.iter_rows():
            _con.execute("INSERT INTO people VALUES (?, ?, ?, ?, ?, ?, ?)", _row)
        for _table in ["projects", "assignments", "tasks", "expenses"]:
            _path = (_data / f"{_table}.csv").as_posix()
            _con.execute(f"INSERT INTO {_table} SELECT * FROM read_csv('{_path}')")
        _con.execute(view_sql)
    return (database,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Notes**

    **`make_data.py`** writes the five CSVs with a fixed random seed (7510), covering the 12 months up to the as_of date, 2026-10-31. The data obeys every rule except one, broken on purpose in exactly two rows: **tasks 1 and 39** are assigned to someone who does not work on the task's project. No constraint can hold that rule, so the database accepts both rows, and question 7 in Part B will list them.

    **database.unlink(missing_ok=True) **deletes the old file, so the database is rebuilt from nothing every time.

    The **for _row **loop inserts people one at a time in **person_id** order, so each manager exists before their reports.

    **read_csv(...) **lets DuckDB read each CSV directly, in table order: projects before assignments, tasks and expenses, because those refer to projects.
    """)
    return


@app.cell
def _(ask):
    # Rule: a task is assigned only to someone who works on its project. Expect tasks 1 and 39.
    ask("""
        SELECT t.task_id, t.project_id, t.assignee_id
        FROM tasks t
        LEFT JOIN assignments a
          ON a.project_id = t.project_id AND a.person_id = t.assignee_id
        WHERE t.assignee_id IS NOT NULL AND a.person_id IS NULL
        ORDER BY t.task_id
    """)
    return


@app.cell
def _(ask):
    # Rule: a task is never assigned before the assignee's start date. Expect no rows.
    ask("""
        SELECT t.task_id, t.created_date, p.start_date
        FROM tasks t
        JOIN people p ON p.person_id = t.assignee_id
        WHERE t.created_date < p.start_date
    """)
    return


@app.cell
def _(ask):
    # Sense check: no expense before its project started. Expect no rows.
    ask("""
        SELECT e.expense_id, e.expense_date, p.start_date
        FROM expenses e
        JOIN projects p USING (project_id)
        WHERE e.expense_date < p.start_date
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## A Look at the Data
    """)
    return


@app.cell
def _(alt, mo, pl):
    _tasks = pl.read_csv(mo.notebook_dir() / "data" / "tasks.csv", try_parse_dates=True)
    _by_day = (
        _tasks.group_by(pl.col("created_date").dt.weekday().alias("weekday"))
        .agg(pl.len().alias("tasks"))
        .sort("weekday")
    )
    mo.ui.altair_chart(
        _by_day.plot.bar(
            x=alt.X("weekday:O", title="Day of the week (1 = Monday, 7 = Sunday)"),
            y=alt.Y("tasks", title="Tasks created"),
        ).properties(title="Tasks created by day of the week")
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Notes**

    Tasks are created only on weekdays, most on Monday (83) and fewest on Thursday (33), with none on weekends. That fits a startup that plans its week on Mondays. However, a real 25-person team would probably log a few tasks over the weekend.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Row Counts
    """)
    return


@app.cell
def _(ask):
    ask("""
        SELECT 'people' AS table_name, count(*) AS row_count FROM people
        UNION ALL SELECT 'projects', count(*) FROM projects
        UNION ALL SELECT 'assignments', count(*) FROM assignments
        UNION ALL SELECT 'tasks', count(*) FROM tasks
        UNION ALL SELECT 'expenses', count(*) FROM expenses
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## A Row It Refuses
    """)
    return


@app.cell
def _(database, duckdb):
    try:
        with duckdb.connect(database) as _con:
            _con.execute(
                "INSERT INTO expenses VALUES (9999, 1, DATE '2026-10-01', -50.00, 'travel', 'negative amount')"
            )
        refused = "accepted"
    except duckdb.ConstraintException as _error:
        refused = str(_error).splitlines()[0]
    refused
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Notes**

    An expense of −$50 breaks the rule that every expense is above zero, so the database refuses it.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Answers You Already Knew
    """)
    return


@app.cell
def _(ask):
    ask("SELECT count(*) AS founders FROM people WHERE manager_id IS NULL")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Notes**

    Expected 2, I asked for two founders who report to nobody.

    Result: 2, matched expected.
    """)
    return


@app.cell
def _(ask):
    ask("SELECT count(*) AS unassigned_tasks FROM tasks WHERE assignee_id IS NULL")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Notes**

    Expected 34, the number of unassigned tasks make_data.py printed.

    Result: 34, matched expected.
    """)
    return


@app.cell
def _(ask):
    ask("SELECT sum(hours_per_week) AS total_hours FROM assignments WHERE person_id = 4")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Notes**

    Expected 50: the sum of person 4’s rows in assignments.csv (13 + 13 + 12 + 12).

    Result: 50, matched expected.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## A View

    Every week the founders ask who is overloaded, so the database keeps that question as a view.
    """)
    return


@app.cell
def _():
    view_sql = """
        CREATE VIEW active_hours_by_person AS
        SELECT p.person_id, p.first_name, p.last_name,
               sum(a.hours_per_week) AS active_hours
        FROM people p
        JOIN assignments a USING (person_id)
        JOIN projects pr USING (project_id)
        WHERE pr.status = 'active'
        GROUP BY p.person_id, p.first_name, p.last_name
    """
    return (view_sql,)


@app.cell
def _(ask):
    ask("SELECT * FROM active_hours_by_person ORDER BY active_hours DESC")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Notes**

    Expected top three: person 5 at 53, person 4 at 50, person 3 at 46.
    """)
    return


if __name__ == "__main__":
    app.run()
