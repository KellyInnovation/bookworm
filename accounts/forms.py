from django.contrib.auth.forms import AuthenticationForm

from core.forms import BootstrapFormMixIn

class LoginForm(BootstrapFormMixIn, AuthenticationForm):
	pass