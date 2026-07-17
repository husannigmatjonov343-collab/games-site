from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, Count
from .models import Post, Category, Game, Comment
from .forms import CommentForm, ContactForm, RegisterForm, SearchForm, GameForm, PostForm

def home(request):
    """Bosh sahifa"""
    featured_posts = Post.objects.filter(is_featured=True, published_date__isnull=False)[:3]
    latest_posts = Post.objects.filter(published_date__isnull=False).order_by('-published_date')[:6]
    popular_posts = Post.objects.filter(published_date__isnull=False).order_by('-views')[:5]
    featured_games = Game.objects.all()[:6]
    categories = Category.objects.annotate(post_count=Count('post'))[:8]
    
    context = {
        'featured_posts': featured_posts,
        'latest_posts': latest_posts,
        'popular_posts': popular_posts,
        'featured_games': featured_games,
        'categories': categories,
    }
    return render(request, 'index.html', context)

def post_list(request):
    """Barcha postlar ro'yxati"""
    posts_list = Post.objects.filter(published_date__isnull=False).order_by('-published_date')
    
    # Kategoriya bo'yicha filter
    category_slug = request.GET.get('category')
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        posts_list = posts_list.filter(category=category)
    
    # Qidiruv
    query = request.GET.get('q')
    if query:
        posts_list = posts_list.filter(
            Q(title__icontains=query) | 
            Q(content__icontains=query) |
            Q(category__name__icontains=query)
        )
    
    # Pagination
    paginator = Paginator(posts_list, 9)  # 9 ta post har bir sahifada
    page = request.GET.get('page')
    posts = paginator.get_page(page)
    
    # Kategoriyalar (sidebar uchun)
    categories = Category.objects.annotate(post_count=Count('post')).filter(post_count__gt=0)
    
    context = {
        'posts': posts,
        'categories': categories,
        'query': query,
    }
    return render(request, 'post_list.html', context)

def post_detail(request, slug):
    """Bitta postni ko'rsatish"""
    post = get_object_or_404(Post, slug=slug, published_date__isnull=False)
    
    # Ko'rishlar sonini oshirish
    post.views += 1
    post.save()
    
    # Izohlar
    comments = post.comments.filter(active=True)
    
    # Izoh formasi
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            messages.success(request, 'Izohingiz qabul qilindi!')
            return redirect('post_detail', slug=post.slug)
    else:
        form = CommentForm()
    
    # O'xshash postlar
    related_posts = Post.objects.filter(
        category=post.category, 
        published_date__isnull=False
    ).exclude(id=post.id)[:3]
    
    context = {
        'post': post,
        'comments': comments,
        'form': form,
        'related_posts': related_posts,
    }
    return render(request, 'post_detail.html', context)

def category_posts(request, slug):
    """Kategoriya bo'yicha postlar"""
    category = get_object_or_404(Category, slug=slug)
    posts_list = Post.objects.filter(category=category, published_date__isnull=False).order_by('-published_date')
    
    paginator = Paginator(posts_list, 9)
    page = request.GET.get('page')
    posts = paginator.get_page(page)
    
    context = {
        'category': category,
        'posts': posts,
    }
    return render(request, 'index_category.html', context)

def game_list(request):
    """Barcha o'yinlar ro'yxati"""
    games_list = Game.objects.all().order_by('-release_date')
    
    # Qidiruv
    query = request.GET.get('q')
    if query:
        games_list = games_list.filter(
            Q(title__icontains=query) | 
            Q(developer__icontains=query)
        )
    
    paginator = Paginator(games_list, 12)
    page = request.GET.get('page')
    games = paginator.get_page(page)
    
    context = {
        'games': games,
        'query': query,
    }
    return render(request, 'game_list.html', context)

def game_detail(request, slug):
    """Bitta o'yin haqida"""
    game = get_object_or_404(Game, slug=slug)
    posts = Post.objects.filter(game=game, published_date__isnull=False).order_by('-published_date')[:5]
    
    context = {
        'game': game,
        'posts': posts,
    }
    return render(request, 'game_detail.html', context)

def search(request):
    """Qidiruv sahifasi"""
    form = SearchForm(request.GET or None)
    posts = []
    games = []
    
    if form.is_valid():
        query = form.cleaned_data.get('query')
        if query:
            posts = Post.objects.filter(
                Q(title__icontains=query) | 
                Q(content__icontains=query) |
                Q(category__name__icontains=query)
            ).filter(published_date__isnull=False).distinct()
            
            games = Game.objects.filter(
                Q(title__icontains=query) | 
                Q(developer__icontains=query) |
                Q(description__icontains=query)
            ).distinct()
    
    context = {
        'form': form,
        'posts': posts,
        'games': games,
    }
    return render(request, 'search.html', context)

def contact(request):
    """Aloqa sahifasi"""
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Xabaringiz yuborildi! Tez orada javob beramiz.')
            return redirect('contact')
    else:
        form = ContactForm()
    
    context = {'form': form}
    return render(request, 'contact.html', context)

def register(request):
    """Ro'yxatdan o'tish"""
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Ro\'yxatdan muvaffaqiyatli o\'tdingiz! Tizimga kiring.')
            return redirect('login')
    else:
        form = RegisterForm()
    
    context = {'form': form}
    return render(request, 'register.html', context)

@login_required
def profile(request):
    """Foydalanuvchi profili"""
    user_posts = Post.objects.filter(author=request.user).order_by('-published_date')
    
    context = {
        'user_posts': user_posts,
    }
    return render(request, 'profile.html', context)


def profile(request):
    return render(request, 'profile.html')
