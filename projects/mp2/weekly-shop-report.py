import marimo

__generated_with = "0.24.2"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #1. The Question.

    Who would use this, and what decision does it help them make? Two or three sentences, in words somebody outside this course would understand.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The operations manager at Northwind Traders needs a weekly report covering the seven days ending today, including today. The report will show the number of orders, total revenue, revenue by shipping country, the top five products by units sold, and orders that have not shipped yet. It will help the manager understand the week's performance and identify any shipping delays. The report will change depending on the day it is run.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #2. My Plan Before AI.

    Before you ask your agent anything, open the API's address in your browser and read what comes back. Then write how you would solve it: the steps, in order, in plain words, in five lines or more. Then answer these:

    - Which functions will your tool need? For each, what goes in and what comes out?
    - Which addresses will they request?
    - How will you know you have every record?
    - Which check will you use in section 6, and which two numbers should agree?.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **What the API returns**

    From the API results, I found that /shop/orders returns the orders under items. The response also includes a pagination section with page, per_page, total, pages, and has_next, which tells me how many orders there are and whether more pages need to be collected.

    **I would approach the task in the following steps:**

    1. From the API results, I found that /shop/orders returns the orders under items. The response also includes a pagination section with page, per_page, total, pages, and has_next, which tells me how many orders there are and whether more pages need to be collected.

    2. Use date.today() to get today's date. The start date will be today minus six days, and the end date will be today. For example, if I run the report on 28 October 2026, the date range will be 22–28 October 2026.

    3. Request /shop/orders using the start and end dates to retrieve orders placed during that period.

    4. Collect every page of orders by requesting the next page while has_next is true. The current response has total: 37, per_page: 50, and pages: 1, so all 37 orders fit on one page. If the API allows a smaller per_page value, I would also test with a smaller page size to check that the loop correctly collects multiple pages.

    5. Use /shop/orders/{order_id} to retrieve the product lines for each order. The order list already contains order_total_dollars, ship_country, and shipped_date, so I mainly need the second endpoint to get each product's name and quantity.

    6. Calculate the report's results:

    - Order count: Count the orders collected.
    - Total revenue: Add the order_total_dollars values. This excludes freight_dollars.
    - Revenue by country: Use a dictionary to add each order's order_total_dollars to the total for its ship_country.
    - Top five products: Use a dictionary to add up quantity for each product_name across all order lines, then select the five products with the highest totals.
    - Unshipped orders: Identify orders where shipped_date is null. For example, order 15630 has a shipped date, while several orders in the list show null.

    7. Put the results into a report and write one sentence summarizing the week's performance for the operations manager.

    **Which functions will my tool need?**

    - get_orders(from_date, to_date, page) — takes the date range and page number as inputs and returns one page of orders.
    - get_all_orders(from_date, to_date) — calls get_orders repeatedly until has_next is false, then returns all orders for the date range.
    - get_order_details(order_id) — takes an order ID as input and returns the order's details and product lines.
    - build_report(orders, lines) — takes the collected orders and their product lines from get_order_details, and returns the report’s results.

    **Which endpoints will they request?**

    - /shop/orders — retrieves orders for the date range and provides pagination information.
    - /shop/orders/{order_id} — retrieves an individual order's product lines, including product names and quantities.

    **How will I know I have every record?**

    I will compare the number of orders collected across all pages with the API's pagination.total. The numbers should agree. When I ran it on 28 October 2026, both numbers were 37.

    **Which checks will I use in Section 6?**

    I will use two checks:

    1. Order count check: The number of orders collected should equal pagination.total (both were 37 when I ran it on 28 October 2026).
    2. Revenue check: The sum of revenue across all shipping countries should equal the total revenue for the week.

    The first check helps confirm that I collected all the orders, while the second helps confirm that my revenue calculations are consistent.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #3. Inputs.

    Every input in one cell.
    """)
    return


@app.cell
def _():
    days = 7
    per_page = 50
    base_url = "https://oim.zhili.dev"
    return base_url, days, per_page


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #4. The Work.

    Your functions, and the code that uses them.
    """)
    return


@app.cell
def _():
    import requests
    from datetime import date, timedelta

    return date, requests, timedelta


