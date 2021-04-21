import imghdr
from datetime import datetime
from pathlib import Path

import requests
from exif import Image

from countries_abbreviation import countries


errors = {
    'wrong_file_format': [], 
    'directory': [],
    'no_exif_data': [],
    'datetime_original': [], 
    'gps_latitude': [], 
    'gps_longitude': [], 
    'same_files': []
}


def file_is_image(image_path):
    '''Returns True or False depending on whether a file is a type of image or not.'''
    try:
        type_of_image = imghdr.what(image_path)
    except IsADirectoryError:
        errors['directory'].append(image_path.stem)
        return False
    if type_of_image:
        return True
    errors['wrong_file_format'].append(image_path.stem)
    return False


def list_images_paths(source):
    '''Returns a list with paths of images.'''
    images_paths = []
    for image_path in source.iterdir():
        if file_is_image(image_path):
            images_paths.append(source / image_path)            
    return images_paths


def read_images(images_paths):
    '''Reads image files and returns a dictionary with path as key and an object of read image as value.'''
    images = {}
    for image_path in images_paths:
        with open(image_path, "rb") as image_file:
            image = Image(image_file)
            images[image_path] = image
    return images


def convert_coordinates_to_decimal(coordinates, coordinates_ref):
    '''Converts latitude and longitude to decimal degrees.'''
    decimal_degrees = coordinates[0] + coordinates[1] / 60 + coordinates[2] / 3600
    if coordinates_ref == "S" or coordinates_ref == "W":
        decimal_degrees = -decimal_degrees
    return decimal_degrees


def type_of_exif_data_exists(image_path, image_obj, type):
    '''Returns True or False depending on whether the type of exif data exists or not.'''
    if image_obj.get(type) is None:
        errors[type].append(image_path.stem)
        return False
    return True



def fetch_exif_data(images_objs):
    '''Returns a dictionary of exif data when they exist. The key is image's path and the value a dictionary with the exif data.'''
    exif_data = {}
    
    for image_path, image_obj in images_objs.items():
        obj_data = {}
        if not image_obj.has_exif:
            errors['no_exif_data'].append(image_path.stem)
            continue

        if not type_of_exif_data_exists(image_path, image_obj, 'datetime_original'):
            obj_data['date'] = datetime.strftime(datetime.today(), '%Y:%m:%d %H:%M:%S')
        else:
            obj_data['date'] = image_obj['datetime_original']
        
        if type_of_exif_data_exists(image_path, image_obj, 'gps_latitude') and type_of_exif_data_exists(image_path, image_obj, 'gps_longitude'):
            latitude = convert_coordinates_to_decimal(image_obj['gps_latitude'], image_obj.gps_latitude_ref)
            longitude = convert_coordinates_to_decimal(image_obj['gps_longitude'], image_obj.gps_longitude_ref)
            
            response = requests.get(f'https://geo-info.co/{latitude},{longitude}')
            results = response.json()
            
            obj_data['city'] = results.get('city')
            obj_data['country'] = next(country['Name'] for country in countries if country['Code'] == results.get('country')) 
        else:
            obj_data['country'] = None
        exif_data[image_path] = obj_data
    return exif_data
 


