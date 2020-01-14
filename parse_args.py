import argparse
import os
import sys


def args_files():
    """
    Parse command line arguments, returning a list of files.

    :return: A list of filenames
    :rtype: list
    """

    files_or_dirs = args.files

    if args.batch_file:
        files_or_dirs.extend(_from_file(args.batch_file))
    elif not args.files:
        files_or_dirs.append(os.getcwd())

    files = []
    for f in files_or_dirs:
        if os.path.isdir(f):
            files.extend(_from_directory(f, args.include_subdirs))
        else:
            files.append(f)

    return files


def _from_file(filename):
    """
    Get filenames from a batch file that contains a list of filenames.

    :param filename: Path to the text file
    :type filename: str
    :return: A list of filenames
    :rtype: list
    """

    with open(filename) as f:
        return [line.strip() for line in f]


def _from_directory(path, subdir):
    """
    Get filenames from a directory. If `subdir` is True, include files
    from subdirectories.

    :param path: Path to the directory
    :type path: str
    :param subdir: True to include subdirectories, otherwise False
    :type subdir: bool
    :return: A list of filenames
    :rtype: list
    """
    walk = os.walk(path)
    if subdir:
        return [os.path.join(r, f) for r, d, fs in walk for f in fs]
    else:
        return [os.path.join(path, f) for f in next(walk)[2]]


def _parse_args():
    """
    Parse command line arguments.

    :return: The parsed arguments
    :rtype: argparse.Namespace
    """

    parser = argparse.ArgumentParser()

    parser.add_argument(
        'files', nargs='*',
        help='files or directories to be sorted')
    parser.add_argument(
        '-b', '--batch-file',
        help='text file containing filenames to sort, one filename per line')
    parser.add_argument(
        '-i', '--include-subdirs',
        action='store_true',
        help='whether to include files in subdirectories')
    parser.add_argument(
        '-l', '--enable-logging',
        action='store_true',
        help='whether to enable Kivy logging')

    # remove consumed args from sys.argv
    known_args, unknown_args = parser.parse_known_args()
    sys.argv = sys.argv[:1] + unknown_args

    if not known_args.enable_logging:
        os.environ['KIVY_NO_CONSOLELOG'] = '1'

    return known_args


args = _parse_args()
