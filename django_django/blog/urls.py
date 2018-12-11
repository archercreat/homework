from blog import views
from django.urls import path

app_name = 'blog'

urlpatterns = [
    path('', views.IndexView.as_view(), name='blog'),
    path('<int:pk>/', views.PostView.as_view(), name='detail'),
    path('<int:pk>/add_comment', views.CommentAdd.as_view(), name='add_comment'),
    path('add_post', views.PostAdd.as_view(), name='add_post'),
]
