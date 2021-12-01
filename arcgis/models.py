from typing import Dict

import requests
from django.db import models

# Create your models here.
from tgbot.models import Location
from utils.models import CreateTracker, GetOrNoneManager


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

    objects = GetOrNoneManager()

    def __str__(self):
        return f"{self.location}, city: {self.city}, country_code: {self.country_code}"

    @classmethod
    def from_json(cls, arcgis_json: Dict, location_id: int) -> None:
        address, location = arcgis_json.get("address"), arcgis_json.get("location")

        if "address" not in arcgis_json or "location" not in arcgis_json:
            return

        arcgis_data = {
            "match_addr": address.get("Match_addr"),
            "long_label": address.get("LongLabel"),
            "short_label": address.get("ShortLabel"),
            "addr_type": address.get("Addr_type"),
            "location_type": address.get("Type"),
            "place_name": address.get("PlaceName"),
            "add_num": address.get("AddNum"),
            "address": address.get("Address"),
            "block": address.get("Block"),
            "sector": address.get("Sector"),
            "neighborhood": address.get("Neighborhood"),
            "district": address.get("District"),
            "city": address.get("City"),
            "metro_area": address.get("MetroArea"),
            "subregion": address.get("Subregion"),
            "region": address.get("Region"),
            "territory": address.get("Territory"),
            "postal": address.get("Postal"),
            "postal_ext": address.get("PostalExt"),
            "country_code": address.get("CountryCode"),
            "lng": location.get("x"),
            "lat": location.get("y")
        }

        arc, _ = cls.objects.update_or_create(location_id=location_id, defaults=arcgis_data)
        return

    @staticmethod
    def reverse_geocode(lat: float, lng: float) -> Dict:
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
