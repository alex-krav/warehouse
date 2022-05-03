BEGIN TRANSACTION;
DROP TABLE IF EXISTS `goods`;
CREATE TABLE IF NOT EXISTS `goods` (
	`id`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	`category_id`	INTEGER NOT NULL,
	`name`	TEXT NOT NULL,
	`quantity`	INTEGER NOT NULL,
	`quantity_unit`	TEXT NOT NULL,
	`term`	INTEGER NOT NULL,
	`start_date`	INTEGER NOT NULL,
	`end_date`	INTEGER NOT NULL
);
INSERT INTO `goods` (id,category_id,name,quantity,quantity_unit,term,start_date,end_date) VALUES 
	(1,1,'молоко',1,'літр',3,10,13),
	(2,2,'телевізор',1,'штука',10,20,30);
DROP TABLE IF EXISTS `categories`;
CREATE TABLE IF NOT EXISTS `categories` (
	`id`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	`name`	TEXT NOT NULL UNIQUE
);
INSERT INTO `categories` (id,name) VALUES 
	(1,'продукти харчування'),
 	(2,'побутова техніка');
COMMIT;
