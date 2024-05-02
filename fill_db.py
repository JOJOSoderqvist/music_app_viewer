from faker import Faker
import psycopg2
import random
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv('db_config.env')

DEFAULT_RATE = 100
EXTENDED_RATE = 1000000

fake = Faker("ru_RU")
Faker.seed(0)

conn = psycopg2.connect(dbname=os.getenv('DB_NAME'), user=os.getenv('DB_USER'), password=os.getenv('DB_PASSWORD'),
                        host=os.getenv('DB_HOST'))
cursor = conn.cursor()

# GENRES
genres_set = set(fake.unique.text(max_nb_chars=10)[:-1] for i in range(DEFAULT_RATE))
# cursor.executemany("INSERT INTO genres (name) VALUES (%s)", genres_set)
for genre in genres_set:
    cursor.execute("INSERT INTO genres (name) VALUES (%s)", (genre,))
conn.commit()

# USERS
unique_users = set()
for i in range(DEFAULT_RATE):
    unique_users.add((fake.unique.user_name(), fake.unique.email(), fake.password()))

cursor.executemany("INSERT INTO app_user (username, email, password) VALUES (%s, %s, %s)", unique_users)
conn.commit()

# ARTISTS
unique_artists = set()
for i in range(DEFAULT_RATE):
    unique_artists.add((fake.unique.user_name(), fake.date(), fake.name()))

cursor.executemany("INSERT INTO artist (nick_name, date_of_birth, real_name) VALUES (%s, %s, %s)", unique_artists)
conn.commit()

# ALBUMS
unique_albums = []
for i in range(DEFAULT_RATE):
    unique_albums.append(
        (random.randint(1, 100), fake.text(max_nb_chars=20)[:-1], random.randint(300, 2000), fake.date()))

cursor.executemany("INSERT INTO albums (artist_id, name, duration, release_date) VALUES (%s, %s, %s, %s)",
                   unique_albums)
conn.commit()

songs = []
# SONGS
for i in range(EXTENDED_RATE):
    random_album = random.randint(1, 100)
    songs.append((random.choice([random_album, None]), random.randint(1, 100), fake.text(max_nb_chars=20)[:-1],
                  random.randint(30, 240), fake.text(max_nb_chars=1000), fake.date(), random.randint(0, 500)))

# cursor.executemany(
#     "INSERT INTO songs (album_id, artist_id, name, duration, text, release_date, number_of_auditions) VALUES (%s, %s, %s, %s, %s, %s, %s)",
#     songs)
for song in songs:
    cursor.execute(
        "INSERT INTO songs (album_id, artist_id, name, duration, text, release_date, number_of_auditions) VALUES (%s, %s, %s, %s, %s, %s, %s)",
        song)
conn.commit()

# PLAYLISTS

playlists = []
for i in range(DEFAULT_RATE):
    playlists.append((random.randint(1, 100), fake.text(max_nb_chars=20)[:-1], fake.text(max_nb_chars=255),
                      fake.date_between_dates(date_start=datetime(2020, 1, 1), date_end=datetime(2024, 12, 31)),
                      random.choice([True, False])))

cursor.executemany(
    "INSERT INTO playlist (user_id, name, description, creation_date, state) VALUES (%s, %s, %s, %s, %s)", playlists)
conn.commit()

# PLAYLIST_SONGS
playlist_songs = set()
for i in range(DEFAULT_RATE * 2):
    playlist_songs.add((random.randint(1, 100), random.randint(1, EXTENDED_RATE)))

cursor.executemany("INSERT INTO playlist_songs (playlist_id, song_id) VALUES (%s, %s)", playlist_songs)

conn.commit()
# ALBUMS_GENRES
albums_genres = set()
for i in range(DEFAULT_RATE * 2):
    albums_genres.add((random.randint(1, 100), random.randint(1, 100)))

cursor.executemany("INSERT INTO albums_genres (album_id, genre_id) VALUES (%s, %s)", albums_genres)
conn.commit()

# SONGS_GENRES
songs_genres = set()
for i in range(DEFAULT_RATE * 2):
    songs_genres.add((random.randint(1, EXTENDED_RATE), random.randint(1, 100)))

cursor.executemany("INSERT INTO songs_genres (song_id, genre_id) VALUES (%s, %s)", songs_genres)
conn.commit()

conn.close()
print('SUCCESS')
