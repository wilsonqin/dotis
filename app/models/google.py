from googlemaps import GoogleMaps
gmaps = GoogleMaps('AIzaSyAkn5QGLQ5p5VqZ5ov2JN8e-cvwv6SEs50')
address = 'Constitution Ave NW & 10th St NW, Washington, DC'
lat, lng = gmaps.address_to_latlng(address)
print lat, lng