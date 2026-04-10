from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Product
from .forms import ProductForm

def register_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect("register")
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists")
            return redirect("register")

        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        messages.success(request, "Account created successfully")
        return redirect("login")

    return render(request, "register.html")

def login_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            user_obj = User.objects.get(email=email)
            username = user_obj.username
        except User.DoesNotExist:
            messages.error(request, "Invalid email or password")
            return redirect("login")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)  # session created
            return redirect("dashboard")
        else:
            messages.error(request, "Invalid credentials")

    return render(request, "login.html")

def logout_view(request):
    logout(request)
    return redirect("login")

def dashboard_view(request):
    if not request.user.is_authenticated:
        return redirect("login")
    return render(request, "dashboard.html")

def home(request):
    if not request.user.is_authenticated:
        return redirect("login")
    products = Product.objects.all()
    context = {
        'products': products,
    }
    return render(request, 'home.html', context)

def add_product(request):
    if not request.user.is_authenticated:
        return redirect("login")
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f"Product '{form.cleaned_data['name']}' added successfully!")
            return redirect('product')
    else:
        form = ProductForm()
    
    return render(request, 'add_product.html', {'form': form})

def edit_product(request, pk):
    if not request.user.is_authenticated:
        return redirect("login")
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, f"Product '{form.cleaned_data['name']}' updated successfully!")
            return redirect('product')
    else:
        form = ProductForm(instance=product)
    
    return render(request, 'edit_product.html', {'form': form, 'product': product})

def delete_product(request, pk):
    if not request.user.is_authenticated:
        return redirect("login")
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        messages.success(request, f"Product '{product.name}' deleted successfully!")
        return redirect('product')
    return render(request, 'delete_product.html', {'product': product})