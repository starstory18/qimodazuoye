from django.db import models


# Create models here.
class Song(models.Model):
    song_name = models.CharField(max_length=1000)
    artist = models.CharField(max_length=1000)
    album_name = models.CharField(max_length=1000)
    album_photo = models.TextField(max_length=1000)
    lyrics = models.TextField(max_length=10000)
    comment = models.TextField(max_length=10000)
    song_play = models.CharField(max_length=1000)
    artist_photo = models.TextField(max_length=1000)
    artist_intro = models.TextField(max_length=10000)

    def __str__(self):
        values = [
            self.song_name,
            self.artist,
            self.album_name,
            self.album_photo,
            self.lyrics,
            self.comment,
            self.song_play,
            self.artist_photo,
            self.artist_intro
        ]
        return ','.join(map(str, values)) + '\n'
