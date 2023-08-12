from django.contrib import admin
from .models import User, Book, File, Location, Client, Type, Author, Language

# Register your models here.
admin.site.register(User)
admin.site.register(Book)
admin.site.register(File)
admin.site.register(Location)
admin.site.register(Client)
admin.site.register(Type)
admin.site.register(Author)
admin.site.register(Language)
