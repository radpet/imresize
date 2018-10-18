# What is this?

This is simple script used for up/down scaling images.
It supports processing both single images and folders.
When a folder is passed the script recursively traverse it, resize images and
create directories thus preserving the directory structure.

# How to use it?

run `python3 resize.py -h`

# Examples
* To resize an image run `python3 resize.py 0.25 path_to_image output_folder`
* To resize folder `python3 resize.py 0.25 path_to_folder output_folder`
