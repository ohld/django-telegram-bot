import requests
from django.db import models

# Create your models here.
from tgbot.models import Location
from utils.models import CreateTracker


class Arcgis(CreateTracker):
    location = models.OneToOneField(Location, on_delete=models.CASCADE, primary_key=True)

    match_addr = models.CharField(max_length=200)
    long_label = models.CharField(max_length=200)
    short_label = models.CharField(max_length=128)

    addr_type = models.CharField(max_length=128)
    location_type = models.CharField(max_length=64)
    place_name = models.CharField(max_length=128)

    add_num = models.CharField(max_length=50)
    address = models.CharField(max_length=128)
    block = models.CharField(max_length=128)
    sector = models.CharField(max_length=128)
    neighborhood = models.CharField(max_length=128)
    district = models.CharField(max_length=128)
    city = models.CharField(max_length=64)
    metro_area = models.CharField(max_length=64)
    subregion = models.CharField(max_length=64)
    region = models.CharField(max_length=128)
    territory = models.CharField(max_length=128)
    postal = models.CharField(max_length=128)
    postal_ext = models.CharField(max_length=128)

    country_code = models.CharField(max_length=32)

    lng = models.DecimalField(max_digits=21, decimal_places=18)
    lat = models.DecimalField(max_digits=21, decimal_places=18)

    def __str__(self):
        return f"{self.location}, city: {self.city}, country_code: {self.country_code}"

    @classmethod
    def from_json(cls, j, location_id):
        a = j.get("address")
        l = j.get("location")

        if "address" not in j or "location" not in j:
            return

        arcgis_data = {
            "match_addr": a.get("Match_addr"),
            "long_label": a.get("LongLabel"),
            "short_label": a.get("ShortLabel"),
            "addr_type": a.get("Addr_type"),
            "location_type": a.get("Type"),
            "place_name": a.get("PlaceName"),
            "add_num": a.get("AddNum"),
            "address": a.get("Address"),
            "block": a.get("Block"),
            "sector": a.get("Sector"),
            "neighborhood": a.get("Neighborhood"),
            "district": a.get("District"),
            "city": a.get("City"),
            "metro_area": a.get("MetroArea"),
            "subregion": a.get("Subregion"),
            "region": a.get("Region"),
            "territory": a.get("Territory"),
            "postal": a.get("Postal"),
            "postal_ext": a.get("PostalExt"),
            "country_code": a.get("CountryCode"),
            "lng": l.get("x"),
            "lat": l.get("y")
        }

        arc, _ = cls.objects.update_or_create(location_id=location_id, defaults=arcgis_data)
        return

    @staticmethod
    def reverse_geocode(lat, lng):
        r = requests.post(
            "https://geocode.arcgis.com/arcgis/rest/services/World/GeocodeServer/reverseGeocode",
            params={
                'f': 'json',
                'location': f'{lng}, {lat}',
                'distance': 50000,
                'outSR': '',
            },
            headers={
                'Content-Type': 'application/json',
            }
        )
        return r.json()