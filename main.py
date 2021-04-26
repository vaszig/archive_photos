import sys
from pathlib import Path

from exif import Image

from manipulate_images import list_image_paths, is_image, fetch_exif_data, filter_exif_data, errors
from manipulate_directory import save_by_date, save_by_location


if __name__ == '__main__':

    source = Path(input('Give source path of photos: ')).resolve()
    target = Path(input('Give target path for photos: ')).resolve()
    if not source.exists() or not target.exists():
        sys.exit(errors)
    
    images_paths = list_image_paths(source)
    if not images_paths:
        errors['no_files'] = True
        sys.exit(errors)

    for image_path in images_paths:
        if is_image(image_path):
            with open(image_path, 'rb') as image_file:
                img_obj = Image(image_file)
                if img_obj.has_exif:
                    exif_data = fetch_exif_data(img_obj)
                    filtered_exif_data = filter_exif_data(exif_data)
                    if filtered_exif_data.get('gps_latitude') and filtered_exif_data.get('gps_longitude'):
                        save_by_location(image_path, filtered_exif_data, target)
                    else:
                        save_by_date(image_path, filtered_exif_data, target)
                else:
                    errors['no_exif_data'].append(image_path)
        else:
            errors['wrong_file_format'].append(image_path.stem)
    
    print(errors)
