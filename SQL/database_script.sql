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

insert into Author
(first_name, last_name, birth_date, nationality, biography)
values
("Amit", "Ghimire","2001-10-08","Indian","He is born and brought from poor family");

insert into Author
(first_name, last_name, birth_date, nationality, biography)
values
("Arman", "Ghimire","2001-10-08","Indian","He is born and brought from poor family"),
("Aswad", "Ghimire","1998-10-08","Indian","He is one of the great person"),
("Alexender", "Ghimire","1999-08-02","Indian","He is consider as great writer of Nation"),
("Abeshek", "Sheresta","1992-10-08","Indian","He is leagend writer ever born in the world"),
("Amar", "Tripathi","1993-10-08","Indian","He is bookish person"),
("Ashan", "Bhujel","1995-10-08","Indian","He is fight like a real fighter for himself."),
("Aryan", "Sheikh","1996-10-08","German","He is the person become voice for voiceles people"),
("Ankit", "Dhakal","1998-10-08","American","He is expertize of Novol"),
("Aniket", "Basnet","1988-10-08","British","He is great writer of histor"),
("Akshat", "Yadav","1994-10-08","Nepali","He is the voice of tribral people");


select * from Author;

create table BookAuthor(
	book_id int not null,
    author_id int not null,
    primary key(book_id, author_id),
    foreign key (book_id) references Book(book_id) ON DELETE RESTRICT ON UPDATE CASCADE,
    foreign key (author_id) references Author(author_id) ON DELETE RESTRICT ON UPDATE CASCADE
);

desc BookAuthor;
select * from Book;
select * from Author;

insert into BookAuthor
values
(1,1),
(2,2),
(3,3),
(4,4),
(5,5),
(6,6),
(7,7),
(8,8),
(8,9),
(9,9),
(10,10),
(10,11),
(8,11);
select * from BookAuthor;

show tables;

create table Category(
	category_id int auto_increment primary key,
    name varchar(30) not null,
    description varchar(100)
);
insert into Category
(name,description)
values 
("University Book","Used to study for formal education"),
("Sci-Fi Book", "Science and Frictional type of books"),
("History Book","Best place to know about the past"),
("Novel","It's one of the book read by rich people to proof they are rich");

create table BookCategory(
	book_id int not null,
	category_id int not null,
    primary key(book_id, category_id),
    foreign key (book_id) references Book(book_id) on delete restrict on update cascade,
    foreign key (category_id) references Category(category_id) on delete restrict on update cascade
);

INSERT INTO BookCategory (book_id, category_id) VALUES
(1, 1), 
(1,2),
(2, 1),
(3, 1),
(4, 1),
(5, 2),
(6, 1),
(7, 2),
(8, 4),
(8, 3),
(9, 1),
(10, 3);


create table Members(
	member_id int auto_increment primary key,
    first_name varchar(15) not null,
    last_name varchar(15),
    email varchar(30) unique,
    phone varchar(15),
    member_type varchar(10),
    registration_date datetime
);
INSERT INTO Members (first_name, last_name, email, phone, member_type, registration_date) VALUES
('Ravi', 'Verma', 'ravi1@gmail.com', '9990010001', 'student', '2023-01-15'),
('Sneha', 'Kumar', 'sneha.k@gamil.com', '9990010002', 'staff', '2023-02-12'),
('Aarav', 'Sharma', 'aarav.s@gmail.com', '9990010003', 'student', '2023-03-10'),
('Meera', 'Yadav', 'meera.y@gmail.com', '9990010004', 'faculty', '2023-04-18'),
('Aditya', 'Singh', 'aditya.s@gmail.com', '9990010005', 'student', '2023-05-05'),
('Nisha', 'Rao', 'nisha.r@gmail.com', '9990010006', 'staff', '2023-06-22'),
('Karan', 'Patel', 'karan.p@gmail.com', '9990010007', 'student', '2023-07-11'),
('Priya', 'Joshi', 'priya.j@gmail.com', '9990010008', 'faculty', '2023-08-19'),
('Ishaan', 'Malhotra', 'ishaan.m@gmail.com', '9990010009', 'student', '2023-09-03'),
('Diya', 'Bansal', 'diya.b@gmail.com', '9990010010', 'staff', '2023-10-01');

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
INSERT INTO Borrowing (member_id, book_id, borrow_date, due_date, return_date, late_fee) VALUES
(1, 1, '2024-01-01', '2024-01-15', '2024-01-14', 0),
(2, 2, '2024-01-10', '2024-01-25', '2024-01-28', 30),
(3, 3, '2024-02-05', '2024-02-20', NULL, NULL),
(4, 4, '2024-03-01', '2024-03-15', '2024-03-15', 0),
(5, 5, '2024-03-10', '2024-03-25', '2024-04-01', 50),
(6, 6, '2024-04-01', '2024-04-15', NULL, NULL),
(7, 7, '2024-04-10', '2024-04-25', '2024-04-24', 0),
(8, 8, '2024-05-05', '2024-05-20', '2024-05-19', 0),
(9, 9, '2024-06-01', '2024-06-15', NULL, NULL),
(10, 10, '2024-06-10', '2024-06-25', '2024-06-28', 30);


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
INSERT INTO Review (member_id, book_id, rating, comments, review_data) VALUES
(1, 1, 5, 'Excellent', 'Great for beginners'),
(2, 2, 4, 'Very Good', 'Well structured'),
(3, 3, 3, 'Average', 'Okay content'),
(4, 4, 5, 'Loved it', 'Helpful for exams'),
(5, 5, 2, 'Not clear', 'Confusing examples'),
(6, 6, 4, 'Nice', 'Good introduction'),
(7, 7, 5, 'Awesome', 'Very detailed'),
(8, 8, 4, 'Useful', 'Practical examples'),
(9, 9, 3, 'Decent', 'Needs improvement'),
(10, 10, 5, 'Amazing', 'Highly recommended');

show tables;


select * from book;
select * from author;


