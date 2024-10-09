from django.shortcuts import render, get_object_or_404,redirect
from django.views.generic import ListView, DetailView, CreateView
from django.core.paginator import Paginator
from django.contrib.postgres.search import TrigramSimilarity
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from .models import Post, Comment
from .forms import CommentForm, EmailPostForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.http import JsonResponse
from taggit.managers import TaggableManager
from django.db.models import Q 


class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        query = self.request.GET.get('q')  
        if query:
            return Post.objects.filter(
                Q(title__icontains=query) | Q(tags__name__icontains=query)
            ).distinct() 
        return Post.objects.all()
    
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = post.comments.all()
    form = CommentForm()

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('post_detail', pk=post.pk)

    return render(request, 'blog/post_detail.html', {'post': post, 'comments': comments, 'form': form})

def like_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    
    if request.user in comment.likes.all():
        comment.likes.remove(request.user)  
        liked = False
    else:
        comment.likes.add(request.user) 
        liked = True
    return JsonResponse({'liked': liked, 'total_likes': comment.total_likes()})


def add_comment(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('post_detail', pk=pk)


def share_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    sent = False
    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = post.title
            subject = f"{cd['name']} recommends you read {post.title}"
            message = f"Read {post.title} at {post_url}\n\n{cd['name']}\'s comments: {cd['comments']}"
            send_mail(subject, message, 'admin@yopmail.com', [cd['to']])
            sent = True
    else:
        form = EmailPostForm()
    return render(request, 'blog/share_post.html', {'post': post, 'form': form, 'sent': sent})

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('post_list') 
    else:
        form = UserCreationForm()
    return render(request, 'blog/signup.html', {'form': form})

from django.contrib.auth.decorators import login_required
@login_required
def profile_view(request):
    return render(request, 'blog/profile.html')



