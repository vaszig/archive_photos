import sys
from pathlib import Path

from manipulate_images import list_images_paths, fetch_exif_data, read_images, errors
from manipulate_directory import define_type_of_archive


if __name__ == '__main__':
    source = Path(input('Give source path of photos: ')).resolve()
    if not source.exists():
        sys.exit('Wrong path.')
    
    images_paths = list_images_paths(source)
    if not images_paths:
        sys.exit(errors)
    
    images_objs = read_images(images_paths)
    exif_data = fetch_exif_data(images_objs)
    while True:
        target = Path(input('Give target path for photos: ')).resolve()
        if not target.exists():
            continue
        else:
            define_type_of_archive(source, target, exif_data)
            break

    print(exif_data)
    print(errors)