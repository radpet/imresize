def main():
    args = get_args()

    import os
    prefix = 'resized_'
    if args.nprefix:
        prefix = args.nprefix

    if os.path.isdir(args.impath):
        image_paths = [os.path.join(args.impath, image_name) for image_name in os.listdir(args.impath)]
    else:
        image_paths = [args.impath]

    if args.out:
        output_folder = args.out
    else:
        output_folder = get_path_without_image_name(image_paths[0])

    if not os.path.exists(output_folder):
        os.mkdir(output_folder)

    for image_path in image_paths:
        resize_save_image(image_path,
                          args.ratio,
                          get_new_image_path(output_folder,
                                             get_image_name_from_path(image_path),
                                             prefix))


def get_args():
    import argparse
    parser = argparse.ArgumentParser()

    parser.add_argument('ratio', help='Ratio to multiply width and height', type=float)
    parser.add_argument('impath', help='Folder or path to image', type=str)

    parser.add_argument('--nprefix', help='Prefix to append to the image name of the resized image', type=str)
    parser.add_argument('--out', help='Folder to output files in', type=str)

    return parser.parse_args()


def resize_save_image(image_path: str, ratio: float, new_image_path: str):
    from PIL import Image
    image = Image.open(image_path)

    print('Resizing {} with ratio={}.'.format(image_path, ratio))
    new_image_size = (int(image.size[0] * ratio), int(image.size[1] * ratio))
    image = image.resize(new_image_size, Image.ANTIALIAS)
    image.save(new_image_path)
    print('Saved {} with size={}'.format(new_image_path, new_image_size))


def get_image_name_from_path(image_path: str) -> str:
    return image_path.rsplit('/', 1)[1]


def get_path_without_image_name(image_path: str) -> str:
    return image_path.rsplit('/', 1)[0]


def get_new_image_path(image_path: str, image_name: str, prefix: str) -> str:
    from os import path
    return path.join(image_path, prefix + image_name)


if __name__ == '__main__':
    main()
