# urls.py
from django.urls import path
from .views import (
    SongListCreate, SongRetrieveUpdateDestroy,
    PlaylistListCreate, PlaylistRetrieveUpdateDestroy,
    PlaylistSongsAPIView,PlaylistSongMoveAPIView
)


urlpatterns = [
    path('api/songs/', SongListCreate.as_view(), name='song-list-create'),
    path('api/songs/<int:pk>/', SongRetrieveUpdateDestroy.as_view(), name='song-detail'),
    path('api/playlists/', PlaylistListCreate.as_view(), name='playlist-list-create'),
    path('api/playlists/<int:pk>/', PlaylistRetrieveUpdateDestroy.as_view(), name='playlist-detail'),
    path('api/playlists/<int:playlist_id>/songs/', PlaylistSongsAPIView.as_view(), name='playlist-songs'),
    path('api/playlists/<int:playlist_id>/songs/<int:song_id>/', PlaylistSongMoveAPIView.as_view(), name='playlist-song-remove'),

]
