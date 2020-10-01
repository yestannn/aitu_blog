from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    FormView
)
from .models import Post, Comment, Friend
from users.models import Profile
from .forms import CommentForm


class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5



class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')

class UserDetail(DetailView):
    model = Profile

class ClubDetail(DetailView):
    model = Profile

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content', 'image']


    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDetailView(LoginRequiredMixin, DetailView):
    model = Post





def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    author = request.user
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = author
            comment.save()
            return redirect('post-detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'blog/add_comment_to_post.html', {'form': form})


@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.delete()
    return redirect('post-detail', pk=comment.post.pk)

def home(request):
    posts =  Post.objects.all().order_by('-date_posted')
    context = {
        'posts': posts
        }

    return render(request, 'blog/home.html', context)

def change_friends(request, operation, pk):
    friend = User.objects.get(pk=pk)
    if operation == 'add':
        Friend.make_friend(request.user, friend)
    elif operation == 'remove':
        Friend.lose_friend(request.user, friend)
    return redirect('blog-about')

def about(request):
    try:
        friend = get_object_or_404(Friend, current_user = request.user)
        friends = friend.users.all()
        if friends:
            text = "Your following"
        else:
            text = "You don't follow to people"
        context = {
            'posts': User.objects.all(),
            'friends' : friends,
            'text': text,
            }
    except:
        text = "You don't follow to people"
        context = {
            'text': text,
            }
    return render(request, 'blog/about.html', context)

def following_post(request):
    try:
        friend = get_object_or_404(Friend, current_user = request.user)
        friends = friend.users.all()
        if friends:
            text = "Your following"
        else:
            text = "You don't follow to people"
        context = {
        'friends' : friends,
        'posts': Post.objects.all().order_by('-date_posted'),
        'text' : text
        }
    except:
        text = "You don't follow to people"
        context = {
        'text' : text,
        'posts': Post.objects.all().order_by('-date_posted'),
        }
    return render(request, 'blog/following_posts.html', context)

def clubs_list(request):

    clubs = Profile.objects.filter(is_user = 'club')
    text = 'List of clubs and organizations'
    context = {
        'clubs':clubs,
        'text':text
        }
    return render(request, 'blog/clubs.html', context)
