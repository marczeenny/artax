import datetime
from functools import wraps
from smtplib import SMTPRecipientsRefused
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.models import Group
from django.core.files.storage import default_storage
from django.db import IntegrityError
from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required
from .models import User, Book, Client, File, Author, Type, Location, Language
from django.core.paginator import Paginator
from django.core.exceptions import ObjectDoesNotExist, ValidationError, PermissionDenied
from django.contrib import messages
import qrcode
import qrcode.image.svg
from django.db.models import Q
# from pillow import Image, ImageDraw, ImageFont
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import *
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string

RED = '\033[91m'
RESET = '\033[0m'

BASE_URL = ''

PER_PAGE = 25


def redirect_view(function):
    def _function(request, *args, **kwargs):
        return redirect('under_construction')

    return _function


def staff_required(function):
    def wrapper(request, *args, **kwargs):
        if request.user.is_active and request.user.is_staff:
            return function(request, *args, **kwargs)
        else:
            return render(request, "403.html", status=403)

    return wrapper


def index(request):
    return render(request, "artax/dashboard.html")


def generate_qr_code(request, string_to_encode):
    qr = qrcode.QRCode(
        version=2,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=8,
        border=4,
    )
    qr.add_data(f"{request.get_host()}/{string_to_encode}")
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    response = HttpResponse(content_type="image/png")
    img.save(response, "PNG")
    return response


def download_qr_code(request, string_to_encode):
    qr_code_response = generate_qr_code(request, string_to_encode)
    qr_code_data = qr_code_response.content
    response = HttpResponse(content_type="image/png")
    response["Content-Disposition"] = f"attachment; filename=qr_code.png"
    response.write(qr_code_data)
    return response


def under_construction(request):
    return render(request, "artax/under-construction.html")


def faq(request):
    return render(request, "artax/faq.html")


def contact(request):
    return render(request, "artax/contact.html")


def blank(request):
    return render(request, "artax/blank.html")


# TODO 1 Users Handling ################################################################################################


def login_view(request):
    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")
        remember_me = request.POST.get("rememberMe")
        user = authenticate(request, username=username, password=password)

        if username == '' or password == '':
            messages.warning(request, "Please fill in all fields.")
            return redirect('login')
        # username doesn't exist or password incorrect.
        if user is None:
            messages.error(request, "Credentials given incorrect, please try again.")
            return redirect('login')
        else:
            if not remember_me:
                request.session.set_expiry(0)
            login(request, user)
            return redirect('profile')
    return render(request, "artax/login.html")


@staff_required
@login_required(login_url="login")
def new_user(request):
    if request.method == "POST":
        password = request.POST.get("password")
        pass_conf = request.POST.get("pwd_conf")

        if password != pass_conf:
            messages.error(request, "Password don't match. Please try again.")
            return redirect("register")
        try:
            user = User.objects.create_user(
                username=request.POST.get("username"),
                email=request.POST.get("email"),
                password=password,
                first_name=request.POST.get("first_name"),
                last_name=request.POST.get("last_name"),
                is_active=False,
            )
            token = default_token_generator.make_token(user)
            user_pk = user.pk
            uid = urlsafe_base64_encode(str(user_pk).encode("utf-8"))

            current_site = get_current_site(request)
            confirmation_link = f'{current_site.domain}/confirm/{uid}/{token}/'

            subject = 'Confirm your email'
            message = render_to_string('artax/email_confirmation_email.html', {
                'user': user,
                'confirmation_link': confirmation_link,
            })
            send_mail(subject, message, "email.the.artax.network@gmail.com", [user.email], html_message=message)
            user.save()
            role = request.POST.get("role")
            if role == '1':
                user.is_superuser = True
            elif role == '2':
                user.is_staff = True
                user.groups.add(Group.objects.get(name="Office Administrator"))
            elif role == '3':
                user.groups.add(Group.objects.get(name="Lawyer"))
            elif role == '4':
                user.groups.add(Group.objects.get(name="Visitor"))

            return render(request, "artax/email-verify-email.html")
        except IntegrityError:
            messages.error(
                request, "Username or email already in use, please try again with a new one or log in instead!")
        except SMTPRecipientsRefused:
            messages.error(
                request, "Email address given is unreachable. Please try again."
            )
            return redirect('register')
    return render(request, "artax/register.html")


