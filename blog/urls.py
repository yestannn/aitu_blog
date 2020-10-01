from django.urls import path
from django.views.decorators.http import  require_POST
from .views import (PostListView,
                    PostDetailView,
                    PostCreateView,
                    PostUpdateView,
                    PostDeleteView,
                    UserPostListView,
                    UserDetail,
                    ClubDetail
                    )
from . import views

urlpatterns = [
    path('', PostListView.as_view(), name='blog-home'),
    path('user/<str:username>', UserPostListView.as_view(), name='user-posts'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('profile/<int:pk>/', UserDetail.as_view(), name='user-detail'),
    path('post/<int:pk>/update', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete', PostDeleteView.as_view(), name='post-delete'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('about/', views.about, name='blog-about'),
    path('following_post/', views.following_post, name='following-post'),
    path('post/<int:pk>/comment/', views.add_comment_to_post, name='add_comment_to_post'),
    path('comment/<int:pk>/remove/', views.comment_remove, name='comment_remove'),
    path('connect/<operation>./<int:pk>/', views.change_friends, name='change_friends'),
    path('clubs/', views.clubs_list, name='clubs'),
    path('clubs/<int:pk>/', ClubDetail.as_view(template_name = 'blog/club_detail.html'), name = 'club-detail'),
]
