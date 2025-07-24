create database lms;

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

INSERT INTO library_col (l_name, campus_location, contact_email, phone_number) VALUES
('HCU', 'Hyderabad Campus', 'hcu@univ.edu', '+91-1234567890'),
('JNTU', 'JNTU Campus', 'jntu@univ.edu', '+91-2134567891'),
('Hyderabad Library', 'Hyderabad', 'hyd@hl.org', '1324567892'),
('Medical Library', 'Medical College', 'med@aiims.edu', '1234577893'),
('Law Library', 'Law Faculty', 'law@univ.edu', '1234567984'),
('Gachibowli Library', 'Arts Campus', 'library@gach.edu', '3334567895'),
('ISB Library', 'Business School', 'library@isb.edu', '1234588896'),
('EFLU', 'EFLU Campus', 'lirary@eflu.edu', '1234567777'),
('Banglore Library', 'Bangalore', 'library@bu.edu', '3214567898'),
('Tech Library', 'Online', 'techno@tech.edu', '1234567889');


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

INSERT INTO Book (title, isbn, publication_date, total_copies, available_copies, library_id) VALUES
('Data Structures', '978-0131103627', '2018-01-15', 10, 4, 1),
('Introduction to Algorithms', '978-0262033848', '2020-05-21', 8, 5, 2),
('Operating Systems', '978-0073529409', '2019-09-10', 12, 7, NULL),
('Database Systems', '978-0133970777', '2017-02-28', 15, 10, 3),
('Computer Networks', '978-0132126953', '2016-03-12', 9, 3, NULL),
('Machine Learning Basics', '978-1492032649', '2021-07-01', 5, 2, 4),
('Artificial Intelligence', '978-0136042594', '2022-01-18', 6, 1, 5),
('Python Programming', '978-0596007973', '2020-08-25', 11, 6, NULL),
('Digital Design', '978-0131989245', '2015-11-15', 7, 2, 6),
('Modern Physics', '978-1133954057', '2019-06-20', 10, 5, 7);

select * from Book;


-- Create Author Table
create table Author(
	author_id int auto_increment primary key,
    first_name varchar(15) not null,
    last_name varchar(15),
    birth_date datetime,
    nationality varchar(30),
    biography varchar(200)
);

create table BookAuthor(
	book_id int not null,
    author_id int not null,
    primary key(book_id, author_id),
    foreign key (book_id) references Book(book_id) ON DELETE RESTRICT ON UPDATE CASCADE,
    foreign key (author_id) references Author(author_id) ON DELETE RESTRICT ON UPDATE CASCADE
);

show tables;
create table Category(
	category_id int auto_increment primary key,
    name varchar(30) not null,
    description varchar(100)
);
create table BookCategory(
	book_id int not null,
	category_id int not null,
    primary key(book_id, category_id),
    foreign key (book_id) references Book(book_id) on delete restrict on update cascade,
    foreign key (category_id) references Category(category_id) on delete restrict on update cascade
);


create table Members(
	member_id int auto_increment primary key,
    first_name varchar(15) not null,
    last_name varchar(15),
    email varchar(30) unique,
    phone varchar(15),
    member_type varchar(10),
    registration_date datetime
);

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

create table Review(
	review_id int auto_increment primary key,
    member_id int,
    book_id int,
    rating smallint unsigned,
    comments varchar(30),
    review_data varchar(50),
    foreign key (member_id) references Members(member_id) ON UPDATE CASCADE,
    foreign key (book_id) references Book(book_id) ON UPDATE CASCADE
);

show tables;