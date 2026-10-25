from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
#from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import Profile
from shop.models import Order


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)  # <-- CHANGED HERE
        if form.is_valid():
            user = form.save()
            return redirect('login')
    else:
        form = CustomUserCreationForm()  # <-- CHANGED HERE

    return render(request, 'accounts/register.html', {'form': form})


@login_required  # This enforces LoginRequiredMixin behaviour
def profile(request):
    # Fetch the user's orders (newest first)
    orders = Order.objects.filter(user=request.user).order_by('-created_at')

    return render(request, 'accounts/profile.html', {'orders': orders})