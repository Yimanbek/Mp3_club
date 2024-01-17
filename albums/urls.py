from django.urls import path
from .views import AlbumCreateView,AlbumDetailView,AlbumListView

urlpatterns = [
    path('create/', AlbumCreateView.as_view()),
    path('detail/<int:pk>/', AlbumDetailView.as_view()),
    path('list/', AlbumListView.as_view()),
]
