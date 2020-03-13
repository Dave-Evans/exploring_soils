from django.db import models

class Book(models.Model):
    NOVEL = 1
    NONFICTION = 2
    BIOGRAPHY = 3
    SHORTSTORY = 4
    GRAPHICNOVEL = 5
    OTHER = 6
    BOOK_TYPES = (
        (NOVEL, 'Novel'),
        (NONFICTION, 'Non-Fiction'),
        (BIOGRAPHY, 'Biography'),
        (SHORTSTORY, 'Short story'),
        (GRAPHICNOVEL, 'Graphic novel'),
        (OTHER, 'Other'),
    )
    title               = models.CharField(max_length=50)
    publication_date    = models.DateField(null=True, blank=True)
    finished_date       = models.DateField(null=True, blank=True)
    author              = models.CharField(max_length=30, blank=True)
    # price             = models.DecimalField(max_digits=5, decimal_places=2)
    pages               = models.IntegerField(blank=True, null=True)
    book_type           = models.PositiveSmallIntegerField(choices=BOOK_TYPES)
    description         = models.TextField(blank=True)
    completed           = models.BooleanField(default = False)
