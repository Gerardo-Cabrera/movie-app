import requests
from django.core.management.base import BaseCommand
from movies.models import Genre

class Command(BaseCommand):
    help = 'Load movie genres from the TMDb API'

    def handle(self, *args, **kwargs):
        url = "https://api.themoviedb.org/3/genre/movie/list?language=en"
        headers = {
            "accept": "application/json",
            "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI1YjE5MGUyYjljMTIzMjA1OThmYTgwZjZiMmMzZTNiNSIsIm5iZiI6MTcyNjg2MDcyNi4wMTI1ODksInN1YiI6IjY2ZWRjOTA2NWVlNjFmYmI3MzhjZjA4NCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.qeAs7FcqZ-FRxydC8Atl0lbfxgNC58rtWKNC4XnYjjw"
        }

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            genres_data = response.json().get("genres", [])

            for genre in genres_data:
                genre_id = genre["id"]
                name = genre["name"]

                _, created = Genre.objects.get_or_create(genre_id=genre_id, defaults={"name": name})

                if created:
                    self.stdout.write(self.style.SUCCESS(f"Genre {name} added."))
                else:
                    self.stdout.write(f"Genre {name} already exists.")
        else:
            self.stdout.write(self.style.ERROR(f"Error to get the genres: {response.status_code}"))
