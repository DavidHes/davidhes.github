--um tabellen raus zu löschen

--To reduce potential errors it is usually a good idea to DROP TABLE containing foreign keys first. 
--This is why we DROP TABLE in reverse order of the CREATE TABLE statements.

BEGIN TRANSACTION;
DROP TABLE IF EXISTS todo_list;
DROP TABLE IF EXISTS list;
DROP TABLE IF EXISTS todo;
COMMIT;
