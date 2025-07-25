show tables;

select * from author;
select * from category;
select * from bookcategory;
select * from Book;
select * from bookauthor;


-- list of books which are present in which library
select l.l_name,
b.title
from library_col l
inner join Book b 
on l.library_id = b.library_id;

-- list of books which are 

-- list the Book with their authors name
select b.title, a.first_name,a.last_name
from Book b 
inner join BookAuthor ba 
on b.book_id=ba.book_id
inner join Author a
on a.author_id = ba.author_id;

-- Books with their authors and categories
select 
b.title,
a.first_name,
a.last_name,
c.name
from book b
inner join bookauthor ba on ba.book_id = b.book_id
inner join author a on a.author_id = ba.book_id
inner join bookcategory bc on b.book_id = bc.book_id
inner join category c on c.category_id = bc.category_id;


-- Most borrowed books in the last 30 days
select b.title,
count(br.book_id) as "No. of Books"
from Borrowing br
inner join book b on b.book_id = br.book_id
where  br.borrow_date > date_sub(now(),interval 30 day)
group by br.book_id 
order by "No. of Books" desc;

-- Members with overdue books and calculated late fees
-- Considering late fee as Rs. 5 per day
-- first look for the member who are didn't submit books on time
select m.first_name, m.last_name, br.due_date, br.return_date
from Members m
inner join Borrowing br on  br.member_id = m.member_id
where br.return_date>br.due_date;

select * from Borrowing;


select
b.title,
count(b.title) as "No. of Times borrowed"
from book b
inner join Borrowing br on b.book_id = br.book_id
group by b.title
order by "No. of Times borrowed" desc 
limit 5;


