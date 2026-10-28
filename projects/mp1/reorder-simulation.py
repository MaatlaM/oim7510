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
    starting_stock = 60
    order_quantity = 100
    lead_time_days = 3
    reorder_points = [20, 30, 40, 50]
    specified_reorder_point = 40
    daily_demand = [12, 15, 9, 14, 18, 11, 10, 16, 13, 17, 8, 12, 20, 14, 11,
                    9, 15, 13, 16, 12, 10, 14, 19, 11, 13, 15, 9, 12, 17, 14]
    return (
        daily_demand,
        lead_time_days,
        order_quantity,
        reorder_points,
        specified_reorder_point,
        starting_stock,
    )


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 4. The Work

    Add as many cells as you need. Try each step yourself before you ask your agent, and commit as you go.
    """)
    return


@app.cell
def _(daily_demand, lead_time_days, order_quantity, starting_stock):
    def simulate(reorder_point):
        stock = starting_stock
        pending = {}
        rows = []
        day = 0
        for demand in daily_demand:
            day = day + 1
            start = stock

            # 1. Deliveries due today arrive first
            arrived = pending.get(day, 0)
            stock = stock + arrived

            # 2. Sell up to today's demand; the rest is lost
            if demand <= stock:
                sold = demand
            else:
                sold = stock
            lost = demand - sold
            stock = stock - sold

            # 3. Count cartons ordered but not yet delivered
            on_order = 0
            for arrival_day, cartons in pending.items():
                if arrival_day > day:
                    on_order = on_order + cartons

            # 4. Order if stock plus what is on the way is at or below the reorder point
            ordered = 0
            if stock + on_order <= reorder_point:
                ordered = order_quantity
                due_day = day + lead_time_days
                pending[due_day] = pending.get(due_day, 0) + order_quantity

            rows.append({"Day": day, "Start": start, "Arrived": arrived,
                         "Demand": demand, "Sold": sold, "Lost": lost,
                         "End": stock, "Ordered": ordered})
        return rows

    return (simulate,)


@app.cell
def _(simulate, specified_reorder_point):
    detail_rows = simulate(specified_reorder_point)

    print(f"Daily results for a reorder point of {specified_reorder_point}")
    print(f"{'Day':>4} {'Start':>6} {'Arrived':>8} {'Demand':>7} {'Sold':>5} {'Lost':>5} {'End':>5} {'Ordered':>8}")
    for _row in detail_rows:
        print(f"{_row['Day']:>4} {_row['Start']:>6} {_row['Arrived']:>8} {_row['Demand']:>7} "
              f"{_row['Sold']:>5} {_row['Lost']:>5} {_row['End']:>5} {_row['Ordered']:>8}")
    return (detail_rows,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 5. The Answer

    *A table of your results in the cell below, printed with `print` and f-strings, then one sentence here that answers the question in section 1, with the number in it.*
    """)
    return


@app.cell
def _(daily_demand, reorder_points, simulate):
    summary = []
    for _rp in reorder_points:
        _rows = simulate(_rp)
        _units_lost = 0
        _lost_days = 0
        _orders = 0
        _end_total = 0
        for _row in _rows:
            _units_lost = _units_lost + _row["Lost"]
            if _row["Lost"] > 0:
                _lost_days = _lost_days + 1
            if _row["Ordered"] > 0:
                _orders = _orders + 1
            _end_total = _end_total + _row["End"]
        summary.append({"Reorder point": _rp, "Units lost": _units_lost,
                        "Lost days": _lost_days, "Orders": _orders,
                        "Avg end": _end_total / len(daily_demand)})

    print(f"{'Reorder point':>13} {'Units lost':>10} {'Days with loss':>14} {'Orders':>6} {'Avg ending stock':>16}")
    for _s in summary:
        print(f"{_s['Reorder point']:>13} {_s['Units lost']:>10} {_s['Lost days']:>14} "
              f"{_s['Orders']:>6} {_s['Avg end']:>16.1f}")
    return (summary,)


