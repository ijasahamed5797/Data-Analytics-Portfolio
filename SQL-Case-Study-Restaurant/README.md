# Restaurant Sales Analysis - SQL Case Study

## Project Overview
This case study analyzes customer behavior, sales patterns, and membership insights for a restaurant using SQL queries. The analysis covers customer spending, visit frequency, product popularity, and membership impact.

## Business Questions Analyzed

1. **Total amount spent by each customer**
2. **Number of days each customer visited**
3. **First item purchased by each customer**
4. **Most purchased menu item overall**
5. **Most popular item for each customer**
6. **First item purchased after becoming a member**
7. **Last item purchased before becoming a member**
8. **Total items and amount spent before membership**
9. **Customer loyalty points calculation**

## Database Schema
- **sales** - Customer orders with product_id and order_date
- **menu** - Product details with prices
- **members** - Customer membership information

## SQL Skills Demonstrated
- Complex JOIN operations
- Window Functions (ROW_NUMBER, RANK)
- Aggregate Functions with GROUP BY
- Conditional logic with CASE statements
- Subqueries and CTEs
- Data filtering and sorting

## Files
- `restaurant_case_study.sql` - Complete SQL analysis
- `database_schema.sql` - Database setup script

## How to Run
1. Execute `database_schema.sql` to create the database
2. Run `restaurant_case_study.sql` to see the analysis
3. Modify queries to explore additional insights
