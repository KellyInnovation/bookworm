from django import forms

from .models import Bookcase, Bookshelf
from core.forms import BootstrapFormMixIn

class BookcaseForm(BootstrapFormMixIn, forms.ModelForm):

	class Meta:
		model = Bookcase
		fields = ('name', 'description', )

class BookshelfForm(BootstrapFormMixIn, forms.ModelForm):

	class Meta:
		model = Bookshelf
		fields = ('shelf_label', )