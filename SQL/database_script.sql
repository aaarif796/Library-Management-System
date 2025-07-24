create database lms;

use lms;
show tables;


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