@app.cell
def _(daily_demand, summary):
    best = None
    for _s in summary:
        if _s["Units lost"] == 0:
            if best is None or _s["Avg end"] < best["Avg end"]:
                best = _s

    print(f"Reorder when stock falls to {best['Reorder point']} cartons because at this level the shop lost no sales "
          f"over {len(daily_demand)} days, with {best['Avg end']:.1f} cartons in the "
          f"refrigerator on average, which is the least of any option where the shop never ran out of oat milk.")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 6. How I Know These Numbers Are Right

    *At least one check that reaches a result a second, independent way. Name what you compared and what came out.*
    """)
    return


@app.cell
def _(daily_demand, detail_rows, starting_stock):
    _total_arrived = 0
    _total_sold = 0
    _total_lost = 0
    for _row in detail_rows:
        _total_arrived = _total_arrived + _row["Arrived"]
        _total_sold = _total_sold + _row["Sold"]
        _total_lost = _total_lost + _row["Lost"]

    _from_totals = starting_stock + _total_arrived - _total_sold
    _from_simulation = detail_rows[-1]["End"]

    print(f"Check 1 (stock): {starting_stock} + {_total_arrived} arrived - {_total_sold} sold "
          f"= {_from_totals}; the simulation ended day {len(daily_demand)} with {_from_simulation}. "
          f"Match: {_from_totals == _from_simulation}")
    print(f"Check 2 (demand): {_total_sold} sold + {_total_lost} lost = {_total_sold + _total_lost}; "
          f"total demand was {sum(daily_demand)}. Match: {_total_sold + _total_lost == sum(daily_demand)}")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Check 1, stock. **

    The simulation carries stock forward one day at a time. As a second route, I added up the 30-day totals instead: starting stock (60) plus all deliveries (400) minus all sales (399) gives 61, the same as the simulation’s ending stock on day 30.

    **Check 2, demand. **

    Every carton a customer wanted was either sold or lost. Sold (399) plus lost (0) equals total demand from the input list (399).
    """)
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
    **What it gave me.**

    The agent’s first plan for the simulation stored each day’s results as a tuple of eight values and removed orders from the pending dictionary once they arrived.

    **What I changed.**

    I compared that plan against notebooks 2 and 3. We have not yet covered deleting from a dictionary, and notebook 3’s guide to choosing a data structure says that many things with named parts should be a list of dictionaries. I asked the agent to rework it, so each day is now a dictionary read by name (row["Lost"]), and orders still on the way are found by keeping only those with arrival_day > day, using .items() and an if, both of which we have covered.

    **How I knew it was right.**

    The daily table for a reorder point of 40 matched a hand trace of days 1 to 5: an order on day 2, arriving on day 5, with no order on day 3 because 100 cartons were already on the way. Both checks in section 6 also agree.

    **Where.**

    Cell 1 in section 4.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 8. Going Further

    *Take at least one step past the main task, in any direction, and use your agent as much as you like. It does not have to work. State what you tried, what you found, and where it is in this notebook.*
    """)
    return


@app.cell
def _(daily_demand, simulate):
    # Going further: put a dollar cost on each part of the trade-off
    holding_cost = 0.50   # per carton, for each night in the refrigerator
    delivery_fee = 40     # per order placed
    lost_margin = 8       # per carton a customer wanted but could not buy
    cost_reorder_points = [10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80]

    cost_summary = []
    for _rp in cost_reorder_points:
        _fridge = 0
        _delivery = 0
        _lost = 0
        for _row in simulate(_rp):
            _fridge = _fridge + _row["End"] * holding_cost
            if _row["Ordered"] > 0:
                _delivery = _delivery + delivery_fee
            _lost = _lost + _row["Lost"] * lost_margin
        cost_summary.append({"Reorder point": _rp, "Fridge": _fridge, "Delivery": _delivery,
                             "Lost": _lost, "Total": _fridge + _delivery + _lost})

    print(f"{'Reorder point':>13} {'Fridge':>9} {'Deliveries':>10} {'Lost sales':>10} {'Total':>9}")
    for _c in cost_summary:
        print(f"{_c['Reorder point']:>13} {_c['Fridge']:>9,.2f} {_c['Delivery']:>10,.2f} "
              f"{_c['Lost']:>10,.2f} {_c['Total']:>9,.2f}")

    cheapest = cost_summary[0]
    for _c in cost_summary:
        if _c["Total"] < cheapest["Total"]:
            cheapest = _c

    print(f"\nCheapest: a reorder point of {cheapest['Reorder point']}, "
          f"costing ${cheapest['Total']:,.2f} over {len(daily_demand)} days.")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **What I tried.**

    I put a dollar cost on each side of the trade-off: $0.50 per carton for each night in the refrigerator, $40 per delivery, and $8 of lost margin per carton a customer could not buy. I then tested reorder points from 10 to 80, reusing the same simulation function.

    **What I found.**

    A reorder point of 40 is the cheapest, at $886.50 over 30 days, which supports the recommendation in section 5. Reordering at 35 costs $904.00 because five lost cartons outweigh the fridge space saved, and every point above 40 costs more because extra stock sits in the refrigerator.

    **Where.**

    Cell 1 at the start of section 8.
    """)
    return


if __name__ == "__main__":
    app.run()
