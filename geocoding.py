from geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent="123")
location = geolocator.geocode("Пермь, ул Петропавловская, 117")

print((location.latitude, location.longitude))
