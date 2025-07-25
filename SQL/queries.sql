show tables;

select * from author;
select * from category;
select * from bookcategory;
select * from Book;
select * from bookauthor;

SET GLOBAL sql_mode='STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO';

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
	select m.first_name, m.last_name, br.due_date,
	datediff(ifnull(br.return_date,now()), br.due_date) * 5 as "Due"
	from Members m
	inner join Borrowing br on  br.member_id = m.member_id
	where ifnull(br.return_date,now())>br.due_date
	order by "Due" desc;

-- Average rating per book with author information 
	select b.title, a.first_name, a.last_name , avg(r.rating)
	from Review r
	inner join Book b on b.book_id = r.book_id
	inner join BookAuthor ba on ba.book_id = b.book_id
	inner join Author a on a.author_id = ba.author_id
	group by b.book_id, a.author_id;


-- Books available in each library with stock levels
	with stock_percentage as(
		select l.l_name as Lib_name, 
        sum(b.available_copies) as Available_Copies,
        floor((sum(b.available_copies)/sum(b.total_copies))*100) as Stock_Percentage
        from Book b join Library_Col l on b.library_id=l.library_id
        group by l.library_id
    )
    select Lib_name, Available_Copies,
    case
		when Stock_Percentage>75 then "High"
        when Stock_Percentage>50 then "Medium"
        else "Low"
	end as Stock_Level
    from stock_percentage;



-- No. of times member borrowed
	select
	b.title,
	count(b.title) as "No. of Times borrowed"
	from book b
	inner join Borrowing br on b.book_id = br.book_id
	group by b.title
	order by "No. of Times borrowed" desc 
	limit 5;

-- List out the library with book number in descending order
	select l.l_name, count(b.book_id)
    from library_col l
    join book b on l.library_id = b.library_id
    group by l.library_id;

-- List the Book which is borrowed by more top 5 member
	select m.member_id, m.first_name, m.last_name, count(br.book_id) as "No. of Books", GROUP_CONCAT(b.title SEPARATOR ', ') as "Name of Book"
    from Members m
    inner join Borrowing br 
    on m.member_id = br.member_id
    inner join book b
    on b.book_id = br.book_id
    group by m.member_id
    order by "No. of Books" desc limit 5;
    

-- List out the Author with the number of book
	select a.first_name, a.last_name, count(b.book_id) as "No. of Book"
    from Author a
    inner join BookAuthor ba on a.author_id = ba.author_id
    inner join Book b on b.book_id=ba.book_id
    group by a.author_id
    order by count(b.book_id) desc;

-- Total late fee remaining in the HCU library
	select sum(br.late_fee) 
    from borrowing br
    join book b on b.book_id = br.book_id
    join library_col l on l.library_id = b.library_id
    where l_name = "HCU" ;
    
    
-- Subqueries and Common Table Expressions (CTEs)
	



desc library_col;    
select * from Library_col;
select * from book;
