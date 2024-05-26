#gis/adress_processor.py

import time
import logging
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError

from apps.masterclasses.models import MasterClass

# Настройка логгирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AddressProcessor:
    def __init__(self, user_agent="RussianF"):
        self.geolocator = Nominatim(user_agent=user_agent)
        self.geocode = self.geolocator.geocode

    def process_address(self, address):
        """Converts address to latitude and longitude."""
        try:
            logger.info(f"Processing address: {address}")
            location = self.geocode(address)
            if location:
                logger.info(f"Coordinates for '{address}' found: (lat: {location.latitude}, lon: {location.longitude})")
                return location.latitude, location.longitude
            else:
                logger.warning(f"No coordinates found for '{address}'.")
                return None, None
        except (GeocoderTimedOut, GeocoderServiceError) as e:
            logger.error(f"Geocoding error: {e}. Retrying...")
            time.sleep(1)
            return self.process_address(address)  # Рекурсивная попытка в случае ошибки
        except Exception as e:
            logger.error(f"An unexpected error occurred: {e}.")
            return None, None

    def process_addresses_in_database(self):
        """Fetches addresses from the database, geocodes them, and updates their coordinates."""
        for event in MasterClass.objects.filter(latitude__isnull=True, longitude__isnull=True).exclude(location_name__exact=''):
            lat, lon = self.process_address(event.location_name)
            if lat and lon:
                event.latitude = lat
                event.longitude = lon
                event.save()
                logger.info(f"Updated MasterClass '{event.title}' with coordinates: (lat: {lat}, lon: {lon})")
            time.sleep(1)  # Задержка между запросами

