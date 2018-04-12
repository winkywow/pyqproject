from django.urls import path
from . import views

app_name = 'pyq'
urlpatterns = [
    path('<str:user_sid>', views.index, name='index'),
    path('<str:user_sid>/post_add', views.post_add, name='post_add'),
    path('<str:user_sid>/<int:post_id>/post_delete', views.post_delete, name='post_delete'),
    path('<str:user_sid>/<int:post_id>/post_edit', views.post_edit, name='post_edit'),
    path('<str:user_sid>/<int:post_id>/post_edit_add', views.post_edit_add, name='post_edit_add'),
]
