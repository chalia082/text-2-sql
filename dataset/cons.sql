-- First, add primary keys with proper quoting
ALTER TABLE categories ADD CONSTRAINT pk_categories PRIMARY KEY (categoryID);
ALTER TABLE products ADD CONSTRAINT pk_products PRIMARY KEY (productID);
ALTER TABLE suppliers ADD CONSTRAINT pk_suppliers PRIMARY KEY (supplierID);
ALTER TABLE employees ADD CONSTRAINT pk_employees PRIMARY KEY (employeeID);
ALTER TABLE territories ADD CONSTRAINT pk_territories PRIMARY KEY (territoryID);
ALTER TABLE regions ADD CONSTRAINT pk_regions PRIMARY KEY (regionID);
ALTER TABLE orders ADD CONSTRAINT pk_orders PRIMARY KEY (orderID);
ALTER TABLE customers ADD CONSTRAINT pk_customers PRIMARY KEY (customerID);
ALTER TABLE shippers ADD CONSTRAINT pk_shippers PRIMARY KEY (shipperID);

-- Composite primary keys
ALTER TABLE orderdetails ADD CONSTRAINT pk_order_details PRIMARY KEY (orderID, productID);
ALTER TABLE employeeterritories ADD CONSTRAINT pk_employee_territories PRIMARY KEY (employeeID, territoryID);

-- Fix data type for reportsTo column
ALTER TABLE employees ALTER COLUMN reportsTo TYPE bigint USING reportsTo::bigint;

-- Then add foreign keys with proper quoting
ALTER TABLE products ADD CONSTRAINT fk_products_supplier 
    FOREIGN KEY (supplierID) REFERENCES suppliers(supplierID);
ALTER TABLE products ADD CONSTRAINT fk_products_category 
    FOREIGN KEY (categoryID) REFERENCES categories(categoryID);

ALTER TABLE orders ADD CONSTRAINT fk_orders_customer 
    FOREIGN KEY (customerID) REFERENCES customers(customerID);
ALTER TABLE orders ADD CONSTRAINT fk_orders_employee 
    FOREIGN KEY (employeeID) REFERENCES employees(employeeID);
ALTER TABLE orders ADD CONSTRAINT fk_orders_shipper 
    FOREIGN KEY (shipVia) REFERENCES shippers(shipperID);

ALTER TABLE orderdetails ADD CONSTRAINT fk_order_details_order 
    FOREIGN KEY (orderID) REFERENCES orders(orderID) ON DELETE CASCADE;
ALTER TABLE orderdetails ADD CONSTRAINT fk_order_details_product 
    FOREIGN KEY (productID) REFERENCES products(productID);

ALTER TABLE territories ADD CONSTRAINT fk_territories_region 
    FOREIGN KEY (regionID) REFERENCES regions(regionID);

ALTER TABLE employeeterritories ADD CONSTRAINT fk_employee_territories_employee 
    FOREIGN KEY (employeeID) REFERENCES employees(employeeID) ON DELETE CASCADE;
ALTER TABLE employeeterritories ADD CONSTRAINT fk_employee_territories_territory 
    FOREIGN KEY (territoryID) REFERENCES territories(territoryID) ON DELETE CASCADE;

-- Now add the employees manager foreign key (after fixing data type)
ALTER TABLE employees ADD CONSTRAINT fk_employees_manager 
    FOREIGN KEY (reportsTo) REFERENCES employees(employeeID);