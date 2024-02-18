from django.views.generic import ListView, DetailView
from .models import ContentCategory, Content, UserComment

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

class ContentDetailView(DetailView):
    model = Content
    template_name = 'blog/content_detail.html'
    context_object_name = 'content'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = UserComment.objects.filter(content=self.object, enabled=True, approved_by_admin=True)
        return context
