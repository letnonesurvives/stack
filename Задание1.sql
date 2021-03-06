USE [stack]
GO
/****** Object:  UserDefinedFunction [stack].[select_orders_by_item_name]    Script Date: 22.03.2021 19:24:36 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
ALTER FUNCTION [stack].[select_orders_by_item_name] (@per nvarchar(255))
RETURNS TABLE 
AS
RETURN 
(
	SELECT Orders.row_id,Customers.name,COUNT(Orders.row_id) AS "items_count" 
	FROM stack.Orders,stack.Customers,stack.OrderItems WHERE stack.customers.row_id = stack.Orders.customer_id AND
	stack.Orders.row_id = stack.OrderItems.order_id AND stack.OrderItems.name = @per 
	GROUP BY Orders.row_id, Customers.name

);