from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from ckeditor.fields import RichTextField
from taggit.managers import TaggableManager
from django.urls import reverse

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Kategoriya nomi")
    slug = models.SlugField(unique=True, verbose_name="Slug")
    image = models.ImageField(upload_to='categories/', blank=True, null=True, verbose_name="Rasm")
    description = models.TextField(blank=True, null=True, verbose_name="Tavsif")
    created_date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Kategoriya"
        verbose_name_plural = "Kategoriyalar"
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('category_posts', args=[self.slug])

class Game(models.Model):
    title = models.CharField(max_length=200, verbose_name="O'yin nomi")
    slug = models.SlugField(unique=True, verbose_name="Slug")
    developer = models.CharField(max_length=200, verbose_name="Developer")
    publisher = models.CharField(max_length=200, blank=True, null=True, verbose_name="Publisher")
    release_date = models.DateField(verbose_name="Chiqish sanasi")
    image = models.ImageField(upload_to='games/', verbose_name="Rasm")
    description = RichTextField(verbose_name="Tavsif")
    platform = models.CharField(max_length=100, blank=True, null=True, verbose_name="Platforma")
    website = models.URLField(blank=True, null=True, verbose_name="Rasmiy sayt")
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "O'yin"
        verbose_name_plural = "O'yinlar"
        ordering = ['-release_date']
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('game_detail', args=[self.slug])

class Post(models.Model):
    title = models.CharField(max_length=200, verbose_name="Sarlavha")
    slug = models.SlugField(unique=True, verbose_name="Slug")
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Muallif")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Kategoriya")
    game = models.ForeignKey(Game, on_delete=models.CASCADE, blank=True, null=True, verbose_name="O'yin")
    content = RichTextField(verbose_name="Matn")
    image = models.ImageField(upload_to='posts/', verbose_name="Asosiy rasm")
    tags = TaggableManager(blank=True, verbose_name="Teglar")
    views = models.IntegerField(default=0, verbose_name="Ko'rishlar soni")
    created_date = models.DateTimeField(default=timezone.now, verbose_name="Yaratilgan sana")
    published_date = models.DateTimeField(blank=True, null=True, verbose_name="Chop etilgan sana")
    updated_date = models.DateTimeField(auto_now=True, verbose_name="Yangilangan sana")
    is_featured = models.BooleanField(default=False, verbose_name="Maxsus post")
    
    class Meta:
        verbose_name = "Post"
        verbose_name_plural = "Postlar"
        ordering = ['-published_date']
    
    def publish(self):
        self.published_date = timezone.now()
        self.save()
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('post_detail', args=[self.slug])

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments', verbose_name="Post")
    name = models.CharField(max_length=80, verbose_name="Ism")
    email = models.EmailField(verbose_name="Email")
    body = models.TextField(verbose_name="Izoh")
    created_date = models.DateTimeField(default=timezone.now, verbose_name="Yaratilgan sana")
    active = models.BooleanField(default=True, verbose_name="Faol")
    
    class Meta:
        verbose_name = "Izoh"
        verbose_name_plural = "Izohlar"
        ordering = ['-created_date']
    
    def __str__(self):
        return f"{self.name} - {self.post.title}"

class Contact(models.Model):
    name = models.CharField(max_length=100, verbose_name="Ism")
    email = models.EmailField(verbose_name="Email")
    subject = models.CharField(max_length=200, verbose_name="Mavzu")
    message = models.TextField(verbose_name="Xabar")
    created_date = models.DateTimeField(auto_now_add=True, verbose_name="Yuborilgan sana")
    is_read = models.BooleanField(default=False, verbose_name="O'qildi")
    
    class Meta:
        verbose_name = "Aloqa"
        verbose_name_plural = "Aloqa xabarlari"
        ordering = ['-created_date']
    
    def __str__(self):
        return f"{self.name} - {self.subject}"