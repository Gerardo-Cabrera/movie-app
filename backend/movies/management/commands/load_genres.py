import requests
from django.conf import settings
from django.core.management.base import BaseCommand
from movies.models import Genre

class Command(BaseCommand):
    help = 'Load movie genres from the TMDB API'

    def handle(self):
        api_url = settings.API_URL_TMDB_GENRES_MOVIES
        api_key_tmdb = settings.API_KEY_TMDB
        api_key = f"api_key={api_key_tmdb}"
        url = f"{api_url}{api_key}"
        response = requests.get(url)

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
