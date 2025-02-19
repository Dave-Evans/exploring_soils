from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.shortcuts import reverse
from django.views.generic import TemplateView, FormView
from django.conf import settings
from .models import Book
from .forms import BookForm, ContactForm

# TODO
# Add 'user' to model and filter by that in list


def home(request):

    return render(request, "home.html")


@login_required
def book_list(request):
    books = Book.objects.all()
    books = books.order_by("finished_date")
    return render(request, "books/book_list.html", {"books": books})


@login_required
def book_delete(request, pk):
    book = get_object_or_404(Book, pk=pk)
    data = dict()
    if request.method == "POST":
        book.delete()
        data["form_is_valid"] = (
            True  # This is just to play along with the existing code
        )
        books = Book.objects.all()
        data["html_book_list"] = render_to_string(
            "books/includes/partial_book_list.html", {"books": books}
        )
    else:
        context = {"book": book}
        data["html_form"] = render_to_string(
            "books/includes/partial_book_delete.html",
            context,
            request=request,
        )
    return JsonResponse(data)


def save_book_form(request, form, template_name):
    data = dict()
    if request.method == "POST":
        if form.is_valid():
            form.save()
            data["form_is_valid"] = True
            books = Book.objects.all()
            data["html_book_list"] = render_to_string(
                "books/includes/partial_book_list.html", {"books": books}
            )
        else:
            data["form_is_valid"] = False
    context = {"form": form}
    data["html_form"] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


@login_required
def book_create(request):
    if request.method == "POST":
        form = BookForm(request.POST)
    else:
        form = BookForm()
    return save_book_form(request, form, "books/includes/partial_book_create.html")


def book_update(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == "POST":
        form = BookForm(request.POST, instance=book)
    else:
        form = BookForm(instance=book)
    return save_book_form(request, form, "books/includes/partial_book_update.html")


class SuccessView(TemplateView):
    template_name = "success.html"


class ContactView(FormView):
    form_class = ContactForm
    template_name = "contact.html"

    def get_success_url(self):
        return reverse("success")

    def form_valid(self, form):
        email = form.cleaned_data.get("email")
        subject = form.cleaned_data.get("subject")
        message = form.cleaned_data.get("message")

        full_message = f"""
            Received message below from {email}, {subject}
            ________________________


            {message}
            """
        send_mail(
            subject="Received contact form submission",
            message=full_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.NOTIFY_EMAIL],
        )
        return super(ContactView, self).form_valid(form)
