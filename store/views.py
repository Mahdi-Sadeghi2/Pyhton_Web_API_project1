from urllib.parse import urlencode
from django.contrib import messages
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView

from .forms import CommentForm
from .models import Category, Product, UserComment
from django.views.generic.edit import FormMixin, CreateView
# from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
class CategoryListView(ListView):
    model = Category
    template_name = 'store/category_list.html'
    context_object_name = 'categories'


class CategoryDetailView(DetailView):
    model = Category
    template_name = 'store/category_detail.html'
    context_object_name = 'category'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = Product.objects.filter(category=self.object)
        return context


class ProductListView(ListView):
    model = Product
    template_name = 'store/product_list.html'
    context_object_name = 'products'

class ProductDetailView(LoginRequiredMixin, FormMixin, DetailView):
    model = Product
    template_name = 'store/product_detail.html'
    context_object_name = 'product'
    form_class = CommentForm
    login_url = 'login'  # Set this to the URL of your login page
    redirect_field_name = 'next'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = UserComment.objects.filter(product=self.object, enabled=True, approved_by_admin=True)
        context['form'] = self.get_form()
        context['images'] = self.object.image_gallery.all()
        context['videos'] = self.object.image_gallery.all()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if not self.request.user.is_authenticated:
            # Redirect to login page with a message and 'next' parameter
            login_url = reverse('login')
            query_string = urlencode({'next': self.request.path})
            redirect_url = f"{login_url}?{query_string}"
            messages.error(self.request, 'You must be logged in to add a comment.')
            return HttpResponseRedirect(redirect_url)

        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.product = self.object
        form.instance.enabled = False
        form.instance.approved_by_admin = False
        form.save()

        self.object.user_comments.add(form.instance)
        messages.success(self.request, 'Your comment is pending approval.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Error submitting the comment.')
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse_lazy('store:product_detail', kwargs={'pk': self.object.pk})
    

# class CustomLoginView(LoginView):
#     template_name = 'registration/login.html'
#     success_url = reverse_lazy('store:product_list')

#     def form_valid(self, form):
#         response = super().form_valid(form)
#         if self.request.user.is_authenticated:
#             messages.success(self.request, 'Your comment was submitted successfully')
#             return response

    


# class SignUpView(CreateView):
#     form_class = UserCreationForm
#     success_url = reverse_lazy('store:login')
#     template_name = 'registration/signup.html'

# class AddToCartView(View):
#     def post(self, request, *args, **kwargs):
#         product_id = self.kwargs.get('pk')
#         quantity = request.POST.get('quantity', 1) 

#         product = get_object_or_404(Product, pk=product_id)

        
#         cart = request.session.get('cart', {})
#         cart[product.id] = {'quantity': quantity, 'name': product.name, 'price': product.price}
#         request.session['cart'] = cart

#         return JsonResponse({'message': 'Product added to cart successfully'})


