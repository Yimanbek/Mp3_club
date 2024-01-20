from django.urls import path
from .views import MusicView,music_website,MusicDetailView,sort_website,filter_music_by_album,MusicOutputView


urlpatterns = [
    #PostMan
    path('create/',MusicView.as_view()),
    path('music/<int:pk>/like/', MusicOutputView.as_view({'post': 'like', 'delete': 'like',})),
    path('music/',MusicOutputView.as_view({'get': 'list'})),
    path('delete/<int:pk>/', MusicDetailView.as_view()),

    #HTML.CSS
    path('music-website/', music_website,name = 'music_website'),
    path('sort/', sort_website, name='sort_website'),
    path('sort_album/',filter_music_by_album, name = 'sort_album')
]