from django.shortcuts import render, get_object_or_404, redirect
from django.views import View

from main.models import Category, Ad
from users.models import User


class HomeView(View):
    def get(self, request):
        if request.user.in_login():
            categories = Category.objects.all()
            ads = Ad.objects.all()
            context = {
                'categories': categories,
                'ads': ads,
            }
            return render(request, 'index.html', context)
        return render(request, 'index-unauth.html')


class CategoryView(View):
    def get(self, request, slug):
        if request.user.in_login():
            category = get_object_or_404(Category, slug=slug)
            context = {
                'category': category,
            }
            return render(request, 'category.html', context)
        return redirect('login')
