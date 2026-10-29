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


if __name__ == "__main__":
    app.run()
