from django.contrib import admin
from .models import Category, Game, Post, Comment, Contact

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'created_date']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']

@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ['title', 'developer', 'release_date', 'created_date']
    prepopulated_fields = {'slug': ('title',)}
    list_filter = ['release_date', 'platform']
    search_fields = ['title', 'developer']

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'category', 'views', 'published_date', 'is_featured']
    prepopulated_fields = {'slug': ('title',)}
    list_filter = ['category', 'published_date', 'is_featured']
    search_fields = ['title', 'content']
    raw_id_fields = ['author']
    date_hierarchy = 'published_date'
    actions = ['publish_posts']
    
    def publish_posts(self, request, queryset):
        for post in queryset:
            post.publish()
    publish_posts.short_description = "Tanlangan postlarni chop etish"

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['name', 'post', 'created_date', 'active']
    list_filter = ['active', 'created_date']
    search_fields = ['name', 'email', 'body']
    actions = ['approve_comments']
    
    def approve_comments(self, request, queryset):
        queryset.update(active=True)
    approve_comments.short_description = "Tanlangan izohlarni faollashtirish"

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'created_date', 'is_read']
    list_filter = ['is_read', 'created_date']
    search_fields = ['name', 'email', 'subject', 'message']
    actions = ['mark_as_read']
    
    def mark_as_read(self, request, queryset):
        queryset.update(is_read=True)
    mark_as_read.short_description = "Tanlangan xabarlarni o'qilgan deb belgilash"