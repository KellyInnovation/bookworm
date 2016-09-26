from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.db.models import Q

from .models import Book, Author

def book_list(request):
	books = Book.objects.all()

	breadcrumbs = (
		("Books", ),
	)

	query = request.GET.get('q')
	if query:
		authors = Author.objects.filter(name__icontains=query)
		books = books.filter(
			Q(title__icontains=query) |
			Q(authors__in=authors)
		)
		books = books.distinct()

	context = {
		"books": books,
		"breadcrumbs": breadcrumbs,
	}

	return render(request, "books/book_list.html", context)

def book_detail(request, id):
	
	book = get_object_or_404(Book, pk=id)

	context = {
		"book": book,
	}


	return render(request, "books/book_detail.html", context)