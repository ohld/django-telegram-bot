from arcgis.models import Arcgis
from dtb.celery import app


@app.task(ignore_result=True)
def save_data_from_arcgis(latitude, longitude, location_id):
    Arcgis.from_json(Arcgis.reverse_geocode(latitude, longitude), location_id=location_id)