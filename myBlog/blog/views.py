from django.shortcuts import render
from .models import Post, Comment, Like
from django.contrib.auth.models import User
from .form import PostForm, CommentForm
from django.shortcuts import redirect
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt


# Create your views here.
def home(request):
    posts = Post.objects.order_by("-id")[:6]
    return render(request, 'home.html', {'posts': posts})


def post_list(request):
    posts = Post.objects.all()
    if request.user.is_authenticated:
        posts = posts.filter(author=request.user)
    return render(request, 'posts.html', {'posts': posts})


def users(request):
    user_list = User.objects.all()
    return render(request, 'users.html', {'users': user_list})


def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            form = CommentForm()
            return render(request, 'post_detail.html', {'form': form, 'post': post})
    else:
        form = PostForm()
    return render(request, 'post_edit.html', {'form': form})


def post_page(request, **kwargs):
    post = Post.objects.get(pk=kwargs['pk'])
    comments = Comment.objects.filter(post_id=post.id)
    form = CommentForm()
    is_liked = False
    if request.user.is_authenticated:
        is_liked = post.likes.filter(author_id=request.user.id).exists()
    return render(request, 'post_page.html', {'post': post, 'comments': comments, 'form': form, 'is_liked': is_liked})


def comment_new(request):
    '''

    :param request:
    :return:
    '''
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = Post.objects.get(pk=request.POST['post_pk'])
            comment.save()
            return redirect('post_page', pk=comment.post_id)
    return redirect('home')


def contact_page(request):
    return render(request, 'contact_page.html')


@csrf_exempt
def post_like(request, **kwargs):
    if request.method == "POST" and request.user.is_authenticated:
        post = Post.objects.get(pk=kwargs['pk'])
        like, created = Like.objects.get_or_create(author=request.user, post=post)
        if not created:
            like.delete()
    elif not request.user.is_authenticated:
        return redirect('login')
    return post_page(request, **kwargs)
