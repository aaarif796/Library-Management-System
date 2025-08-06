from django.db import models

from django.db import models

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
