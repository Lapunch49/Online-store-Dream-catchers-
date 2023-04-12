CREATE table source_file_catchers (
	id integer PRIMARY KEY autoincrement, 
	filename varchar(255) NOT NULL, 
	processed datetime
);

create table photos(
	id integer PRIMARY KEY autoincrement,
	photo varchar(1000),
	fk_product_id integer NOT NULL,	
	FOREIGN KEY (fk_product_id) REFERENCES dream_catchers(id)
);

create table dream_catchers (
	id integer PRIMARY KEY autoincrement,
	name varchar(255),
	price integer NOT NULL,
	color varchar(255),
	country varcher(255),
	material varchar(255),
	sizes varchar(255),
	form varchar(255),
	description varchar(500),
	
	
	source_file integer REFERENCES source_file_catchers(id) ON DELETE CASCADE
);

create table users (
	id integer PRIMARY KEY autoincrement,  
	email varchar(255) NOT NULL
);

create table orders (
	id integer PRIMARY KEY autoincrement,
	fk_product_id integer REFERENCES dream_catchers(id),
	fk_user_id integer REFERENCES users(id),
	email varchar(255) REFERENCES users(email),
	
	full_user_name varchar(255),
	phone_number varchar(20),
	address varchar(255),
	payment varchar(255)
);