use lms;
show tables;

INSERT INTO library_col (l_name, campus_location, contact_email, phone_number) VALUES
('HCU', 'Hyderabad Campus', 'hcu@univ.edu', '+91-1234567890'),
('JNTU', 'JNTU Campus', 'jntu@univ.edu', '+91-2134567891'),
('Medical Library', 'Medical College', 'med@aiims.edu', '1234577893');

INSERT INTO Book (title, isbn, publication_date, total_copies, available_copies, library_id) VALUES
('Data Structures', '+91-0131103627', '2018-01-15', 10, 4, 1),
('Intro to Algorithms', '+977-0262033848', '2020-05-21', 8, 5, 2),
('Operating Systems', '+1-0073529409', '2019-09-10', 12, 7, NULL),
('Database Systems', '+99-0133970777', '2017-02-28', 15, 10, 1),
('Computer Networks', '+8-0132126953', '2016-03-12', 9, 3, NULL),
('Machine Learning', '+88-1492032649', '2021-07-01', 5, 2, 3),
('Artificial Intelligence', '+1-0136042594', '2022-01-18', 6, 1, 2),
('Python Programming', '+9-0596007973', '2020-08-25', 11, 6, NULL),
('Digital Design', '+8-0131989245', '2015-11-15', 7, 2, 3),
('Modern Physics', '+2-1133954057', '2019-06-20', 10, 5, 1),
('Deep Learning', '1617294433', '2021-07-10', 8, 6, 1),
('NLP Essentials', '+91-1491978238', '2020-11-15', 10, 4, 2),
('Cybersecurity', '+88-0135774778', '2019-08-05', 6, 2, 3),
('Data Viz Guide', '+92-0134384688', '2022-03-22', 7, 5, 1),
('Cloud Computing', '+90-1118283305', '2023-01-30', 9, 7, 2);


INSERT INTO Author (first_name, last_name, birth_date, nationality, biography) VALUES
('Thomas', 'Cormen', '1956-01-01', 'American', 'Algorithm specialist'),
('Andrew', 'S. Tanenbaum', '1944-03-16', 'Dutch-American', 'OS and networking expert'),
('Ian', 'Goodfellow', '1985-04-15', 'American', 'Deep learning researcher'),
('Yann', 'LeCun', '1960-07-08', 'French-American', 'AI pioneer'),
('Guido', 'van Rossum', '1956-01-31', 'Dutch', 'Python creator'),
('Mark', 'Zuckerberg', '1984-05-14', 'American', 'Tech innovator'),
('Brian', 'Kernighan', '1942-01-01', 'Canadian', 'C language and systems author'),
('Donald', 'Knuth', '1938-01-10', 'American', 'Algorithm analysis legend');


INSERT INTO BookAuthor (book_id, author_id) VALUES
(1, 1), (2, 1), (3, 2), (4, 2),
(5, 2), (6, 3), (7, 4), (8, 5),
(9, 2), (10, 7), (11, 3), (12, 3),
(13, 2), (14, 6), (15, 6);

INSERT INTO Category (name, description) VALUES
('University Book','Academic resources for students'),
('Sci-Fi','Science and futuristic stories'),
('History','Books covering historical events'),
('Novel','Literary fiction and storytelling'),
('Technology','Modern computing and IT topics');

INSERT INTO BookCategory (book_id, category_id) VALUES
(1, 1), (2, 1), (3, 1), (4, 1),
(5, 5), (6, 5), (7, 5), (8, 5),
(9, 5), (10, 3), (11, 5), (12, 5),
(13, 5), (14, 5), (15, 5);

