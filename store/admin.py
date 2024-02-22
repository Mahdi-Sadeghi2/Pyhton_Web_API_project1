# store/admin.py
from django.contrib import admin
from .models import Category, Product, Image, Video, UserComment

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'description','price')
    search_fields = ('id', 'name', 'category',)
    list_filter = ('category', 'name', 'price',)

@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ('image',)

@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('video',)

@admin.register(UserComment)
class UserCommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'comment_text', 'enabled', 'approved_by_admin')
    search_fields = ('id', 'user', 'product',)
    list_filter = ('product', 'user',)
    
    
    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def approve_comments(self, request, queryset):
    # Custom action to approve selected comments
        updated_count = queryset.update(approved_by_admin=True)
        self.message_user(request, f'Successfully approved {updated_count} comments.')
    approve_comments.short_description = "Approve selected comments"

class UserCommentInline(admin.TabularInline):
    model = UserComment
    

class ContentAdmin(admin.ModelAdmin):
    inlines = [UserCommentInline]