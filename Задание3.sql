select stack.Customers.name from stack.Customers,stack.OrderItems,stack.Orders  
where stack.Customers.row_id = stack.Orders.customer_id AND stack.Orders.registered_at > '2019-12-31' AND 
stack.Orders.row_id = stack.OrderItems.order_id AND stack.OrderItems.name = N'Кассовый аппарат' GROUP BY Customers.name
