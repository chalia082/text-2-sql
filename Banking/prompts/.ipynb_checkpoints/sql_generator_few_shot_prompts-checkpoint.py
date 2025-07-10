class FewShotPrompt:
    """Class containing few-shot SQL generation prompt."""

    def __init__(self):
        self.examples = [
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
                'sql': "SELECT lt.loan_type_name, COUNT(l.loan_id) AS num_loans FROM loan_types lt LEFT JOIN loans l ON lt.loan_type_id = l.loan_type_id GROUP BY lt.loan_type_name;"
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
                    "WHERE ABS(DATE_PART('day', a.open_date::timestamp - cc.expiry_date::timestamp)) <= 90 "
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
