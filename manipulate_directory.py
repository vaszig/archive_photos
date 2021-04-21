import sys
from pathlib import Path
from datetime import datetime

from manipulate_images import errors


def save_by_date(target, image_path, image_data, year, date):
    '''Saves photo according to the date taken.'''
    year_dir = target / year

    if not year_dir.exists():
        year_dir.mkdir(parents=True)
    target_path = year_dir / (date + '_' + image_path.stem)
    if target_path.exists():
        errors['same_files'].append(image_path.stem)
    else:
        image_path.rename(target_path)


def save_by_location(image_path, image_data, location_dir, year, date):
    '''Saves photo according to the location.'''

    year_dir = location_dir / year 

    if not location_dir.exists():
        year_dir.mkdir(parents=True)
    if not year_dir.exists():
        year_dir.mkdir(parents=True)

    target_path = year_dir / (date + '_' + image_path.stem)
    if target_path.exists():
        errors['same_files'].append(image_path.stem)
    else:
        image_path.rename(target_path)


def define_type_of_archive(source, target, exif_data):
    '''Defines wether the photo will be archived by date or by location (according to the existing metadata).'''

    for image_path, image_data in exif_data.items():
        date = str(datetime.strptime(image_data['date'], '%Y:%m:%d %H:%M:%S').date())
        year = str(datetime.strptime(image_data['date'], '%Y:%m:%d %H:%M:%S').year)
        if image_data.get('country') is not None and image_data.get('city') is not None:
            location_dir = target / (image_data['country'] + '-' + image_data['city'])
            save_by_location(image_path, image_data, location_dir, year, date)
        else:
            save_by_date(target, image_path, image_data, year, date)