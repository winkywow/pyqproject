from django.urls import path
from . import views

app_name = 'pyq'
urlpatterns = [
    path('<int:user_id>', views.index, name='index'),
    path('<int:user_id>/post_add', views.post_add, name='post_add'),
    path('<int:user_id>/<int:post_id>/post_delete', views.post_delete, name='post_delete'),
    path('<int:user_id>/<int:post_id>/post_edit', views.post_edit, name='post_edit'),
    path('<int:user_id>/<int:post_id>/post_edit_add', views.post_edit_add, name='post_edit_add'),
]
