from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", views.index, name="index"),
    path("faq/", views.faq, name="faq"),
    path("contact/", views.contact, name="contact"),
    path("blank/", views.blank, name="blank"),
    path("login/", views.login_view, name="login"),
    path("register/", views.new_user, name="register"),
    path("confirm/<str:uidb64>/<str:token>/", views.confirm_email, name="verify_email"),
    path("profile/", views.profile, name="profile"),
    path("change-password/", views.change_password, name="change_password"),
    path("logout/", views.logout_view, name="logout"),
    path("books/new-book/", views.new_book, name="new_book"),
    path('view-summary/<int:book_id>/', views.view_book_summary, name='view_book_summary'),
    path("books/queries/", views.book_queries, name="book_queries"),
    path("books/", views.all_books, name="all_books"),
    path("books/query-by/", views.query_books_by, name="query_books_by"),
    path("books/<int:book_id>/", views.show_book, name="show_book"),
    path("books/delete-book/<int:book_id>/", views.delete_book, name="delete_book"),
    path('books/qrcode/<str:string_to_encode>/', views.generate_qr_code, name='generate_qr_code'),
    path('download_qr_code/<str:string_to_encode>/', views.download_qr_code, name='download_qr_code'),
    path("files/new-file/", views.add_new_file, name="new_file"),
    path("files/", views.all_files, name="all_files"),
    path("files/queries/", views.file_queries, name="file_queries"),
    path("files/query-by/", views.query_files_by, name="query_files_by"),
    path("files/<int:file_id>/", views.show_file, name="show_file"),
    path("files/delete-file/<int:file_id>/", views.delete_file, name="delete_file"),
    path("clients/", views.all_clients, name="all_clients"),
    path("clients/new-client/", views.new_client, name="new_client"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)