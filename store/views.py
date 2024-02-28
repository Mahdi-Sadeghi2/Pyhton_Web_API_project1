from django.shortcuts import render
from django.contrib.auth.views import LogoutView
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import (ListView, DetailView)
from .forms import CommentForm
from .models import (Category, Product, UserComment)
from django.views.generic.edit import (FormMixin, CreateView)
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
import logging
# View for listing product categories
logger = logging.getLogger(__name__)


class CategoryListView(ListView):
    model = Category
    template_name = 'store/category_list.html'
    context_object_name = 'categories'

    # Add logging to the view

    def get(self, request, *args, **kwargs):
        try:
            return super().get(request, *args, **kwargs)
        except Exception as e:
            logger.error(f"Error in CategoryListView: {str(e)}")
            messages.error(
                request, 'An error occurred while retrieving categories.')
            return HttpResponseRedirect(reverse_lazy('home'))

# View for displaying details of a specific product category


class CategoryDetailView(DetailView):
    model = Category
    template_name = 'store/category_detail.html'
    context_object_name = 'category'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = Product.objects.filter(category=self.object)
        return context


# View for listing all products
class ProductListView(ListView):
    model = Product
    template_name = 'store/product_list.html'
    context_object_name = 'products'


# View for displaying details of a specific product with comment functionality
class ProductDetailView(LoginRequiredMixin, FormMixin, DetailView):
    model = Product
    template_name = 'store/product_detail.html'
    context_object_name = 'product'
    form_class = CommentForm
    login_url = 'store:login'
    redirect_field_name = 'next'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = UserComment.objects.filter(
            product=self.object, enabled=True, approved_by_admin=True)
        context['form'] = self.get_form()
        context['media'] = self.object.media

        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if self.request.user.is_authenticated:
            if form.is_valid():
                return self.form_valid(form)
            else:
                return self.form_invalid(form)
        else:
            messages.error(
                self.request, 'You must be logged in to submit a comment.')
            return HttpResponseRedirect(self.get_success_url())

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.content = self.object
        form.instance.enabled = False
        form.instance.approved_by_admin = False
        form.save()

        messages.success(self.request, 'Your comment is pending approval.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Error submitting the comment.')
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse_lazy('store:category_detail', kwargs={'pk': self.object.pk})


# Custom login view with additional logic
class CustomLoginView(LoginView):
    template_name = 'registration/login.html'
    # success_url = reverse_lazy('store:product_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        if self.request.user.is_authenticated:
            # self.success_url = reverse_lazy('blog:content_detail')
            messages.success(
                self.request, 'Your comment was submitted successfully')
            return response

    def get_success_url(self):
        return reverse_lazy('store:product_list')


# View for user registration
class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('store:login')
    template_name = 'registration/signup.html'


# Custom logout view with redirection
class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('store/login')
    template_name = 'registration/logged_out.html'


# Home view rendering the home.html template
def home(request):
    return render(request, 'home.html')
