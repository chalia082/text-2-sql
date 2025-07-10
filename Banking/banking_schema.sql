-- Table: account_types
CREATE TABLE account_types (
    account_type_id INTEGER PRIMARY KEY,
    account_type VARCHAR(50)
);

-- Table: loan_types
CREATE TABLE loan_types (
    loan_type_id INTEGER PRIMARY KEY,
    loan_type VARCHAR(50)
);

-- Table: branches
CREATE TABLE branches (
    branch_id INTEGER PRIMARY KEY,
    branch_name VARCHAR(100),
    city VARCHAR(100),
    state VARCHAR(100),
    manager_name VARCHAR(100),
    open_date DATE
);

-- Table: customers
CREATE TABLE customers (
    customer_id INTEGER PRIMARY KEY,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    email VARCHAR(100),
    phone VARCHAR(50),
    dob DATE,
    region VARCHAR(100),
    address TEXT
);

-- Table: employees
CREATE TABLE employees (
    employee_id INTEGER PRIMARY KEY,
    branch_id INTEGER,
    name VARCHAR(100),
    email VARCHAR(100),
    phone VARCHAR(50),
    role VARCHAR(50),
    FOREIGN KEY (branch_id) REFERENCES branches(branch_id)
);

-- Table: accounts
CREATE TABLE accounts (
    account_id INTEGER PRIMARY KEY,
    customer_id INTEGER,
    branch_id INTEGER,
    account_type_id INTEGER,
    balance NUMERIC(12,2),
    open_date DATE,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
    FOREIGN KEY (branch_id) REFERENCES branches(branch_id),
    FOREIGN KEY (account_type_id) REFERENCES account_types(account_type_id)
);

-- Table: transactions
CREATE TABLE transactions (
    txn_id INTEGER PRIMARY KEY,
    account_id INTEGER,
    txn_date DATE,
    amount NUMERIC(12,2),
    txn_type VARCHAR(20),
    description TEXT,
    FOREIGN KEY (account_id) REFERENCES accounts(account_id)
);

-- Table: loans
CREATE TABLE loans (
    loan_id INTEGER PRIMARY KEY,
    customer_id INTEGER,
    account_id INTEGER,
    loan_type_id INTEGER,
    amount NUMERIC(12,2),
    start_date DATE,
    term_months INTEGER,
    interest_rate NUMERIC(5,2),
	issued_by_employee_id INTEGER,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
    FOREIGN KEY (account_id) REFERENCES accounts(account_id),
    FOREIGN KEY (loan_type_id) REFERENCES loan_types(loan_type_id)
);

-- Table: loan_payments
CREATE TABLE loan_payments (
    payment_id INTEGER PRIMARY KEY,
    loan_id INTEGER,
    payment_date DATE,
    amount NUMERIC(12,2),
    status VARCHAR(20),
    interest_amount INTEGER,
    FOREIGN KEY (loan_id) REFERENCES loans(loan_id)
);

-- Table: credit_cards
CREATE TABLE credit_cards (
    card_id INTEGER PRIMARY KEY,
    customer_id INTEGER,
    account_id INTEGER,
    card_type VARCHAR(50),
    credit_limit NUMERIC(12,2),
    issue_date DATE,
    processed_by_employee_id INTEGER,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
    FOREIGN KEY (account_id) REFERENCES accounts(account_id)
);

-- Table: card_transactions
CREATE TABLE card_transactions (
    card_txn_id INTEGER PRIMARY KEY,
    card_id INTEGER,
    txn_date DATE,
    merchant VARCHAR(100),
    amount NUMERIC(12,2),
    category VARCHAR(50),
    FOREIGN KEY (card_id) REFERENCES credit_cards(card_id)
);

-- Table: atm_withdrawals
CREATE TABLE atm_withdrawals (
    withdrawal_id INTEGER PRIMARY KEY,
    account_id INTEGER,
    withdrawal_date DATE,
    amount NUMERIC(12,2),
    atm_location TEXT,
    FOREIGN KEY (account_id) REFERENCES accounts(account_id)
);
