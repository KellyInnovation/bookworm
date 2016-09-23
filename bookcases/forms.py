from django import forms

from .models import Bookcase
from core.forms import BootstrapFormMixIn

class BookcaseForm(BootstrapFormMixIn, forms.ModelForm):

	class Meta:
		model = Bookcase
		fields = ('name', 'description', )