def confirm_email(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode("utf-8")
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, ObjectDoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return render(request, 'artax/email_confirmed.html')
    else:
        return render(request, 'artax/email_confirmation_invalid.html')


@login_required(login_url="login")
def profile(request):
    if request.method == "POST":
        current_user = request.user
        current_user.first_name = request.POST.get("firstName")
        current_user.last_name = request.POST.get("lastName")
        current_user.job = request.POST.get("job")
        current_user.address = request.POST.get("address")
        current_user.phone = request.POST.get("phone")
        current_user.email = request.POST.get("email")
        current_user.about = request.POST.get("about")
        current_user.save()
    context = {}
    for user_group in request.user.groups.values_list('name', flat=True):
        context['clearance'] = user_group
    # print(context['clearance'])
    return render(request, "artax/users-profile.html", context=context)


@login_required(login_url="login")
def change_password(request):
    if request.method == "POST":
        current_password = request.POST.get("password")
        new_password = request.POST.get("new_password")
        renew_password = request.POST.get("renew_password")
        user = User.objects.filter(username=request.user.username).first()
        if new_password != renew_password:
            messages.error(request, "Password entered don't match. Please try again.")
            return redirect('profile')
        elif current_password == new_password:
            messages.error(request, "Password entered is the same as original. Please choose a new one and try again.")
            return redirect('profile')
        elif authenticate(request, username=user.username, password=current_password) is None:
            messages.error(request, 'Current password incorrect, please try again.')
            return redirect('profile')
        else:
            user.set_password(new_password)
            user.save()
            update_session_auth_hash(request, request.user)
            return redirect("profile")
    return redirect("profile")


@login_required(login_url="login")
def logout_view(request):
    logout(request)
    return redirect("login")


# TODO 2 Book Library ##################################################################################################

@login_required(login_url="login")
def all_books(request):
    page_obj = paginator_books(request, Book.objects.all())
    return render(request, "artax/all-books.html", {"page_obj": page_obj})


def paginator_books(request, books):
    page_number = request.GET.get('page')
    if request.GET.get("asc") == 'False':
        books = books[::-1]
    paginator = Paginator(books, PER_PAGE)
    page_obj = paginator.get_page(page_number)
    return page_obj


@permission_required("artax.change_book", raise_exception=True)
def remove_book_summary(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == 'POST':
        if book.summary:
            default_storage.delete(book.summary.path)
            book.summary = None
            book.save()
    return redirect('show_book', book_id=book_id)


@permission_required("artax.change_book", raise_exception=True)
def remove_book_cover(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == 'POST':
        if book.cover:
            default_storage.delete(book.cover.path)
            book.cover = None
            book.save()
    return redirect('show_book', book_id=book_id)


@permission_required("artax.change_book", raise_exception=True)
def change_book_summary(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    book_summary = request.FILES.get('bookSummary')
    if request.method == 'POST' and book_summary and book.summary == '':
        if book_summary.content_type != "application/pdf":
            messages.warning(request, "File type for image summary invalid.")
            return redirect("show_book", book_id=book_id)
        book.summary = book_summary
        book.save()
    return redirect('show_book', book_id=book_id)


@permission_required("artax.change_book", raise_exception=True)
def change_book_cover(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    book_cover = request.FILES.get("bookCover")
    if request.method == 'POST' and book_cover and book.cover == "":
        if book_cover.content_type != "image/png" and book_cover.content_type != "image/jpg" and book_cover.content_type != "image/jpeg":
            messages.warning(request, "File type for image cover invalid.")
            return redirect("show_book", book_id=book_id)
        book.cover = book_cover
        book.save()
    return redirect('show_book', book_id=book_id)


@login_required(login_url="login")
def new_book(request):
    book_record = Book.objects.all().last()
    if book_record is None:
        book_id = 1
    else:
        book_id = book_record.id + 1
    types, authors, locations, languages = Type.objects.all(), Author.objects.all(), Location.objects.all().order_by("code"), Language.objects.all()
    if request.method == "POST":
        if not request.user.has_perm("artax.add_book"):
            raise PermissionDenied
        else:
            if Book.objects.filter(title=request.POST.get("bookTitle")).first():
                messages.warning(request, "A book already exists with that title. Choose another one and try again.")
                return redirect('new_book')
            else:
                book_type = Type.objects.get(pk=request.POST.get("bookType"))
                special_id = f"{book_type.code}{Book.objects.filter(type=book_type).count() + 1}"

                purchase_date = request.POST.get("purchaseDate")
                if purchase_date == '':
                    purchase_date = None

                book_summary = request.FILES.get("bookSummary")
                book_cover = request.FILES.get("bookCover")

                if book_summary is not None and book_summary.content_type != "application/pdf":
                    messages.warning(request, "File type for summary invalid.")
                    return redirect("new_book")
                if book_cover is not None and book_cover.content_type != "image/png" and book_cover.content_type != "image/jpg" and book_cover.content_type != "image/jpeg":
                    messages.warning(request, "File type for image cover invalid.")
                    return redirect("new_book")

                new_book_record = Book(
                    lib_id=special_id,
                    author=Author.objects.get(pk=request.POST.get("authorName")),
                    title=request.POST.get("bookTitle"),
                    subject=request.POST.get("subject", None),
                    type=book_type,
                    section=request.POST.get("bookSection", None),
                    location=Location.objects.get(pk=request.POST.get("bookLocation")),
                    language=Language.objects.get(pk=request.POST.get("bookLanguage")),
                    summary=book_summary,
                    cover=book_cover,
                    publisher=request.POST.get("publisher"),
                    publishing_date=request.POST.get("publishingYear"),
                    purchase_date=purchase_date,
                    isbn=request.POST.get("isbn", None),
                    number_of_copies=request.POST.get("numberOfCopies"),
                    registrator=request.user,
                    last_editor=request.user,
                    last_edit_time=datetime.datetime.now(),
                )
                try:
                    new_book_record.save()
                except ValueError as error:
                    messages.warning(request, f"ValueError: {error}")
                    return redirect("new_book")
                except ValidationError as error:
                    messages.warning(request, f"ValidationError: {error}")
                    return redirect("new_book")
            return redirect("show_book", book_id=book_id)
    return render(request, "artax/new-book.html", {"book_id": book_id, "types": types, "locations": locations,
                                                   "authors": authors, "languages": languages,
                                                   "url_arg": f"{BASE_URL}books%2F{book_id}%2F"})


@login_required(login_url="login")
def book_queries(request):
    context = {
        "types": Type.objects.all(),
        "authors": Author.objects.all(),
        "locations": Location.objects.all(),
        "languages": Language.objects.all(),
    }
    return render(request, "artax/queries-books.html", context)

@login_required(login_url="login")
def query_books_by(request):
    book_query_param = request.GET.get("book_query_param")
    book_param = request.POST.get("name")
    print(RED, book_query_param, RESET)
    books = Book.objects.all()
    if book_query_param == "mfqf":
        filters = {
            "type": ("type__name__icontains", "type"),
            "location": ("location__code__icontains", "location"),
            "title": ("title__icontains", "title"),
            "content": ("subject__icontains", "content"),
            "language": ("language__code__icontains", "language"),
            "author": ("author__name__icontains", "author"),
            "publisher": ("publisher__icontains", "publisher"),
        }
        filter_params = {}
        for field, (lookup, param_name) in filters.items():
            value = request.POST.get(param_name)
            print(field)
            print(value)
            if value != "0" and str(value).strip() != "":
                filter_params[lookup] = value

        if filter_params:
            print(filter_params)
            books = books.filter(**filter_params)
    else:
        book = get_object_or_404(Book, lib_id=f"{book_param}{request.POST.get('name_id')}") if book_query_param == "special_id" else get_object_or_404(Book, pk=book_param)
        if book is None or book == []:
            return render(request, "artax/record-404.html", {'param': "book"})
        else:
            return redirect("show_book", book_id=book.id)

    if books.exists() is False:
        context = {'param': "book"}
        return render(request, "artax/record-404.html", context)
    else:
        page_obj = paginator_books(request, books)
        return render(request, "artax/all-books.html", {"page_obj": page_obj})


@login_required(login_url="login")
def show_book(request, book_id):
    book_record = get_object_or_404(Book, pk=book_id)
    types, authors, locations, languages = Type.objects.all(), Author.objects.all(), Location.objects.all(), Language.objects.all()
    if request.method == "POST":
        if not request.user.has_perm("artax.change_book"):
            raise PermissionDenied
        book_author = Author.objects.get(pk=request.POST.get("author"))
        book_location = Location.objects.get(pk=request.POST.get("location"))
        book_language = Language.objects.get(pk=request.POST.get("language"))
        book_record.author = book_author
        book_record.locations = book_location
        book_record.language = book_language
        book_record.title = request.POST.get("title")
        book_record.subject = request.POST.get("subject")
        book_record.section = request.POST.get("section")
        book_record.publisher = request.POST.get("publisher")
        book_record.publishing_date = request.POST.get("publishing_date")
        book_record.isbn = request.POST.get("isbn")
        book_record.number_of_copies = request.POST.get("numberOfCopies")
        book_record.last_edit_time = datetime.datetime.now()
        book_record.last_editor = request.user
        book_record.save()
    return render(request, "artax/record-book.html", {"book": book_record, "types": types, "locations": locations,
                                                      "authors": authors, "languages": languages,
                                                      "url_arg": f"{BASE_URL}books%2F{book_id}%2F"
                                                      })


@permission_required("artax.delete_book", raise_exception=True)
@login_required(login_url="login")
def delete_book(request, book_id):
    Book.objects.get(pk=book_id).delete()
    return redirect("all_books")


# TODO 3 File System ###################################################################################################

@redirect_view
@login_required(login_url="login")
def add_new_file(request):
    file_for_id = File.objects.all().last()
    if file_for_id is None:
        file_for_id = 1
    else:
        file_for_id = file_for_id.id + 1
    locations = Location.objects.all()
    clients = Client.objects.all()
    if request.method == "POST":
        new_file = File(
            client=Client.objects.get(pk=request.POST.get("client")),
            opponent=request.POST.get("opponent"),
            subject=request.POST.get("content"),
            sections=request.POST.get("sections"),
            location=Location.objects.get(pk=request.POST.get("location")),
        )
        new_file.save()
        return redirect("show_file", file_id=file_for_id)
    return render(request, "artax/new-file.html",
                  {"file_id": file_for_id, "clients": clients,
                   "locations": locations, "url_arg": f"{BASE_URL}files%2F{file_for_id}%2F"})


@redirect_view
@login_required(login_url="login")
def all_files(request):
    print(request)
    page_number = request.GET.get('page')
    files = File.objects.all()
    if request.GET.get("asc") == 'False':
        files = files[::-1]
    paginator = Paginator(files, PER_PAGE)
    page_obj = paginator.get_page(page_number)
    return render(request, "artax/all-files.html", {"page_obj": page_obj})


@redirect_view
@login_required(login_url="login")
def file_queries(request):
    clients = Client.objects.all()
    locations = Location.objects.all()
    return render(request, "artax/queries-files.html", {"clients": clients, "locations": locations})


@redirect_view
@login_required(login_url="login")
def query_files_by(request):
    print(RED, "Hello")
    file_query_param = request.GET.get("file_query_param")
    file_param = request.POST.get("name")
    print(file_param)
    print(file_query_param, RESET)
    if file_query_param == "client" or file_query_param == "location" or file_query_param == "subject":
        files = File.objects.filter(client__name__contains=file_param).all()
    elif file_query_param == "location":
        print("I am here")
        files = File.objects.filter(location__code__contains=file_param).all()
    elif file_query_param == "subject":
        files = File.objects.filter(subject__contains=file_param).all()
        print(RED, files, RESET)
    else:
        file = get_object_or_404(File, pk=file_param)
        return redirect(show_file, file_id=file.id)
    print("woho")
    return render(request, "artax/all-files.html", {"page_obj": files})


@redirect_view
@login_required(login_url="login")
def show_file(request, file_id):
    file_record = get_object_or_404(File, pk=file_id)
    clients, locations = Client.objects.all(), Location.objects.all()
    if request.method == "POST":
        client = Client.objects.get(pk=request.POST.get("client"))
        location = Location.objects.get(pk=request.POST.get("location"))
        file_record.opponent = request.POST.get("opponent")
        file_record.subject = request.POST.get("content")
        file_record.client = client
        file_record.sections = request.POST.get("sections")
        file_record.location = location
        file_record.save()
    return render(request, "artax/record-file.html", {"file": file_record, "clients": clients,
                                                      "locations": locations, "url_arg": f"{BASE_URL}files%2F{file_id}%2F"})


@redirect_view
@login_required(login_url="login")
def delete_file(request, file_id):
    print(request)
    File.objects.get(pk=file_id).delete()
    return redirect("all_files")


# TODO 4 Client System #################################################################################################

@redirect_view
@login_required(login_url="login")
def all_clients(request):
    page_number = request.GET.get('page')
    clients = Client.objects.all()
    if request.GET.get("asc") == 'False':
        clients = clients[::-1]
    paginator = Paginator(clients, PER_PAGE)
    page_obj = paginator.get_page(page_number)
    return render(request, "artax/all-clients.html", {"page_obj": page_obj})


@redirect_view
@login_required(login_url="login")
def new_client(request):
    return render(request, "artax/new-client.html")