INSERT INTO Members (first_name, last_name, email, phone, member_type, registration_date) VALUES
('John', 'Doe', 'john.doe@gmail.com', '9123450001', 'student', '2023-01-01'),
('Alice', 'Smith', 'alice.smith@gmail.com', '9123450002', 'faculty', '2023-01-02'),
('Bob', 'Johnson', 'bob.j@gmail.com', '9123450003', 'staff', '2023-01-03'),
('Neha', 'Rana', 'neha.r@gmail.com', '9123450004', 'student', '2023-01-04'),
('Vikram', 'Kapoor', 'vikram.k@gmail.com', '9123450005', 'student', '2023-01-05'),
('Tanvi', 'Mehta', 'tanvi.m@gmail.com', '9123450006', 'faculty', '2023-01-06'),
('Raj', 'Thakur', 'raj.t@gmail.com', '9123450007', 'student', '2023-01-07'),
('Ayaan', 'Malik', 'ayaan.m@gmail.com', '9123450008', 'student', '2023-01-08'),
('Pooja', 'Arora', 'pooja.a@gmail.com', '9123450009', 'faculty', '2023-01-09'),
('Manav', 'Chawla', 'manav.c@gmail.com', '9123450010', 'student', '2023-01-10'),
('Divya', 'Garg', 'divya.g@gmail.com', '9123450011', 'staff', '2023-01-11'),
('Kabir', 'Gupta', 'kabir.g@gmail.com', '9123450012', 'student', '2023-01-12'),
('Simran', 'Bhatia', 'simran.b@gmail.com', '9123450013', 'faculty', '2023-01-13'),
('Harsh', 'Verma', 'harsh.v@gmail.com', '9123450014', 'student', '2023-01-14'),
('Sara', 'Ali', 'sara.a@gmail.com', '9123450015', 'faculty', '2023-01-15'),
('Rehan', 'Khan', 'rehan.k@gmail.com', '9123450016', 'staff', '2023-01-16'),
('Ishita', 'Sharma', 'ishita.s@gmail.com', '9123450017', 'student', '2023-01-17'),
('Om', 'Patel', 'om.p@gmail.com', '9123450018', 'student', '2023-01-18'),
('Meena', 'Joshi', 'meena.j@example.com', '9123450019', 'faculty', '2023-01-19'),
('Nikhil', 'Rao', 'nikhil.r@gmail.com', '9123450020', 'student', '2023-01-20');

INSERT INTO Borrowing (member_id, book_id, borrow_date, due_date, return_date, late_fee) VALUES
(1, 1, '2025-07-01', '2025-07-10', '2025-07-10', 0),
(2, 2, '2025-07-01', '2025-07-11', '2025-07-13', 10),
(3, 3, '2025-07-02', '2025-07-12', NULL, NULL),
(4, 4, '2025-07-02', '2025-07-13', NULL, NULL),
(5, 5, '2025-07-03', '2025-07-14', '2025-07-14', 0),
(6, 6, '2025-07-03', '2025-07-15', NULL, NULL),
(7, 7, '2025-07-04', '2025-07-16', NULL, NULL),
(8, 8, '2025-07-04', '2025-07-17', NULL, NULL),
(9, 9, '2025-07-05', '2025-07-18', NULL, NULL),
(10, 10, '2025-07-05', '2025-07-19', '2025-07-19', 0),
(11, 11, '2025-07-06', '2025-07-20', '2025-07-21', 5),
(12, 12, '2025-07-06', '2025-07-21', NULL, NULL),
(13, 13, '2025-07-07', '2025-07-22', NULL, NULL),
(14, 14, '2025-07-07', '2025-07-23', '2025-07-24', 10),
(15, 15, '2025-07-08', '2025-07-24', NULL, NULL),
(16, 1, '2025-07-08', '2025-07-25', NULL, NULL),
(17, 2, '2025-07-09', '2025-07-26', NULL, NULL),
(18, 3, '2025-07-09', '2025-07-27', NULL, NULL),
(19, 4, '2025-07-10', '2025-07-28', '2025-07-28', 0),
(20, 5, '2025-07-10', '2025-07-29', NULL, NULL),
(1, 6, '2025-07-11', '2025-07-30', NULL, NULL),
(2, 7, '2025-07-11', '2025-07-31', NULL, NULL),
(3, 8, '2025-07-12', '2025-08-01', NULL, NULL),
(4, 9, '2025-07-12', '2025-08-02', NULL, NULL),
(5, 10, '2025-07-13', '2025-08-03', NULL, NULL);

INSERT INTO Review (member_id, book_id, rating, comments, review_data) VALUES
(1, 1, 5, 'Excellent book', 'Very useful'),
(2, 2, 4, 'Great content', 'Well explained'),
(3, 3, 4, 'Helpful', 'Conceptually strong'),
(4, 4, 5, 'Loved it', 'Very detailed'),
(5, 5, 3, 'Good', 'Could be better'),
(6, 6, 5, 'Superb', 'Best for ML'),
(7, 7, 2, 'Okayish', 'Average content'),
(8, 8, 4, 'Useful', 'Practically relevant'),
(9, 9, 5, 'Perfect', 'Easy to understand'),
(10, 10, 3, 'Basic', 'Too simple'),
(11, 11, 4, 'Informative', 'Nice structure'),
(12, 12, 5, 'Impressive', 'Deep insights');
