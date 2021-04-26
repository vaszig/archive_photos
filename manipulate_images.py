import imghdr
from datetime import datetime
from pathlib import Path

import requests

from countries_abbreviation import countries


errors = {
    'no_files': [],
    'wrong_file_format': [], 
    'directory': [],
    'no_exif_data': [],
    'datetime_original': [], 
    'gps_latitude': [], 
    'gps_longitude': [], 
    'same_files': []
}


def is_image(image_path):
    """Returns True or False depending on whether a file is a type of image or not."""
    try:
        type_of_image = imghdr.what(image_path)
    except IsADirectoryError:
        errors['directory'].append(image_path.stem)
        return False
    if type_of_image:
        return True
    return False


def list_image_paths(source):
    """Returns a list with paths of images according to the given source path."""
    images_paths = []
    for image_path in source.iterdir():
        # if file_is_image(image_path):
        images_paths.append(source / image_path)            
    return images_paths


def convert_coordinates_to_decimal(coordinates, coordinates_ref):
    """Converts latitude and longitude to decimal degrees."""
    decimal_degrees = coordinates[0] + coordinates[1] / 60 + coordinates[2] / 3600
    if coordinates_ref == "S" or coordinates_ref == "W":
        decimal_degrees = -decimal_degrees
    return decimal_degrees


def fetch_exif_data(image_obj):
    """Returns a dictionary of exif data needed."""
    exif_data = {}
    exif_data['datetime_original'] = image_obj.get('datetime_original', datetime.strftime(datetime.now(), '%Y:%m:%d %H:%M:%S'))
    exif_data['gps_latitude'] = image_obj.get('gps_latitude')
    exif_data['gps_latitude_ref'] = image_obj.get('gps_latitude_ref')
    exif_data['gps_longitude'] = image_obj.get('gps_longitude')
    exif_data['gps_longitude_ref'] = image_obj.get('gps_longitude_ref')
    breakpoint()
    return exif_data


def filter_exif_data(exif_data):
    """Returns a new dictionary with the existed types of exif data."""
    filtered_exif_data = {}
    expected = ['datetime_original', 'gps_latitude', 'gps_latitude_ref', 'gps_longitude', 'gps_longitude_ref']

    for key, value in exif_data.items():
        if key in expected:
            filtered_exif_data[key] = value
    return filtered_exif_data


def get_gps_location(gps_latitude, gps_latitude_ref, gps_longitude, gps_longitude_ref):
    """Uses third party api and fetches the location."""
    gps_location = {}
    latitude = convert_coordinates_to_decimal(gps_latitude, gps_latitude_ref)
    longitude = convert_coordinates_to_decimal(gps_longitude, gps_longitude_ref)

    try:
        response = requests.get(f'https://geo-info.co/{latitude},{longitude}')
    except requests.exceptions.RequestException as e:
        raise SystemExit(e)
    
    results = response.json()
        
    gps_location['city'] = results.get('city')
    gps_location['country'] = next(country['Name'] for country in countries if country['Code'] == results.get('country')) 
    
    return gps_location
 


