from django.contrib import admin
from .models import *
from .serializers import AdminPostSerializer
models = [UserProfile,Like,Comment,Follow]

for model in models:
    admin.site.register(model)



@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'description', 'user_id')  # Customize the columns you want to display
    list_display_links = ('id', 'title')  # Add clickable links to specific fields
    list_filter = ('user',)  # Add filters if needed
    search_fields = ('title', 'description')  # Add search fields

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user')  # Optimize database queries

    def get_serializer(self, request, obj=None):
        return AdminPostSerializer()

    def user_id(self, obj):
        return obj.user.id

    user_id.short_description = 'User ID'    

