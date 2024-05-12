from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from .models import Song, Playlist,PlaylistSong
from .serializers import SongSerializer, PlaylistSerializer,PlaylistSongSerializer
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q

class CustomPagination(PageNumberPagination):
    page_size = 10
    page_query_param = 'page'
    max_page_size = 100

class SongListCreate(generics.ListCreateAPIView):
    queryset = Song.objects.all()
    serializer_class = SongSerializer
    pagination_class = CustomPagination

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response({"Success. The song entry has been created"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get_queryset(self):
        queryset = super().get_queryset()
        q = self.request.query_params.get('q')
        if q:
            queryset = queryset.filter(Q(name__icontains=q) | Q(artist__icontains=q))
        return queryset

class SongRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Song.objects.all()
    serializer_class = SongSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        queryset = super().get_queryset()
        q = self.request.query_params.get('q')
        if q:
            queryset = queryset.filter(Q(name__icontains=q) | Q(artist__icontains=q))
        return queryset

class PlaylistListCreate(generics.ListCreateAPIView):
    queryset = Playlist.objects.all()
    serializer_class = PlaylistSerializer
    pagination_class = CustomPagination

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response({"Success. The playlist entry has been created"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get_queryset(self):
        queryset = super().get_queryset()
        q = self.request.query_params.get('q')
        if q:
            queryset = queryset.filter(Q(name__icontains=q) | Q(artist__icontains=q))
        return queryset

class PlaylistRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Playlist.objects.all()
    serializer_class = PlaylistSerializer
    pagination_class = CustomPagination

    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"Success. The name of the playlist has been edited"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"Success. The playlist has been deleted"}, status=status.HTTP_200_OK)
    
class PlaylistSongsAPIView(generics.ListAPIView):
    serializer_class = SongSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        playlist_id = self.kwargs['playlist_id']
        try:
            playlist = Playlist.objects.get(pk=playlist_id)
            return playlist.songs.all()
        except Playlist.DoesNotExist:
            return []
    
class PlaylistSongMoveAPIView(generics.ListAPIView):
    serializer_class = SongSerializer
    pagination_class = CustomPagination

    
    def delete(self, request, *args, **kwargs):
        try:
            playlist_id = self.kwargs['playlist_id']
            song_id = self.kwargs['song_id']

            playlist = Playlist.objects.get(pk=playlist_id)
            song = Song.objects.get(pk=song_id)
            playlist.songs.remove(song)

            return Response({"Success. Song has been removed from the playlist"}, status=status.HTTP_200_OK)

        except (Playlist.DoesNotExist, Song.DoesNotExist):
            return Response({"Error. Playlist or Song not found."}, status=status.HTTP_404_NOT_FOUND)


    def get_queryset(self):
        queryset = super().get_queryset()
        q = self.request.query_params.get('q')
        if q:
            queryset = queryset.filter(Q(name__icontains=q) | Q(artist__icontains=q))
        return queryset



class PlaylistSongMoveAPIView(generics.UpdateAPIView):
    queryset = PlaylistSong.objects.all()
    serializer_class = PlaylistSongSerializer
    lookup_field = 'playlist_id' 
    

    def delete(self, request, *args, **kwargs):
            try:
                playlist_id = self.kwargs['playlist_id']
                song_id = self.kwargs['song_id']

                playlist = Playlist.objects.get(pk=playlist_id)
                song = Song.objects.get(pk=song_id)
                playlist.songs.remove(song)

                return Response({"Success. Song has been removed from the playlist"}, status=status.HTTP_200_OK)

            except (Playlist.DoesNotExist, Song.DoesNotExist):
                return Response({"Error. Playlist or Song not found."}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, *args, **kwargs):
        try:
            playlist_id = self.kwargs['playlist_id']
            song_id = self.kwargs['song_id']
            new_position = request.data.get('position')  # Get the new position from request data
            
            playlist = Playlist.objects.get(pk=playlist_id)
            song = Song.objects.get(pk=song_id)

           
            # Remove the song from the playlist to reposition it
            playlist.songs.remove(song)

            # Reinsert the song at the new position
            playlist.songs.add(song, through_defaults={'position': new_position})

            return Response({"Success. Song has been moved to the new position in the playlist"}, status=status.HTTP_200_OK)

        except (Playlist.DoesNotExist, Song.DoesNotExist):
            return Response({"Error. Playlist or Song not found."}, status=status.HTTP_404_NOT_FOUND)
        

        