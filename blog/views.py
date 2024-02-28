from django.contrib.auth.views import LogoutView
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView
from .models import (ContentCategory, Content, UserComment)
from django.views.generic.edit import (FormMixin, CreateView)
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CommentForm
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
import logging

logger = logging.getLogger(__name__)

try:
    class CategoryListView(ListView):
        # ListView to display a list of content categories
        model = ContentCategory
        template_name = 'blog/category_list.html'
        context_object_name = 'categories'


    class CategoryDetailView(DetailView):
        # DetailView to display details of a specific content category
        model = ContentCategory
        template_name = 'blog/category_detail.html'
        context_object_name = 'category'

        def get_context_data(self, **kwargs):
            # Add contents related to this category to the context
            context = super().get_context_data(**kwargs)
            context['contents'] = Content.objects.filter(category=self.object)
            return context


    class ContentListView(ListView):
        # ListView to display a list of contents
        model = Content
        template_name = 'blog/content_list.html'
        context_object_name = 'contents'


    class ContentDetailView(LoginRequiredMixin, FormMixin, DetailView):
        # DetailView for displaying details of a specific content along with comment functionality
        model = Content
        template_name = 'blog/content_detail.html'
        context_object_name = 'content'
        form_class = CommentForm
        login_url = 'blog:login'
        redirect_field_name = 'next'

        def get_context_data(self, **kwargs):
            # Add comments and comment form to the context
            context = super().get_context_data(**kwargs)
            context['comments'] = UserComment.objects.filter(
                content=self.object, enabled=True, approved_by_admin=True)
            context['form'] = self.get_form()
            return context

        def post(self, request, *args, **kwargs):
            # Handle form submission for comments
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
            # Save the valid comment and display success message
            form.instance.user = self.request.user
            form.instance.content = self.object
            form.instance.enabled = False
            form.instance.approved_by_admin = False
            form.save()

            messages.success(self.request, 'Your comment is pending approval.')
            return super().form_valid(form)

        def form_invalid(self, form):
            # Display error message for invalid form submission
            messages.error(self.request, 'Error submitting the comment.')
            return super().form_invalid(form)

        def get_success_url(self):
            # Redirect to the content detail page after form submission
            return reverse_lazy('blog:content_detail', kwargs={'pk': self.object.pk})


    class CustomLoginView(LoginView):
        # Customized LoginView to handle successful login with additional message
        template_name = 'registration/login.html'

        def form_valid(self, form):
            response = super().form_valid(form)
            if self.request.user.is_authenticated:
                messages.success(
                    self.request, 'Your comment was submitted successfully')
                return response

        def get_success_url(self):
            # Redirect to the content list page after successful login
            return reverse_lazy('blog:content_list')


    class SignUpView(CreateView):
        # View for user registration
        form_class = UserCreationForm
        success_url = reverse_lazy('blog:login')
        template_name = 'registration/signup.html'


    class CustomLogoutView(LogoutView):
        # Customized LogoutView to display a custom template after logout
        template_name = 'registration/logged_out.html'
except Exception as e:
        logger.error(f"Error in some_function: {str(e)}")