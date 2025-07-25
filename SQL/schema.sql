create database lms;
show databases;

use lms;
show tables;

-- creating Library_Collection table
create table library_col (
library_id int AUTO_INCREMENT PRIMARY KEY,
l_name varchar(30) not null,
campus_location varchar(100) not null,
contact_email varchar(30) unique,
phone_number varchar(15) unique
);


-- create Book table
create table Book(
book_id int auto_increment primary key,
title varchar(30) not null,
isbn varchar(20) not null,
publication_date datetime not null,
total_copies smallint unsigned,
available_copies int unsigned,
library_id int,
foreign key (library_id) references library_col(library_id) on update cascade
);


-- Create Author Table
create table Author(
	author_id int auto_increment primary key,
    first_name varchar(15) not null,
    last_name varchar(15),
    birth_date datetime,
    nationality varchar(30),
    biography text
);


-- create table BookAuthor
create table BookAuthor(
	book_id int not null,
    author_id int not null,
    primary key(book_id, author_id),
    foreign key (book_id) references Book(book_id) ON DELETE RESTRICT ON UPDATE CASCADE,
    foreign key (author_id) references Author(author_id) ON DELETE RESTRICT ON UPDATE CASCADE
);

-- create table Category
create table Category(
	category_id int auto_increment primary key,
    name varchar(30) not null,
    description text
);

-- Create BookCategory
create table BookCategory(
	book_id int not null,
	category_id int not null,
    primary key(book_id, category_id),
    foreign key (book_id) references Book(book_id) on delete restrict on update cascade,
    foreign key (category_id) references Category(category_id) on delete restrict on update cascade
);


-- Create table Members
create table Members(
	member_id int auto_increment primary key,
    first_name varchar(15) not null,
    last_name varchar(15),
    email varchar(30) unique,
    phone varchar(15),
    member_type varchar(10),
    registration_date datetime
);

-- Create table borrowing
create table Borrowing(
	borrowing_id int auto_increment primary key,
    member_id int,
    book_id int,
    borrow_date datetime,
    due_date datetime,
    return_date datetime,
    late_fee int,
    foreign key (member_id) references Members(member_id) ON UPDATE CASCADE,
    foreign key (book_id) references Book(book_id) ON UPDATE CASCADE
);


-- Create table Review
create table Review(
	review_id int auto_increment primary key,
    member_id int,
    book_id int,
    rating smallint unsigned,
    comments text,
    review_data text,
    foreign key (member_id) references Members(member_id) ON UPDATE CASCADE,
    foreign key (book_id) references Book(book_id) ON UPDATE CASCADE
);

show tables;

desc author;

