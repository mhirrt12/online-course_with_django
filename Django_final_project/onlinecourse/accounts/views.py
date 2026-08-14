from django.shortcuts import render, redirect
from .forms import RegistrationForm


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()

            return redirect('register')

    else:
        form = RegistrationForm()

    return render(request, 'accounts/register.html', {'form': form})

def login(request):
   return render(request, 'accounts/login.html')