-- creates a trigger that decreases an item quantity
-- after adding a new order
CREATE TRIGGER quantity_decreaser
AFTER INSERT ON orders
FOR EACH ROW
UPDATE items 
SET quantity = quantity - NEW.number 
WHERE name=NEW.item_name;
