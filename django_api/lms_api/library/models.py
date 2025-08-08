from django.db import models

class Library_Col(models.Model):
    l_name = models.CharField(max_length=30)
    campus_location = models.CharField(max_length=100)
    contact_email = models.EmailField(max_length=50, null=True, blank= True)
    phone_number = models.CharField(max_length=15, null = True, blank= True)

    class Meta:
        db_table = 'library_col'

    def __str__(self):
        return self.l_name

class Author(models.Model):
    first_name = models.CharField(max_length= 15)
    last_name = models.CharField(max_length= 15, null = True)
    birth_date = models.DateField(null= True)
    nationality = models.CharField(max_length= 30, null = True)
    biography = models.TextField(null = True)

    class Meta:
        db_table = 'author'

    def __str__(self):
        return self.first_name

class Category(models.Model):
    name = models.CharField(max_length= 30, null = False)
    description = models.TextField(null = True)

    class Meta:
        db_table = 'category'

    def __str__(self):
        return self.name


class Book(models.Model):
    library = models.ForeignKey(Library_Col,on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=30)
    isbn = models.CharField(max_length=20)
    publication_date = models.DateTimeField()
    total_copies = models.PositiveSmallIntegerField(null=True, blank=True)
    available_copies = models.PositiveIntegerField(null=True, blank=True)
    authors = models.ManyToManyField(Author)
    categories = models.ManyToManyField(Category)

    class Meta:
        db_table = 'book'

    def __str__(self):
        return self.title



class Member(models.Model):
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
    member = models.ForeignKey(Member, on_delete= models.SET_NULL, null = True)
    book = models.ForeignKey(Book,on_delete= models.SET_NULL, null = True)
    borrow_date = models.DateTimeField()
    due_date = models.DateTimeField(null = True)
    return_date = models.DateTimeField(null = True)
    late_fee = models.IntegerField(null = True)

    class Meta:
        db_table = 'borrowing'

    def __str__(self):
        return self.member.first_name


class Review(models.Model):
    member = models.ForeignKey(Member, on_delete= models.SET_NULL, null = True)
    book = models.ForeignKey(Book , on_delete= models.SET_NULL, null = True)
    rating = models.PositiveSmallIntegerField(null = True)
    comments = models.TextField(null = True)
    review_data = models.TextField(null = True)

    class Meta:
        db_table = 'review'

    def __str__(self):
        return self.member.first_name