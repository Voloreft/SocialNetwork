from requests import get, post

print(get('http://localhost:5000/api/picture').json())
