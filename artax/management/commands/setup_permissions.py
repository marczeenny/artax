from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType


class Command(BaseCommand):
    help = 'Sets up user groups and permissions'

    def handle(self, *args, **options):
        user_content_type = ContentType.objects.get(app_label='artax', model="user")
        user_permission_view = Permission.objects.get(codename='view_user', content_type=user_content_type)
        user_permission_change = Permission.objects.get(codename='change_user', content_type=user_content_type)
        user_permission_delete = Permission.objects.get(codename='delete_user', content_type=user_content_type)
        user_permission_add = Permission.objects.get(codename='add_user', content_type=user_content_type)

        book_content_type = ContentType.objects.get(app_label='artax', model="book")
        book_permission_view = Permission.objects.get(codename='view_book', content_type=book_content_type)
        book_permission_change = Permission.objects.get(codename='change_book', content_type=book_content_type)
        book_permission_delete = Permission.objects.get(codename='delete_book', content_type=book_content_type)
        book_permission_add = Permission.objects.get(codename='add_book', content_type=book_content_type)

        visitors_group, _ = Group.objects.get_or_create(name='Visitors')
        visitors_group.permissions.add(book_permission_view, user_permission_view)
        lawyer_group, _ = Group.objects.get_or_create(name='Lawyers')
        lawyer_group.permissions.add(book_permission_view, book_permission_change, user_permission_view,
                                     user_permission_change)
        admin_group, _ = Group.objects.get_or_create(name='Office Administrators')
        admin_group.permissions.add(book_permission_view, book_permission_add, book_permission_change,
                                    book_permission_delete, user_permission_view, user_permission_add,
                                    user_permission_change, user_permission_delete)
