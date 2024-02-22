from django.contrib import admin
from .models import ContentCategory, Content, Image, Video, UserComment


# Register your models here.

@admin.register(ContentCategory)
class ContentCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('id',)

@admin.register(Content)
class ContentAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'description')
    search_fields = ('id', 'title', 'category',)
    list_filter = ('category', 'title',)

@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ('image',)

@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('video',)

@admin.register(UserComment)
class UserCommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'content', 'comment_text', 'enabled', 'approved_by_admin')
    list_filter = ('enabled', 'approved_by_admin')
    search_fields = ('id', 'user',)

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