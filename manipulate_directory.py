import sys
from pathlib import Path
from datetime import datetime

from manipulate_images import get_gps_location, errors


def save_by_date(image_path, image_data, target):
    """Saves photo according to the date taken."""
    date = str(datetime.strptime(image_data['datetime_original'], '%Y:%m:%d %H:%M:%S').date())
    year = str(datetime.strptime(image_data['datetime_original'], '%Y:%m:%d %H:%M:%S').year)

    year_dir = target / year

    if not year_dir.exists():
        year_dir.mkdir(parents=True)
    target_path = year_dir / (date + '_' + image_path.stem)
    if target_path.exists():
        errors['same_files'].append(image_path.stem)
    else:
        image_path.rename(target_path)


def save_by_location(image_path, image_data, target):
    """Saves photo according to the location."""
    location = get_gps_location(image_data['gps_latitude'], image_data['gps_latitude_ref'], image_data['gps_longitude'], image_data['gps_longitude_ref'])
    date = str(datetime.strptime(image_data['datetime_original'], '%Y:%m:%d %H:%M:%S').date())
    year = str(datetime.strptime(image_data['datetime_original'], '%Y:%m:%d %H:%M:%S').year)

    location_dir = target / (location['country'] + '-' + location['city'])
    year_dir = location_dir / year    

    if not location_dir.exists() or not year_dir.exists():
        year_dir.mkdir(parents=True)

    target_path = year_dir / (date + '_' + image_path.stem)
    if target_path.exists():
        errors['same_files'].append(image_path.stem)
    else:
        image_path.rename(target_path)