@app.cell
def _(date, days, timedelta):
    end_date = date.today()
    start_date = end_date - timedelta(days=days - 1)
    start_date, end_date
    return end_date, start_date


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Fetch One Page**
    """)
    return


@app.cell
def _(base_url, per_page, requests):
    def get_orders(from_date, to_date, page):
        reply = requests.get(
            f"{base_url}/shop/orders",
            params={
                "from_date": str(from_date),
                "to_date": str(to_date),
                "page": page,
                "per_page": per_page,
            },
            timeout=30,
        )
        reply.raise_for_status()
        return reply.json()

    return (get_orders,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Fetch Every Page**
    """)
    return


@app.cell
def _(get_orders):
    def get_all_orders(from_date, to_date):
        orders = []
        page = 1
        while True:
            data = get_orders(from_date, to_date, page)
            orders.extend(data["items"])
            if not data["pagination"]["has_next"]:
                return orders, data["pagination"]["total"]
            page += 1

    return (get_all_orders,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Fetch One Order's Lines**
    """)
    return


@app.cell
def _(base_url, requests):
    def get_order_details(order_id):
        reply = requests.get(f"{base_url}/shop/orders/{order_id}", timeout=30)
        reply.raise_for_status()
        return reply.json()

    return (get_order_details,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Calculate The Results**
    """)
    return


@app.function
def build_report(orders, lines):
    revenue = 0
    revenue_by_country = {}
    for order in orders:
        total = order["order_total_dollars"]
        country = order["ship_country"]
        revenue = revenue + total
        revenue_by_country[country] = revenue_by_country.get(country, 0) + total

    units_by_product = {}
    for line in lines:
        name = line["product_name"]
        units_by_product[name] = units_by_product.get(name, 0) + line["quantity"]

    top_products = sorted(units_by_product, key=units_by_product.get, reverse=True)[:5]

    unshipped = []
    for order in orders:
        if not order["shipped_date"]:
            unshipped.append(order)

    return {
        "order_count": len(orders),
        "revenue": round(revenue, 2),
        "revenue_by_country": revenue_by_country,
        "top_products": [(name, units_by_product[name]) for name in top_products],
        "unshipped": unshipped,
    }


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Brief Notes

    **.get(country, 0) **returns the running total so far for a country from the dictionary. If it is the first time a country appears, it uses 0 as the starting value.

    **sorted(..., key=units_by_product.get, reverse=True) **orders the product names by how many units of each product were sold, largest first, and **[:5] **keeps the top five.

    **not order["shipped_date"] **is true when the shipped date is null (which becomes None in Python) or an empty string. It checks whether the order has a shipping date. If it doesn't, then the order has not shipped yet.

    The function returns everything as one dictionary, so section 5 can pick out each part.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Use The Functions**

    The functions are used to fetch the orders and their lines, and build the report.
    """)
    return


@app.cell
def _(end_date, get_all_orders, get_order_details, start_date):
    orders, reported_total = get_all_orders(start_date, end_date)

    lines = []
    for _order in orders:
        _details = get_order_details(_order["order_id"])
        lines.extend(_details["lines"])

    report = build_report(orders, lines)
    return orders, report, reported_total


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    First, collect all orders for the date range and get the reported total number of orders.

    Then, go through each order, retrieve its details, and collect its product lines into one list.

    Finally, pass the orders and product lines to **build_report()** to calculate the report results.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #5. The Answer.
    Your result table, printed with print and f-strings with the columns lined up, and one sentence that answers the question in section 1 with the numbers in it. Print the sentence from code with an f-string, so that it changes when the data does.
    """)
    return


