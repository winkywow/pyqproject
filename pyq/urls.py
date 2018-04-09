from django.urls import path
from . import views

app_name = 'pyq'
urlpatterns = [
    path('<int:user_id>', views.index, name='index'),
    path('<int:user_id>/post_add', views.post_add, name='post_add'),
]
