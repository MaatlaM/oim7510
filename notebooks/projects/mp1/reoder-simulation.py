# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "marimo",
# ]
# ///
"""Mini Project 1.
"""

import marimo

__generated_with = "0.24.2"
app = marimo.App(width="medium", sql_output="polars")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Mini Project 1

    Your choice of option, what each one asks for, the due date and how it is graded are on the Mini Project 1 page of the course site, linked from the calendar. This notebook is the shape to build it in. Keep the headings, and replace each line in italics with your own.

    Save it in your course repository as `projects/mp1/<your-tool>.py`, named for what it does, such as `loan-schedule.py`, and open it with `uv run marimo edit`.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 1. The Question

    *Who would use this, and what decision does it help them make? Two or three sentences, in words somebody outside this course would understand.*
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The coffee shop owner or manager would use this tool to decide how low the oat milk inventory should fall before they place a new order. By comparing different reorder points (the stock levels that trigger an order), they can see which option best balances running out of oat milk and losing sales against ordering too early and taking up limited refrigerator space. Finding the right balance is the challenge because demand ranges from 8 to 20 cartons a day, while deliveries take three days to arrive in lots of 100 cartons.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 2. My Plan Before AI

    *Before you ask your agent anything, write how you would solve it: the steps, in order, in plain words, in five lines or more. Then answer these two questions:*

    - *What does your loop carry from one step to the next, the way a running total carries its sum?*
    - *Which check will you use in section 6, and which two numbers should agree?*

    *Commit this notebook with the message `mp1: plan before AI`.*
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Steps**

    1. Start with 60 cartons in stock and no orders on the way. Each order is 100 cartons and arrives 3 days after it is placed.
    2. Each day, add any delivery due that day to the Starting Stock to get the Available Stock.
    3. Sell up to that day’s demand. Any demand above the Available Stock is lost.
    4. Calculate the Ending Stock where Ending Stock = Available Stock − Cartons Sold.
    5. Add the Ending Stock to the cartons on order but not yet delivered. If the total is at or below the reorder point, order 100 cartons, due 3 days later. An order placed on day 2 arrives at the start of day 5.
    6. Repeat for all 30 days, recording one row per day for a reorder point of 40.
    7. Run the same simulation for reorder points of 20, 30, 40 and 50, and compare units lost, days with lost sales, orders placed, and average ending stock.
    8. Recommend the reorder point that best balances lost sales against stock sitting in the refrigerator.

    **Question 1: What does your loop carry from one step to the next, the way a running total carries its sum?**

    The stock on hand, the orders on the way with their arrival days, and running totals of units lost, days with lost sales, orders placed, and ending stock (for the average). Each day starts where the previous day ended.

    **Question 2: Which check will you use in section 6, and which two numbers should agree?**

    Over the 30 days, 60 + Total Arrivals − Total Sold should equal the Ending Stock on day 30. Lost sales are not subtracted, because those cartons were never sold. As a second check, Total Sold + Total Lost should equal Total Demand (399 cartons).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 3. Inputs

    Every number the project starts from goes in the cell below, and nowhere else, so that changing one input changes every result after it.

    Copy in the default inputs for your option from the Mini Project 1 page. If you chose D, your own option, type your data in here, or ask your agent to generate it with `faker`. The required part reads no file.
    """)
    return


@app.cell
def _():
    # Your inputs.
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 4. The Work

    Add as many cells as you need. Try each step yourself before you ask your agent, and commit as you go.
    """)
    return


@app.cell
def _():
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 5. The Answer

    *A table of your results in the cell below, printed with `print` and f-strings, then one sentence here that answers the question in section 1, with the number in it.*
    """)
    return


@app.cell
def _():
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 6. How I Know These Numbers Are Right

    *At least one check that reaches a result a second, independent way. Name what you compared and what came out.*
    """)
    return


@app.cell
def _():
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 7. Working With the Agent

    *Pick one piece of AI output you did not accept as-is. What did it give you, what did you change, and how did you know? Point to the commit or the cell.*

    *If the agent got it right the first time: what did you do to verify that?*
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 8. Going Further

    *Take at least one step past the main task, in any direction, and use your agent as much as you like. It does not have to work. State what you tried, what you found, and where it is in this notebook.*
    """)
    return


if __name__ == "__main__":
    app.run()
