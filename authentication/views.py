from django.contrib.auth import login
from django.shortcuts import redirect, render

from . import forms


def signup_page(request):
    form = forms.SignupForm()
    if request.method == 'POST':
        form = forms.SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            # auto-login user
            login(request, user)
            return redirect('logout')
    return render(request, 'authentication/signup.html', context={'form': form})
