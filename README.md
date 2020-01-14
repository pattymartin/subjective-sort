# Subjective Sort

This project sorts images based on user input. Images will be displayed two at
a time so that the user can select which one they prefer. This repeats until
the list of images is fully sorted.

## Getting Started

The project can be run from the command line using the options described in the
Usage section below. The sorting function can also be imported into another
Python script (e.g. `from image_sort import image_sort`).

Images are displayed in a [Kivy](https://kivy.org/#home) window, so Kivy is
required to run the script. Alternatively, the executable `ssort.exe` can be
used instead, requiring neither Python nor Kivy. This is a standalone
executable requiring no installation.

This project is created with:
* Python 3.7.4
* Kivy 1.11.1 ([Installation instructions](
  https://kivy.org/doc/stable/gettingstarted/installation.html))

## Controls

An image can be selected either by clicking on it, or by pressing `1` or `2` on
the keyboard to select the left or right image respectively. A comparison can
be undone by pressing `Ctrl`+`Z`. If the window is closed before sorting is
finished, the sorting will resume the next time the script runs.

## Usage

```
python subjective_sort [OPTIONS] FILE [FILE...]
```
```
ssort.exe [OPTIONS] FILE [FILE...]
```

If no files are specified, files in the current working directory will be
sorted by default.

Positional arguments:
```
  files                              Files or directories to be sorted
```

Optional arguments:
```
  -h, --help                         Show the help message and exit
  -b, --batch-file BATCH_FILE        Text file containing filenames to sort,
                                     one filename per line
  -i, --include-subdirs              Include files from subdirectories
  -l, --enable-logging               Enable Kivy logging, which is disabled by
                                     default
```
