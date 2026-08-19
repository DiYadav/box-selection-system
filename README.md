# Box Selector — AI-Assisted Box Selection System

A small Django + Django REST Framework application that recommends the cheapest shipping box that can safely hold all items in an order.

This project was built for the **Python/Django Hiring Assignment: AI-Assisted Box Selection System**.

The system considers:

- Product dimensions
- Product weight
- Box internal dimensions
- Box maximum weight capacity
- Box cost
- Item rotation
- Total item volume
- Packing efficiency

---

## Problem Statement

When a customer places an order, the warehouse team needs to know which shipping box should be used.

Each product has physical dimensions and weight, while each available box has internal dimensions, maximum weight capacity, and cost.

The system evaluates the available boxes and recommends the **cheapest feasible box** that can safely contain the order.

If multiple boxes have the same cost, the box with the smaller internal volume is selected.

If no box can safely contain the order, the system returns an explanation of why the candidate boxes were rejected.

---

## Tech Stack

- Python
- Django
- Django REST Framework
- SQLite
- pytest
- pytest-django

---

## Features

- Product catalogue
- Box catalogue
- Order and order-item management
- Quantity expansion into individual physical items
- Rotation-aware dimension checking
- Weight capacity validation
- Volume capacity validation
- Configurable packing efficiency
- Cheapest feasible box selection
- Smaller-volume tie-breaking for equal-cost boxes
- Detailed no-suitable-box errors
- Stateless box recommendation endpoint
- Cached recommendation on orders
- Recalculation of an existing order's recommendation
- Automated unit, order-flow, and API tests
- GitHub Actions test workflow

---

# Project Setup
## 1. Clone the repository

```bash
1. git clone https://github.com/DiYadav/box-selection-system
   cd box-selection-system


2. Create a virtual environment

python -m venv venv
venv\Scripts\activate

Linux / macOS
python3 -m venv venv
source venv/bin/activate

3. Install dependencies
pip install -r requirements.txt

4. Apply database migrations
python manage.py migrate

6. Run the development server
python manage.py runserver

7.Run all test cases in terminal
pytest -v
