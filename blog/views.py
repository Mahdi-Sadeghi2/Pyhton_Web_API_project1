
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView
from .models import ContentCategory, Content, UserComment
from django.views.generic.edit import FormMixin, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CommentForm
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
class CategoryListView(ListView):
    model = ContentCategory
    template_name = 'blog/category_list.html'
    context_object_name = 'categories'

class CategoryDetailView(DetailView):
    model = ContentCategory
    template_name = 'blog/category_detail.html'
    context_object_name = 'category'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['contents'] = Content.objects.filter(category=self.object)
        return context

class ContentListView(ListView):
    model = Content
    template_name = 'blog/content_list.html'
    context_object_name = 'contents'

class ContentDetailView(LoginRequiredMixin,FormMixin, DetailView):
    model = Content
    template_name = 'blog/content_detail.html'
    context_object_name = 'content'
    form_class = CommentForm
    login_url = 'login'  
    redirect_field_name = 'next'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = UserComment.objects.filter(content=self.object, enabled=True, approved_by_admin=True)
        context['form'] = self.get_form()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

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
        return reverse_lazy('blog:content_detail', kwargs={'pk': self.object.pk})
    

class CustomLoginView(LoginView):
    template_name = 'registration/login.html'

    def form_valid(self, form):
        response = super().form_valid(form)
        if self.request.user.is_authenticated:
            self.success_url = reverse_lazy('blog:content_list')
            messages.success(self.request, 'Your comment was submitted successfully')
            return response

    


class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('blog:login')
    template_name = 'registration/signup.html'