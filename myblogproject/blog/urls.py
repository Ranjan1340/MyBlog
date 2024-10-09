from django.urls import path
from .views import PostListView, post_detail, add_comment, like_comment, share_post,profile_view

urlpatterns = [
    path('', PostListView.as_view(), name='post_list'),
    # path('post/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('post/<int:pk>/comment/', add_comment, name='add_comment'),
    path('comment/<int:pk>/like/', like_comment, name='like_comment'),
    path('post/<int:pk>/share/', share_post, name='share_post'),
    path('post/<int:pk>/', post_detail, name='post_detail'),
    path('like-comment/<int:comment_id>/', like_comment, name='like_comment'),
    path('profile/', profile_view, name='profile'),

]
