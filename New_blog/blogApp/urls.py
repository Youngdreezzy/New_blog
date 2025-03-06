from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('add_blog/', add_blog, name='add_blog'),
    path('blog/<int:blog_id>/', view_blog, name='view_blog'),
    path('delete-blog/<int:blog_id>/', deleteBlog, name="delete-blog"),
    path('edit-blog/<int:blog_id>/', editBlog, name="edit-blog"),
    path('view-all-blogs/', viewAllBlogs , name="view-all-blogs"), 
    path('approve-reject-blog/<int:blog_id>/<str:action>/', approve_reject_blog, name='approve-reject-blog'),
    path('color-combinations/', color_combinations, name='color-combinations'),
    path('blog/<int:blog_id>/comment/', add_comment, name='add_comment'),
    path('like/<int:blog_id>/', like_blog, name='like_blog'),
    path('trending/', trending_styles, name='trending'),
    path('comment/<int:comment_id>/delete/', delete_comment, name='delete_comment'),

]
