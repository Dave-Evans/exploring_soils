from django import forms
from .models import Book

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ('title', 'publication_date', 'finished_date', 'author', 'pages', 'book_type', 'description', 'completed' )

