from requests import get

u = get(
    'https://theartistunion.com/tracks/369375').content
with open('static/upload_files/music.wav', 'wb') as f:
    f.write(u)
