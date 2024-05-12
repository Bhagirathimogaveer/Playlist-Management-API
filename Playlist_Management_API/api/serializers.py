# serializers.py
from rest_framework import serializers
from .models import Song, Playlist,PlaylistSong

class SongSerializer(serializers.ModelSerializer):
    class Meta:
        model = Song
        fields = '__all__'

class PlaylistSongSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlaylistSong
        fields = ['position']


class PlaylistSerializer(serializers.ModelSerializer):
    songs = serializers.PrimaryKeyRelatedField(queryset=Song.objects.all(), many=True)

    class Meta:
        model = Playlist
        fields = ['id', 'name', 'songs']

    def create(self, validated_data):
        songs_data = validated_data.pop('songs')
        playlist = Playlist.objects.create(**validated_data)
        for song_data in songs_data:
            playlist.songs.add(song_data)
        return playlist
