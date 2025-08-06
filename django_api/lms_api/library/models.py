from django.db import models
from pydantic.v1.main import Model

class Library_Col(models.Model):
    library_id = models.AutoField(primary_key= True)
    l_name = models.CharField(max_length=30)
    campus_location = models.CharField(max_length=100)
    contact_email = models.CharField(max_length=30, null=True, blank= True)
    phone_number = models.CharField(max_length=15, null = True, blank= True)

    class Meta:
        db_table = 'library_col'
        managed = False

    def __str__(self):
        return self.l_name

class Book(models.Model):
    book_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=30)
    isbn = models.CharField(max_length=20)
    publication_date = models.DateTimeField()
    total_copies = models.PositiveSmallIntegerField(null=True, blank=True)
    available_copies = models.PositiveIntegerField(null=True, blank=True)
    library_id = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = 'book'
        managed = False

    def __str__(self):
        return self.title


class Author(models.Model):
    author_id = models.AutoField(primary_key= True)
    first_name = models.CharField(max_length= 15)
    last_name = models.CharField(max_length= 15, null = True)
    birth_date = models.DateTimeField(null= True)
    nationality = models.CharField(max_length= 30, null = True)
    biography = models.TextField(null = True)

    class Meta:
        db_table = 'author'
        managed = False

    def __str__(self):
        return self.first_name

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
        managed = False

    def __str__(self):
        return self.first_name


class Borrowing(models.Model):
    borrowing_id = models.AutoField(primary_key = True)
    member_id = models.ForeignKey(Member, on_delete= models.SET_NULL, null = True)
    book_id = models.ForeignKey(Book,on_delete= models.SET_NULL, null = True)
    borrow_date = models.DateTimeField()
    due_date = models.DateTimeField()
    return_date = models.DateTimeField()
    late_fee = models.IntegerField()

    class Meta:
        db_table = 'borrowing'
        managed = False

    def __str__(self):
        return self.borrowing_id


class Review(models.Model):
    review_id = models.AutoField(primary_key= True)
    member_id = models.ForeignKey(Member, on_delete= models.SET_NULL)
    book_id = models.ForeignKey(Book , on_delete= models.SET_NULL)
    rating = models.SmallIntegerField(null = True)
    comments = models.TextField(null = True)
    review_data = models.TextField(null = True)

    class Meta:
        db_table = 'review'
        managed = False

    def __str__(self):
        return self.review_id


class Category(models.Model):
    category_id = models.AutoField(primary_key= True)
    name = models.CharField(max_length= 30, null = False)
    description = models.TextField(null = True)

    class Meta:
        db_table = 'category'
        managed = False

    def __str__(self):
        return self.name

