# Installation Guide

## Windows 10 / 11

1. Install Python 3.10 or newer.
2. Open the extracted folder and double-click `start_windows.bat`.
3. On the first launch, pip installs `Pillow` and `reportlab`.
4. Choose a year, import 12 or 13 images, generate the PDF.
5. Find results in the `output` folder.

## Manual install

```cmd
py -3 -m pip install -r requirements.txt
py -3 calendar_lite.py
```

## Demo without GUI

```cmd
py -3 calendar_lite.py --demo --year 2027
```

This creates a demo PDF, PNG preview and HTML simulation in `output`.

## Troubleshooting

- **`py` is not recognized:** install Python with the Windows launcher, or replace `py -3` with `python` in the BAT file.
- **`No module named PIL` or `reportlab`:** run `py -3 -m pip install -r requirements.txt`.
- **Tkinter unavailable:** on Linux install your distribution's `python3-tk` package.
- **Photos out of order:** sort/rename images `01_...` through `13_...` before selecting them. The file dialog order is used.
- **PDF cannot be saved:** close the previously opened PDF and ensure the folder is writable.
- **No photos:** the program can generate a placeholder calendar; import photos for a finished result.

## No PHP / WAMP required

This GitHub Lite release runs independently of the commercial PHP edition.
