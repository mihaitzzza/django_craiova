from django.db import models
from django.core.validators import MinValueValidator
from library.models.category import Subcategory
from library.models.publisher import Publisher


class Book(models.Model):
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE)
    publisher = models.ManyToManyField(Publisher, through='PublishedBook', related_name='publishers')
    title = models.CharField(unique=True, max_length=255)
    author = models.CharField(max_length=255)
    year = models.IntegerField()

    def __str__(self):
        return self.title


class PublishedBook(models.Model):
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=6, decimal_places=2, validators=[
        MinValueValidator(0.00)
    ])
    supply = models.IntegerField(validators=[
        MinValueValidator(0)
    ], default=0)

    def __str__(self):
        return f'{self.book.title} [{self.publisher.name}]'