@app.cell
def _(days, end_date, report, start_date):
    _countries = sorted(report["revenue_by_country"].items(), key=lambda pair: pair[1], reverse=True)

    print(f"Northwind Traders, {start_date} to {end_date}")
    print(f"Orders: {report['order_count']}    Revenue: ${report['revenue']:,.2f}")
    print()

    print(f"{'Country':<16}{'Revenue ($)':>14}")
    for _country, _rev in _countries:
        print(f"{_country:<16}{_rev:>14,.2f}")
    print()

    print(f"{'Product':<36}{'Units':>8}")
    for _name, _units in report["top_products"]:
        print(f"{_name:<36}{_units:>8}")
    print()

    print(f"{'Order':<8}{'Customer':<36}{'Country':<16}{'Required by':>12}")
    for _o in sorted(report["unshipped"], key=lambda o: o["required_date"]):
        print(f"{_o['order_id']:<8}{_o['customer_name']:<36}{_o['ship_country']:<16}{_o['required_date'][:10]:>12}")
    print()

    _top_name, _top_units = report["top_products"][0]
    _lead_country, _lead_rev = _countries[0]
    print(
        f"In the {days} days from {start_date} to {end_date}, Northwind received "
        f"{report['order_count']} orders worth ${report['revenue']:,.2f}, led by "
        f"{_lead_country} (${_lead_rev:,.2f}); the top seller was {_top_name} "
        f"({_top_units} units), and {len(report['unshipped'])} orders have not shipped yet."
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Brief Notes**

    This code organizes and prints the weekly report. First, it sorts countries by revenue, from highest to lowest. It then prints the date range, total number of orders, total revenue, revenue by country, and the top five products by units sold. Next, it lists unshipped orders, sorting them by required date so that orders due soonest appear first. Finally, it prints a one-sentence summary of the week's results, including the order count, total revenue, leading country, best-selling product, and number of orders that have not shipped yet.

    Why sort the unshipped orders?

    The API returns orders newest first, but the newest orders are not necessarily the most urgent. Sorting by **required_date** puts the orders due soonest at the top, helping the manager see which shipments need attention first.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #6. How I Know These Numbers Are Right.

    Reach at least one result a second way, in this notebook, and show that the two agree. Write a cell that gets the same number from other fields, or open the raw reply in your browser and find each number of one row of your table there. For instance: an average bill is close to the average value times the tax rate divided by 1,000; an order's total equals the sum of its lines; the number of records you collected equals the total the API reports.
    """)
    return


@app.cell
def _(get_order_details, orders, report, reported_total):
    # Check 1: orders collected vs. the API's total
    print(f"Orders collected: {len(orders)}   API total: {reported_total}   "
          f"Agree: {len(orders) == reported_total}")

    # Check 2: revenue by country adds up to total revenue
    _country_sum = round(sum(report["revenue_by_country"].values()), 2)
    print(f"Sum of countries: ${_country_sum:,.2f}   Total revenue: ${report['revenue']:,.2f}   "
          f"Agree: {abs(_country_sum - report['revenue']) < 0.01}")

    # Check 3: one order's total equals the sum of its lines
    _check = get_order_details(orders[0]["order_id"])
    _line_sum = round(sum(line["line_total_dollars"] for line in _check["lines"]), 2)
    print(f"Order {_check['order_id']}: total ${_check['order_total_dollars']:,.2f}   "
          f"sum of lines ${_line_sum:,.2f}   "
          f"Agree: {abs(_line_sum - _check['order_total_dollars']) < 0.01}")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Brief Notes**

    Check 1 confirms the pagination loop collected every order.

    Check 2 confirms the revenue calculations are consistent: adding up the countries gives back the total.
    Check 3 reaches a number a second way, using a different source: the order’s total from the API against the sum of its individual lines. This is one of the brief’s own examples.

    abs(a - b) < 0.01 counts two amounts as equal when they’re less than a cent apart, because rounding can leave tiny differences.

    When I ran the report on 28 October 2026, all three checks passed. First, the number of orders collected was 37, which matched the API's reported total of 37. Second, the revenue by country added up to $919,557.03, matching the total revenue of $919,557.03. Third, order 20700 had an order total of $45,714.84, which matched the sum of its individual product lines at $45,714.84. Order 20700 also had $327.75 in freight, so the match confirms that order_total_dollars excludes freight.

    Since all three checks agree, this gives me confidence that I collected all the orders and that the revenue calculations are consistent with the API data.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #7. Working With the Agent.

    Pick one piece of AI output you did not accept as-is. What did it give you, what did you change, and how did you know? Point to the commit or the cell. If the agent got it right the first time: What did you do to verify that? Pointing to your check in section 6 is enough.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #8. Reading It Back.

    Pick two functions in your notebook that your agent wrote or helped write. For each, write in your own words what goes in, what comes out, and one line you had to ask about. Then choose one change to what the tool does, such as another county, another week or another rule. Changing one value in your Inputs cell is enough. Write what you expect to change in the answer. Commit with the message mp2: prediction, make the change, run it, and write what happened and whether it matched.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #9. Going Further.
    What you tried past the main task, what you found, and where it is in the notebook.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #10. Time Spent.
    About how many hours this project took you outside class, as one number. It is not graded.
    """)
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
