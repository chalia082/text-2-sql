# Add a comment at the top to encourage using joins
# If a column is not present in a table, but can be obtained by joining related tables, use the appropriate join to get the desired output.

class FewShotPrompt:
    """Class containing few-shot SQL generation prompt."""

    def __init__(self):
        self.examples = [
            {
                'question': 'Find customers who have made payments on more than one loan.',
                'sql': (
                    "SELECT l.customer_id "
                    "FROM loan_payments lp "
                    "JOIN loans l ON lp.loan_id = l.loan_id "
                    "GROUP BY l.customer_id "
                    "HAVING COUNT(DISTINCT lp.loan_id) > 1;"
                )
            },
            {
                'question': 'List the total payment amount for each customer who has made a loan payment.',
                'sql': (
                    "SELECT l.customer_id, SUM(lp.amount) AS total_paid "
                    "FROM loan_payments lp "
                    "JOIN loans l ON lp.loan_id = l.loan_id "
                    "GROUP BY l.customer_id;"
                )
            },
            {
                'question': 'Find the email addresses of customers who have made a payment on a loan.',
                'sql': (
                    "SELECT DISTINCT c.email "
                    "FROM loan_payments lp "
                    "JOIN loans l ON lp.loan_id = l.loan_id "
                    "JOIN customers c ON l.customer_id = c.customer_id;"
                )
            },
            # ✅ Simple Examples
            {
                'question': 'List all customers and their phone numbers.',
                'sql': "SELECT customer_id, first_name, last_name, phone_number FROM customers;"
            },
            {
                'question': 'What are the names and types of all accounts?',
                'sql': "SELECT a.account_id, at.account_type_name FROM accounts a JOIN account_types at ON a.account_type_id = at.account_type_id;"
            },
            {
                'question': 'Show all employees working in each branch.',
                'sql': "SELECT e.employee_id, e.name, b.branch_name FROM employees e JOIN branches b ON e.branch_id = b.branch_id;"
            },
            {
                'question': 'How many loan types are available?',
                'sql': "SELECT COUNT(*) FROM loan_types;"
            },
            {
                'question': 'List all transactions made on a specific date.',
                'sql': "SELECT * FROM transactions WHERE transaction_date = '2023-01-01';"
            },
            {
                'question': 'Show the names of all branches.',
                'sql': "SELECT branch_name FROM branches;"
            },
            {
                'question': 'What is the total number of ATM withdrawals?',
                'sql': "SELECT COUNT(*) AS total_withdrawals FROM atm_withdrawals;"
            },
            {
                'question': 'Get a list of all credit cards issued.',
                'sql': "SELECT * FROM credit_cards;"
            },
            {
                'question': 'Show all customers who live in New York.',
                'sql': "SELECT * FROM customers WHERE city = 'New York';"
            },
            {
                'question': 'What are the names and addresses of all branches?',
                'sql': "SELECT branch_name, address FROM branches;"
            },

            # ✅ Mid-Level Examples
            {
                'question': 'List all accounts with their current balances and account types.',
                'sql': "SELECT a.account_id, a.balance, at.account_type_name FROM accounts a JOIN account_types at ON a.account_type_id = at.account_type_id;"
            },
            {
                'question': 'Show customers along with the number of accounts they hold.',
                'sql': "SELECT c.customer_id, c.first_name, c.last_name, COUNT(a.account_id) AS num_accounts FROM customers c JOIN accounts a ON c.customer_id = a.customer_id GROUP BY c.customer_id, c.first_name, c.last_name;"
            },
            {
                'question': 'Which employees work in each branch?',
                'sql': "SELECT e.employee_id, e.name, b.branch_name FROM employees e JOIN branches b ON e.branch_id = b.branch_id;"
            },
            {
                'question': 'What is the total balance held in each branch?',
                'sql': "SELECT b.branch_name, SUM(a.balance) AS total_balance FROM branches b JOIN accounts a ON b.branch_id = a.branch_id GROUP BY b.branch_name;"
            },
            {
                'question': 'Find the number of loans per loan type.',
                'sql': "SELECT lt.loan_type, COUNT(l.loan_id) AS num_loans FROM loan_types lt LEFT JOIN loans l ON lt.loan_type_id = l.loan_type_id GROUP BY lt.loan_type;"
            },
            {
                'question': 'List customers who have both an account and a loan.',
                'sql': "SELECT DISTINCT c.customer_id, c.first_name, c.last_name FROM customers c JOIN accounts a ON c.customer_id = a.customer_id JOIN loans l ON c.customer_id = l.customer_id;"
            },
            {
                'question': 'Show the total number of credit card transactions per customer.',
                'sql': "SELECT cc.customer_id, COUNT(ct.transaction_id) AS total_transactions FROM credit_cards cc JOIN card_transactions ct ON cc.card_id = ct.card_id GROUP BY cc.customer_id;"
            },
            {
                'question': 'List customers with more than 2 credit cards.',
                'sql': "SELECT customer_id FROM credit_cards GROUP BY customer_id HAVING COUNT(*) > 2;"
            },
            {
                'question': 'Find employees hired before 2020.',
                'sql': "SELECT employee_id, name FROM employees WHERE hire_date < '2020-01-01';"
            },
            {
                'question': 'Which branches have more than 5 employees?',
                'sql': "SELECT b.branch_name, COUNT(e.employee_id) AS num_employees FROM branches b JOIN employees e ON b.branch_id = e.branch_id GROUP BY b.branch_name HAVING COUNT(e.employee_id) > 5;"
            },

            # ✅ Complex Examples
            {
                'question': 'List customers who have opened an account, received a credit card, and taken a loan all within 3 months.',
                'sql': (
                    "SELECT DISTINCT c.customer_id, c.first_name, c.last_name "
                    "FROM customers c "
                    "JOIN accounts a ON c.customer_id = a.customer_id "
                    "JOIN credit_cards cc ON c.customer_id = cc.customer_id "
                    "JOIN loans l ON c.customer_id = l.customer_id "
                    "WHERE ABS(DATE_PART('day', a.open_date::timestamp - cc.issue_date::timestamp)) <= 90 "
                    "AND ABS(DATE_PART('day', a.open_date::timestamp - l.issue_date::timestamp)) <= 90;"
                )
            },
            {
                'question': "Show each employee's branch and total number of accounts at their branch.",
                'sql': (
                    "SELECT e.employee_id, e.name, b.branch_name, COUNT(a.account_id) AS total_accounts "
                    "FROM employees e "
                    "JOIN branches b ON e.branch_id = b.branch_id "
                    "JOIN accounts a ON b.branch_id = a.branch_id "
                    "GROUP BY e.employee_id, e.name, b.branch_name;"
                )
            },
            {
                'question': "Find each branch's average account balance and number of customers served.",
                'sql': (
                    "SELECT b.branch_name, AVG(a.balance) AS avg_balance, COUNT(DISTINCT a.customer_id) AS num_customers "
                    "FROM branches b "
                    "JOIN accounts a ON b.branch_id = a.branch_id "
                    "GROUP BY b.branch_name;"
                )
            },
            {
                'question': 'Show loans that are overdue (due_date < today).',
                'sql': "SELECT loan_id, customer_id, amount FROM loans WHERE due_date < CURRENT_DATE AND status != 'Closed';"
            },
            {
                'question': 'Identify customers who have made the highest number of ATM withdrawals this year.',
                'sql': (
                    "SELECT a.customer_id, COUNT(*) AS withdrawal_count "
                    "FROM atm_withdrawals aw "
                    "JOIN accounts a ON aw.account_id = a.account_id "
                    "WHERE EXTRACT(YEAR FROM aw.withdrawal_date) = EXTRACT(YEAR FROM CURRENT_DATE) "
                    "GROUP BY a.customer_id "
                    "ORDER BY withdrawal_count DESC "
                    "LIMIT 5;"
                )
            },
            {
                'question': 'Find the top 5 credit cards with the highest average transaction amount.',
                'sql': (
                    "SELECT ct.card_id, AVG(ct.amount) AS avg_amount "
                    "FROM card_transactions ct "
                    "GROUP BY ct.card_id "
                    "ORDER BY avg_amount DESC "
                    "LIMIT 5;"
                )
            },
            {
                'question': 'Find customers who have made payments on more than one loan.',
                'sql': (
                    "SELECT l.customer_id "
                    "FROM loan_payments lp "
                    "JOIN loans l ON lp.loan_id = l.loan_id "
                    "GROUP BY l.customer_id "
                    "HAVING COUNT(DISTINCT lp.loan_id) > 1;"
                )
            },
            {
                'question': 'List the total payment amount for each customer who has made a loan payment.',
                'sql': (
                    "SELECT l.customer_id, SUM(lp.amount) AS total_paid "
                    "FROM loan_payments lp "
                    "JOIN loans l ON lp.loan_id = l.loan_id "
                    "GROUP BY l.customer_id;"
                )
            },
            {
                'question': 'Find the email addresses of customers who have made a payment on a loan.',
                'sql': (
                    "SELECT DISTINCT c.email "
                    "FROM loan_payments lp "
                    "JOIN loans l ON lp.loan_id = l.loan_id "
                    "JOIN customers c ON l.customer_id = c.customer_id;"
                )
            },
            {
                'question': 'Show each branch’s performance: number of employees, accounts, and total loan amount.',
                'sql': (
                    "SELECT b.branch_name, "
                    "COUNT(DISTINCT e.employee_id) AS num_employees, "
                    "COUNT(DISTINCT a.account_id) AS num_accounts, "
                    "SUM(l.amount) AS total_loans "
                    "FROM branches b "
                    "LEFT JOIN employees e ON b.branch_id = e.branch_id "
                    "LEFT JOIN accounts a ON b.branch_id = a.branch_id "
                    "LEFT JOIN loans l ON a.customer_id = l.customer_id "
                    "GROUP BY b.branch_name;"
                )
            },
            {
                'question': 'Find customers with both a loan and a credit card, and their total loan amount (using a CTE).',
                'sql': (
                    "WITH customer_loans AS (SELECT customer_id, SUM(amount) AS total_loan_amount FROM loans GROUP BY customer_id), "
                    "customer_cards AS (SELECT customer_id FROM credit_cards GROUP BY customer_id) "
                    "SELECT c.customer_id, c.first_name, c.last_name, cl.total_loan_amount "
                    "FROM customers c "
                    "JOIN customer_loans cl ON c.customer_id = cl.customer_id "
                    "JOIN customer_cards cc ON c.customer_id = cc.customer_id;"
                )
            },
            {
                'question': 'Find the top 3 customers with the highest total loan amount and show their total number of accounts.',
                'sql': (
                    "SELECT c.customer_id, c.first_name, c.last_name, SUM(l.amount) AS total_loan_amount, COUNT(DISTINCT a.account_id) AS num_accounts "
                    "FROM customers c "
                    "JOIN loans l ON c.customer_id = l.customer_id "
                    "LEFT JOIN accounts a ON c.customer_id = a.customer_id "
                    "GROUP BY c.customer_id, c.first_name, c.last_name "
                    "ORDER BY total_loan_amount DESC "
                    "LIMIT 3;"
                )
            },
            {
                'question': 'For each branch, show the month with the highest number of new accounts opened in the last year.',
                'sql': (
                    "WITH monthly_accounts AS ( "
                    "  SELECT b.branch_name, DATE_TRUNC('month', a.open_date) AS month, COUNT(*) AS num_accounts "
                    "  FROM branches b "
                    "  JOIN accounts a ON b.branch_id = a.branch_id "
                    "  WHERE a.open_date >= (CURRENT_DATE - INTERVAL '1 year') "
                    "  GROUP BY b.branch_name, DATE_TRUNC('month', a.open_date) "
                    ") "
                    "SELECT branch_name, month, num_accounts "
                    "FROM ( "
                    "  SELECT branch_name, month, num_accounts, "
                    "         ROW_NUMBER() OVER (PARTITION BY branch_name ORDER BY num_accounts DESC) AS rn "
                    "  FROM monthly_accounts "
                    ") ranked "
                    "WHERE rn = 1;"
                )
            },
            {
                'question': 'List customers who have never made a loan payment late (i.e., all their payments were on or before the due date).',
                'sql': (
                    "SELECT DISTINCT c.customer_id, c.first_name, c.last_name "
                    "FROM customers c "
                    "JOIN loans l ON c.customer_id = l.customer_id "
                    "JOIN loan_payments lp ON l.loan_id = lp.loan_id "
                    "GROUP BY c.customer_id, c.first_name, c.last_name "
                    "HAVING SUM(CASE WHEN lp.payment_date > lp.due_date THEN 1 ELSE 0 END) = 0;"
                )
            },
            {
                'question': 'Find the average, minimum, and maximum account balance for each account type, and show only those account types where the maximum balance exceeds $50,000.',
                'sql': (
                    "SELECT at.account_type_name, AVG(a.balance) AS avg_balance, MIN(a.balance) AS min_balance, MAX(a.balance) AS max_balance "
                    "FROM account_types at "
                    "JOIN accounts a ON at.account_type_id = a.account_type_id "
                    "GROUP BY at.account_type_name "
                    "HAVING MAX(a.balance) > 50000;"
                )
            },
            {
                'question': 'For each customer, show their most recent transaction (by date) and the transaction amount.',
                'sql': (
                    "SELECT t.customer_id, t.transaction_id, t.transaction_date, t.amount "
                    "FROM transactions t "
                    "JOIN ( "
                    "  SELECT customer_id, MAX(transaction_date) AS max_date "
                    "  FROM transactions "
                    "  GROUP BY customer_id "
                    ") latest ON t.customer_id = latest.customer_id AND t.transaction_date = latest.max_date;"
                )
            },
            {
                'question': 'Show the month-over-month growth rate in the number of new loans issued for the past 6 months.',
                'sql': (
                    "WITH monthly_loans AS ( "
                    "  SELECT DATE_TRUNC('month', issue_date) AS month, COUNT(*) AS num_loans "
                    "  FROM loans "
                    "  WHERE issue_date >= (CURRENT_DATE - INTERVAL '6 months') "
                    "  GROUP BY DATE_TRUNC('month', issue_date) "
                    ") "
                    "SELECT month, num_loans, "
                    "       LAG(num_loans) OVER (ORDER BY month) AS prev_month_loans, "
                    "       ROUND(100.0 * (num_loans - LAG(num_loans) OVER (ORDER BY month)) / NULLIF(LAG(num_loans) OVER (ORDER BY month), 0), 2) AS growth_rate_percent "
                    "FROM monthly_loans "
                    "ORDER BY month;"
                )
            },
            {
                'question': 'Find customers who have both a loan and a credit card, but have never had an account with a negative balance.',
                'sql': (
                    "WITH has_loan AS (SELECT DISTINCT customer_id FROM loans), "
                    "     has_card AS (SELECT DISTINCT customer_id FROM credit_cards), "
                    "     never_negative AS ( "
                    "       SELECT a.customer_id FROM accounts a "
                    "       GROUP BY a.customer_id "
                    "       HAVING MIN(a.balance) >= 0 "
                    "     ) "
                    "SELECT c.customer_id, c.first_name, c.last_name "
                    "FROM customers c "
                    "JOIN has_loan l ON c.customer_id = l.customer_id "
                    "JOIN has_card cc ON c.customer_id = cc.customer_id "
                    "JOIN never_negative nn ON c.customer_id = nn.customer_id;"
                )
            },
            {
                'question': 'Find the average loan amount and total interest paid for each loan type.',
                'sql': (
                    "SELECT lt.loan_type, AVG(l.amount) AS avg_loan_amount, SUM(lp.interest_amount) AS total_interest_paid "
                    "FROM loan_types lt "
                    "JOIN loans l ON lt.loan_type_id = l.loan_type_id "
                    "JOIN loan_payments lp ON l.loan_id = lp.loan_id "
                    "GROUP BY lt.loan_type;"
                )
            },
            {
                'question': 'Show all loans that are overdue (past their due date).',
                'sql': (
                    "SELECT loan_id, customer_id, amount "
                    "FROM loans "
                    "WHERE (start_date + INTERVAL '1 month' * term_months) < CURRENT_DATE "
                    "AND status != 'Closed';"
                )
            },
            {
                'question': 'Find customers whose loans will be due in the next 30 days.',
                'sql': (
                    "SELECT l.loan_id, l.customer_id, l.amount, (l.start_date + INTERVAL '1 month' * l.term_months) AS due_date "
                    "FROM loans l "
                    "WHERE (l.start_date + INTERVAL '1 month' * l.term_months) BETWEEN CURRENT_DATE AND (CURRENT_DATE + INTERVAL '30 days');"
                )
            },
            {
                'question': 'List all loans with their due date and the number of payments made.',
                'sql': (
                    "SELECT l.loan_id, l.customer_id, l.amount, (l.start_date + INTERVAL '1 month' * l.term_months) AS due_date, "
                    "       COUNT(lp.payment_id) AS num_payments "
                    "FROM loans l "
                    "LEFT JOIN loan_payments lp ON l.loan_id = lp.loan_id "
                    "GROUP BY l.loan_id, l.customer_id, l.amount, l.start_date, l.term_months;"
                )
            },
            {
                'question': 'Show loans that are overdue and have had no payment in the last 60 days.',
                'sql': (
                    "SELECT l.loan_id, l.customer_id, l.amount "
                    "FROM loans l "
                    "WHERE (l.start_date + INTERVAL '1 month' * l.term_months) < CURRENT_DATE "
                    "AND NOT EXISTS ( "
                    "    SELECT 1 FROM loan_payments lp "
                    "    WHERE lp.loan_id = l.loan_id "
                    "    AND lp.payment_date >= (CURRENT_DATE - INTERVAL '60 days') "
                    ");"
                )
            },
            {
                'question': 'Find customers who have made at least one late loan payment.',
                'sql': (
                    "SELECT DISTINCT c.customer_id, c.first_name, c.last_name "
                    "FROM customers c "
                    "JOIN loans l ON c.customer_id = l.customer_id "
                    "JOIN loan_payments lp ON l.loan_id = lp.loan_id "
                    "WHERE lp.payment_date > lp.due_date;"
                )
            },
            {
                'question': 'Identify loans that were paid off early (last payment before due date).',
                'sql': (
                    "SELECT l.loan_id, l.customer_id, MAX(lp.payment_date) AS last_payment_date, "
                    "       (l.start_date + INTERVAL '1 month' * l.term_months) AS due_date "
                    "FROM loans l "
                    "JOIN loan_payments lp ON l.loan_id = lp.loan_id "
                    "GROUP BY l.loan_id, l.customer_id, l.start_date, l.term_months "
                    "HAVING MAX(lp.payment_date) < (l.start_date + INTERVAL '1 month' * l.term_months);"
                )
            },
            {
                'question': 'Find customers whose loan amounts have increased over time (i.e., each new loan is larger than the previous).',
                'sql': (
                    "SELECT customer_id "
                    "FROM ( "
                    "  SELECT customer_id, amount, "
                    "         LAG(amount) OVER (PARTITION BY customer_id ORDER BY start_date) AS prev_amount "
                    "  FROM loans "
                    ") t "
                    "WHERE prev_amount IS NOT NULL AND amount > prev_amount;"
                )
            },
            {
                'question': 'Which branch has the highest loan default rate?',
                'sql': (
                    "SELECT b.branch_name, "
                    "       COUNT(CASE WHEN l.status = 'Defaulted' THEN 1 END)::float / COUNT(*) AS default_rate "
                    "FROM branches b "
                    "JOIN accounts a ON b.branch_id = a.branch_id "
                    "JOIN loans l ON a.account_id = l.account_id "
                    "GROUP BY b.branch_name "
                    "ORDER BY default_rate DESC "
                    "LIMIT 1;"
                )
            },
            {
                'question': 'List customers who have never missed a loan payment.',
                'sql': (
                    "SELECT DISTINCT c.customer_id, c.first_name, c.last_name "
                    "FROM customers c "
                    "JOIN loans l ON c.customer_id = l.customer_id "
                    "JOIN loan_payments lp ON l.loan_id = lp.loan_id "
                    "GROUP BY c.customer_id, c.first_name, c.last_name "
                    "HAVING SUM(CASE WHEN lp.status = 'missed' THEN 1 ELSE 0 END) = 0;"
                )
            },
            # --- AGGREGATE DIFFERENCE/COMBINATION EXAMPLES ---
            {
                'question': 'Show customers with the highest difference between account balance and total loan.',
                'sql': (
                    "WITH customer_balances AS ("
                    "  SELECT customer_id, SUM(balance) AS total_balance "
                    "  FROM accounts "
                    "  GROUP BY customer_id"
                    "), "
                    "customer_loans AS ("
                    "  SELECT customer_id, SUM(amount) AS total_loan "
                    "  FROM loans "
                    "  GROUP BY customer_id"
                    ") "
                    "SELECT c.customer_id, c.first_name, c.last_name, "
                    "       ABS(cb.total_balance - cl.total_loan) AS balance_loan_difference "
                    "FROM customers c "
                    "LEFT JOIN customer_balances cb ON c.customer_id = cb.customer_id "
                    "LEFT JOIN customer_loans cl ON c.customer_id = cl.customer_id "
                    "ORDER BY balance_loan_difference DESC;"
                )
            },
            {
                'question': 'Show employees with the highest difference between total loans issued and total loan payments received.',
                'sql': (
                    "WITH employee_loans AS ("
                    "  SELECT issued_by_employee_id, SUM(amount) AS total_issued "
                    "  FROM loans "
                    "  GROUP BY issued_by_employee_id"
                    "), "
                    "employee_payments AS ("
                    "  SELECT l.issued_by_employee_id, SUM(lp.amount) AS total_payments "
                    "  FROM loan_payments lp "
                    "  JOIN loans l ON lp.loan_id = l.loan_id "
                    "  GROUP BY l.issued_by_employee_id"
                    ") "
                    "SELECT e.employee_id, e.name, "
                    "       ABS(el.total_issued - ep.total_payments) AS issued_payment_difference "
                    "FROM employees e "
                    "LEFT JOIN employee_loans el ON e.employee_id = el.issued_by_employee_id "
                    "LEFT JOIN employee_payments ep ON e.employee_id = ep.issued_by_employee_id "
                    "ORDER BY issued_payment_difference DESC;"
                )
            },
            {
                'question': 'Show branches with the largest difference between total deposits and total withdrawals.',
                'sql': (
                    "WITH branch_deposits AS ("
                    "  SELECT a.branch_id, SUM(t.amount) AS total_deposits "
                    "  FROM transactions t "
                    "  JOIN accounts a ON t.account_id = a.account_id "
                    "  WHERE t.txn_type = 'deposit' "
                    "  GROUP BY a.branch_id"
                    "), "
                    "branch_withdrawals AS ("
                    "  SELECT a.branch_id, SUM(t.amount) AS total_withdrawals "
                    "  FROM transactions t "
                    "  JOIN accounts a ON t.account_id = a.account_id "
                    "  WHERE t.txn_type = 'withdrawal' "
                    "  GROUP BY a.branch_id"
                    ") "
                    "SELECT b.branch_id, b.branch_name, "
                    "       ABS(bd.total_deposits - bw.total_withdrawals) AS deposit_withdrawal_difference "
                    "FROM branches b "
                    "LEFT JOIN branch_deposits bd ON b.branch_id = bd.branch_id "
                    "LEFT JOIN branch_withdrawals bw ON b.branch_id = bw.branch_id "
                    "ORDER BY deposit_withdrawal_difference DESC;"
                )
            },
            {
                'question': 'Show customers whose total payments exceed their total loan amount.',
                'sql': (
                    "WITH customer_payments AS ("
                    "  SELECT l.customer_id, SUM(lp.amount) AS total_payments "
                    "  FROM loan_payments lp "
                    "  JOIN loans l ON lp.loan_id = l.loan_id "
                    "  GROUP BY l.customer_id"
                    "), "
                    "customer_loans AS ("
                    "  SELECT customer_id, SUM(amount) AS total_loan "
                    "  FROM loans "
                    "  GROUP BY customer_id"
                    ") "
                    "SELECT c.customer_id, c.first_name, c.last_name "
                    "FROM customers c "
                    "JOIN customer_payments cp ON c.customer_id = cp.customer_id "
                    "JOIN customer_loans cl ON c.customer_id = cl.customer_id "
                    "WHERE cp.total_payments > cl.total_loan;"
                )
            },
            # --- LOAN PAYOFF TIMING EXAMPLES ---
            {
                'question': 'Identify all customers who paid off their loans early.',
                'sql': (
                    "WITH loan_payoff AS ("
                    "  SELECT l.loan_id, l.customer_id, l.start_date, l.term_months, l.amount, "
                    "         MAX(lp.payment_date) AS last_payment_date, SUM(lp.amount) AS total_paid "
                    "  FROM loans l "
                    "  JOIN loan_payments lp ON l.loan_id = lp.loan_id "
                    "  GROUP BY l.loan_id, l.customer_id, l.start_date, l.term_months, l.amount"
                    ") "
                    "SELECT DISTINCT c.customer_id, c.first_name, c.last_name "
                    "FROM customers c "
                    "JOIN loan_payoff p ON c.customer_id = p.customer_id "
                    "WHERE p.total_paid >= p.amount "
                    "  AND p.last_payment_date < (p.start_date + INTERVAL '1 month' * p.term_months);"
                )
            },
            {
                'question': 'Identify all customers who paid off their loans late.',
                'sql': (
                    "WITH loan_payoff AS ("
                    "  SELECT l.loan_id, l.customer_id, l.start_date, l.term_months, l.amount, "
                    "         MAX(lp.payment_date) AS last_payment_date, SUM(lp.amount) AS total_paid "
                    "  FROM loans l "
                    "  JOIN loan_payments lp ON l.loan_id = lp.loan_id "
                    "  GROUP BY l.loan_id, l.customer_id, l.start_date, l.term_months, l.amount"
                    ") "
                    "SELECT DISTINCT c.customer_id, c.first_name, c.last_name "
                    "FROM customers c "
                    "JOIN loan_payoff p ON c.customer_id = p.customer_id "
                    "WHERE p.total_paid >= p.amount "
                    "  AND p.last_payment_date > (p.start_date + INTERVAL '1 month' * p.term_months);"
                )
            },
            {
                'question': 'List all loans that are fully paid off.',
                'sql': (
                    "WITH loan_payoff AS ("
                    "  SELECT l.loan_id, l.amount, SUM(lp.amount) AS total_paid "
                    "  FROM loans l "
                    "  JOIN loan_payments lp ON l.loan_id = lp.loan_id "
                    "  GROUP BY l.loan_id, l.amount"
                    ") "
                    "SELECT loan_id, amount, total_paid "
                    "FROM loan_payoff "
                    "WHERE total_paid >= amount;"
                )
            },
            {
                'question': 'List all loans that are not yet fully paid off.',
                'sql': (
                    "WITH loan_payoff AS ("
                    "  SELECT l.loan_id, l.amount, SUM(lp.amount) AS total_paid "
                    "  FROM loans l "
                    "  LEFT JOIN loan_payments lp ON l.loan_id = lp.loan_id "
                    "  GROUP BY l.loan_id, l.amount"
                    ") "
                    "SELECT loan_id, amount, total_paid "
                    "FROM loan_payoff "
                    "WHERE total_paid < amount OR total_paid IS NULL;"
                )
            },
            # --- CUSTOMER ACTIVITY AGGREGATION EXAMPLES ---
            {
                'question': 'List the most active customers based on total transaction and withdrawal count.',
                'sql': (
                    "WITH customer_accounts AS ("
                    "  SELECT customer_id, account_id FROM accounts"
                    "), "
                    "transactions_count AS ("
                    "  SELECT a.customer_id, COUNT(t.txn_id) AS total_transactions "
                    "  FROM customer_accounts a "
                    "  LEFT JOIN transactions t ON a.account_id = t.account_id "
                    "  GROUP BY a.customer_id"
                    "), "
                    "withdrawals_count AS ("
                    "  SELECT a.customer_id, COUNT(w.withdrawal_id) AS total_withdrawals "
                    "  FROM customer_accounts a "
                    "  LEFT JOIN atm_withdrawals w ON a.account_id = w.account_id "
                    "  GROUP BY a.customer_id"
                    ") "
                    "SELECT c.customer_id, c.first_name, c.last_name, "
                    "       COALESCE(tc.total_transactions, 0) + COALESCE(wc.total_withdrawals, 0) AS total_activity_count "
                    "FROM customers c "
                    "LEFT JOIN transactions_count tc ON c.customer_id = tc.customer_id "
                    "LEFT JOIN withdrawals_count wc ON c.customer_id = wc.customer_id "
                    "ORDER BY total_activity_count DESC;"
                )
            },
            {
                'question': 'Find customers with the highest number of ATM withdrawals and transactions separately.',
                'sql': (
                    "WITH customer_accounts AS ("
                    "  SELECT customer_id, account_id FROM accounts"
                    "), "
                    "transactions_count AS ("
                    "  SELECT a.customer_id, COUNT(t.txn_id) AS total_transactions "
                    "  FROM customer_accounts a "
                    "  LEFT JOIN transactions t ON a.account_id = t.account_id "
                    "  GROUP BY a.customer_id"
                    "), "
                    "withdrawals_count AS ("
                    "  SELECT a.customer_id, COUNT(w.withdrawal_id) AS total_withdrawals "
                    "  FROM customer_accounts a "
                    "  LEFT JOIN atm_withdrawals w ON a.account_id = w.account_id "
                    "  GROUP BY a.customer_id"
                    ") "
                    "SELECT c.customer_id, c.first_name, c.last_name, "
                    "       COALESCE(tc.total_transactions, 0) AS total_transactions, "
                    "       COALESCE(wc.total_withdrawals, 0) AS total_withdrawals "
                    "FROM customers c "
                    "LEFT JOIN transactions_count tc ON c.customer_id = tc.customer_id "
                    "LEFT JOIN withdrawals_count wc ON c.customer_id = wc.customer_id "
                    "ORDER BY total_transactions DESC, total_withdrawals DESC;"
                )
            }
        ]

    def get_prompt(self, user_question: str) -> str:
        examples_text = "\n\n---\n\n".join(
            f"Q: {ex['question']}\nA: {ex['sql']}" for ex in self.examples
        )
        return (
            "You are a top-tier SQL generation assistant for a banking database.\n"
            "Your job is to translate natural language questions into syntactically correct and efficient SQL queries.\n\n"
            "You must ONLY generate SELECT statements or read-only queries — never use INSERT, UPDATE, DELETE, DROP, etc.\n\n"
            "Use these few-shot examples as guidance:\n\n"
            f"{examples_text}\n\n---\n\nQ: {user_question}\nA:"
        )
