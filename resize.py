def main():
    args = get_args()

    import os
    if args.nprefix:
        prefix = args.nprefix
    else:
        prefix = 'resized_{}_'.format(args.ratio)

    if os.path.isdir(args.impath):
        image_paths = [os.path.join(args.impath, image_name) for image_name in os.listdir(args.impath)]
    else:
        image_paths = [args.impath]

    image_paths = [os.path.normpath(path) for path in image_paths]

    resize_image_paths(image_paths, args.ratio, prefix, args.out)


def resize_image_paths(image_paths, ratio, prefix, root_output_folder):
    import os

    def dfs(current_image_path, visited, current_output_folder):
        if current_image_path in visited:
            return
        else:
            visited.add(current_image_path)

        if not os.path.exists(current_output_folder):
            os.mkdir(current_output_folder)

        if not os.path.isdir(current_image_path):
            resize_save_image(current_image_path,
                              ratio,
                              get_new_image_path(
                                  current_output_folder,
                                  get_image_name_from_path(current_image_path),
                                  prefix))
        else:
            new_output_folder = os.path.join(current_output_folder, get_last_path_node(current_image_path))
            for image_name in os.listdir(current_image_path):
                dfs(os.path.join(current_image_path, image_name), visited, new_output_folder)

    visited = set()

    if not os.path.exists(root_output_folder):
        os.mkdir(root_output_folder)

    root_input_folder = get_basename(image_paths[0])
    for image_path in image_paths:
        dfs(image_path, visited, os.path.join(root_output_folder, root_input_folder))


def get_last_path_node(path: str) -> str:
    import os
    return path.rsplit(os.sep, 1)[1]


def get_basename(path):
    import os
    return os.path.basename(os.path.dirname(path))


def get_args():
    import argparse
    parser = argparse.ArgumentParser()

    parser.add_argument('ratio', help='Ratio to multiply width and height', type=float)
    parser.add_argument('impath', help='Folder or path to image', type=str)
    parser.add_argument('out', help='Folder to output files in', type=str)

    parser.add_argument('--nprefix', help='Prefix appended to the filename of the resized image', type=str)

    return parser.parse_args()


def resize_save_image(image_path: str, ratio: float, new_image_path: str):
    from PIL import Image
    try:
        image = Image.open(image_path)
        print('Resizing {} with ratio={}.'.format(image_path, ratio))
        new_image_size = (int(image.size[0] * ratio), int(image.size[1] * ratio))
        image = image.resize(new_image_size, Image.ANTIALIAS)
        image.save(new_image_path)
        print('Saved {} with size={}'.format(new_image_path, new_image_size))
    except IOError:
        print('Error resizing {}'.format(image_path))


def get_image_name_from_path(image_path: str) -> str:
    return get_last_path_node(image_path)


def get_path_without_image_name(image_path: str) -> str:
    import os
    return image_path.rsplit(os.sep, 1)[0]


def get_new_image_path(image_path: str, image_name: str, prefix: str) -> str:
    from os import path
    return path.join(image_path, prefix + image_name)


if __name__ == '__main__':
    main()
