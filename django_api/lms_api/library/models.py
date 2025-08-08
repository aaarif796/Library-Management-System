from django.db import models

class Library_Col(models.Model):
    l_name = models.CharField(max_length=30)
    campus_location = models.CharField(max_length=100)
    contact_email = models.CharField(max_length=30, null=True, blank= True)
    phone_number = models.CharField(max_length=15, null = True, blank= True)

    class Meta:
        db_table = 'library_col'

    def __str__(self):
        return self.l_name

class Author(models.Model):
    author_id = models.AutoField(primary_key= True)
    first_name = models.CharField(max_length= 15)
    last_name = models.CharField(max_length= 15, null = True)
    birth_date = models.DateTimeField(null= True)
    nationality = models.CharField(max_length= 30, null = True)
    biography = models.TextField(null = True)

    class Meta:
        db_table = 'author'

    def __str__(self):
        return self.first_name

    
class Book(models.Model):
    library = models.ForeignKey(Library_Col,on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=30)
    isbn = models.CharField(max_length=20)
    publication_date = models.DateTimeField()
    total_copies = models.PositiveSmallIntegerField(null=True, blank=True)
    available_copies = models.PositiveIntegerField(null=True, blank=True)
    authors = models.ManyToManyField(Author, related_name='books')
    class Meta:
        db_table = 'book'

    def __str__(self):
        return self.title



class Member(models.Model):
    member_id = models.AutoField(primary_key= True)
    first_name = models.CharField(max_length= 15)
    last_name = models.CharField(max_length= 15)
    email = models.EmailField(max_length=30, unique= True, null = True)
    phone = models.CharField(max_length= 15, null = True)
    member_type = models.CharField(max_length= 10, null = True)
    registration_date = models.DateTimeField(null = True)

    class Meta:
        db_table = 'members'

    def __str__(self):
        return self.first_name


class Borrowing(models.Model):
    borrowing_id = models.AutoField(primary_key = True)
    member = models.ForeignKey(Member, on_delete= models.SET_NULL, null = True)
    book = models.ForeignKey(Book,on_delete= models.SET_NULL, null = True)
    borrow_date = models.DateTimeField()
    due_date = models.DateTimeField()
    return_date = models.DateTimeField()
    late_fee = models.IntegerField()

    class Meta:
        db_table = 'borrowing'

    def __str__(self):
        return str(self.borrowing_id)


class Review(models.Model):
    review_id = models.AutoField(primary_key= True)
    member = models.ForeignKey(Member, on_delete= models.SET_NULL, null = True)
    book = models.ForeignKey(Book , on_delete= models.SET_NULL, null = True)
    rating = models.SmallIntegerField(null = True)
    comments = models.TextField(null = True)
    review_data = models.TextField(null = True)

    class Meta:
        db_table = 'review'

    def __str__(self):
        return str(self.review_id)


class Category(models.Model):
    category_id = models.AutoField(primary_key= True)
    name = models.CharField(max_length= 30, null = False)
    description = models.TextField(null = True)

    class Meta:
        db_table = 'category'

    def __str__(self):
        return self.name

# class BookCategory(models.Model):
#     id = models.AutoField(primary_key=True)
#     book = models.ForeignKey(Book, on_delete=models.CASCADE)
#     category = models.ForeignKey(Category, on_delete=models.CASCADE)
#     class Meta:
#         db_table = 'bookcategory'
#         managed = False
#         unique_together = ('book', 'category')
#
#
# class BookAuthor(models.Model):
#     book = models.ForeignKey(Book, on_delete=models.CASCADE)
#     author = models.ForeignKey('Author', on_delete=models.CASCADE)
#     class Meta:
#         db_table = 'bookauthor'
#         managed = False
#         unique_together = ('book', 'author')
