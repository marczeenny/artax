from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.


class User(AbstractUser):
    email = models.EmailField(blank=True, unique=True)
    about = models.TextField()
    job = models.CharField(max_length=200)
    address = models.TextField()
    phone = models.CharField(max_length=100)
    date_of_registration = models.DateField(default=datetime.today)

    def __str__(self):
        return f"@{self.username}"

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}".strip()


class Book(models.Model):
    lib_id = models.CharField(max_length=50, default="ABC123")
    author = models.ForeignKey("Author", models.PROTECT, related_name="book")
    title = models.CharField(max_length=250)
    subject = models.TextField(null=True)
    type = models.ForeignKey("Type", models.PROTECT, related_name="book")
    section = models.CharField(max_length=250)
    location = models.ForeignKey("Location", models.PROTECT, related_name="book", null=True)
    publisher = models.CharField(max_length=250)
    publishing_date = models.CharField(max_length=250, null=True)
    purchase_date = models.DateField(null=True)
    isbn = models.IntegerField(null=True)
    number_of_copies = models.IntegerField()
    language = models.ForeignKey("Language", models.SET_NULL, related_name="book", null=True)
    date_of_registration = models.DateField(default=datetime.today)
    registrator = models.ForeignKey(User, models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.title} by {self.author}"


class File(models.Model):
    client = models.ForeignKey("Client", models.PROTECT)
    opponent = models.CharField(max_length=200, null=True)
    subject = models.TextField(null=True)
    location = models.ForeignKey("Location", models.SET_NULL, null=True)
    sections = models.CharField(max_length=100)
    date_of_registration = models.DateField(default=datetime.today)


class Client(models.Model):
    name = models.CharField(max_length=350, unique=True)
    person_in_charge = models.CharField(max_length=200, null=True)
    mobile_number = PhoneNumberField(null=True, region="LB")
    landline_number = PhoneNumberField(null=True, region="LB")
    address = models.TextField(null=True)
    web_address = models.URLField(null=True)
    date_of_registration = models.DateField(default=datetime.today)
    email = models.EmailField(null=True)


class Author(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.name}"


class Type(models.Model):
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=3)

    def __str__(self):
        return f"{self.name} | Code: {self.code}"


class Location(models.Model):
    code = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.code}"


class Language(models.Model):
    name = models.CharField(max_length=250)
    code = models.CharField(max_length=3)

    def __str__(self):
        return f"{self.name} | Code: {self.code}"
