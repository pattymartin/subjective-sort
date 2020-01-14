import parse_args
from image_sort import image_sort

files = parse_args.args_files()
print(image_sort(files))
