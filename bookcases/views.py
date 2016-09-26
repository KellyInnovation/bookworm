from django.shortcuts import render, get_object_or_404, redirect
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.db.models import Count
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import Bookcase, Bookshelf
from .forms import BookcaseForm, BookshelfForm


def bookcase_list(request):
	bookcases = Bookcase.objects.annotate(shelf_count=Count('bookshelf')).all()

	breadcrumbs = (
		("Bookcases",),
	)

	context = {
		"bookcases": bookcases,
		"breadcrumbs": breadcrumbs,
	}
	return render(request, "bookcases/bookcase_list.html", context)

@login_required
def bookcase_new(request):
	if request.method == "POST":
		form = BookcaseForm(request.POST)
		if form.is_valid():
			bookcase = form.save()
			message.success(request, "Bookcase created!")
			return redirect("bookcases:bookcase_detail", id=bookcase.pk)
	else:
		form = BookcaseForm()

	context = {
		"form": form,
	}

	return render(request, "bookcases/bookcase_edit.html", context)

@login_required
def bookcase_edit(request, id):
	bookcase = get_object_or_404(Bookcase, pk=id)

	if request.method == "POST":
		form = BookcaseForm(request.POST, instance=bookcase)
		if form.is_valid():
			bookcase = form.save()
			message.success(request, "Bookcase updated!")
			return redirect("bookcases:bookcase_detail", id=bookcase.pk)
	else:
		form = BookcaseForm(instance=bookcase)

	context = {
		"form": form,
		"bookcase": bookcase,
	}

	return render(request, "bookcases/bookcase_edit.html", context)

def bookcase_detail(request, id):
	bookcase = get_object_or_404(Bookcase, pk=id)
	bookshelves = bookcase.bookshelf_set.annotate(book_count=Count('book')).all()

	breadcrumbs = (
		("Bookcases", reverse("bookcases:bookcase_list"),),
		(bookcase.name,),
	)

	context = {
		"bookcase": bookcase,
		"bookshelves": bookshelves,
		"breadcrumbs": breadcrumbs,
	}

	return render(request, "bookcases/bookcase_detail.html", context)


def bookshelf_detail(request, id):
	query_set = Bookshelf.objects.annotate(book_count=Count('book'))
	query_set = query_set.select_related('bookcase')
	bookshelf = get_object_or_404(query_set, pk=id)
	books = bookshelf.book_set.prefetch_related('authors').all()

	breadcrumbs = (
		("Bookcases", reverse("bookcases:bookcase_list"),),
		(bookshelf.bookcase.name, reverse("bookcases:bookcase_detail", args=[bookshelf.bookcase.pk])),
		(bookshelf.shelf_label,),
	)

	context = {
		"bookshelf": bookshelf,
		"books": books,
		"breadcrumbs": breadcrumbs,
	}

	return render(request, "bookcases/bookshelf_detail.html", context)

@login_required
def bookshelf_new(request, bookcase_id):
	bookcase = get_object_or_404(Bookcase, pk=bookcase_id)

	if request.method == "POST":
		form = BookshelfForm(request.POST)

		if form.is_valid():
			bookshelf = form.save(commit=False)
			bookshelf.bookcase = bookcase
			bookshelf.save()

			messages.success(request, "Bookshelf created!")

			return redirect("bookcases:bookshelf_detail", id=bookshelf.pk)
	else:
		form = BookshelfForm()

	context = {
		"form": form,
	}

	return render(request, "bookcases/bookshelf_edit.html", context)

@login_required
def bookshelf_edit(request, id):
	bookshelf = get_object_or_404(Bookshelf, pk=id)

	if request.method == "POST":
		form = BookshelfForm(request.POST, instance=bookshelf)

		if form.is_valid():
			bookshelf = form.save()

			messages.success(request, "Bookshelf updated!")

			return redirect("bookcases:bookshelf_detail", id=bookshelf.pk)
	else:
		form = BookshelfForm(instance=bookshelf)

	context = {
		"form": form,
	}

	return render(request, "bookcases/bookshelf_edit.html", context)
