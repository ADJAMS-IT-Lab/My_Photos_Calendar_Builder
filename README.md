# MODEL 01 LITE — Photo Wall Calendar (Python)

A lightweight, **English-only**, Gregorian A4 photo wall-calendar generator for Windows and other Python desktop environments. **No Arabic text or Hijri dates.**

## Features

- Import **12 or 13 photos at once**: 12 = one photo per month (January photo also used on cover); 13 = cover photo + one for each month.
- Generate a **14-page A4 PDF** (cover, 12 months, annual overview).
- Save PDFs in `output/` with a timestamped filename.
- Generate a **PNG preview** and a **browser-based HTML slideshow simulation**.
- Annual overview is laid out as a 3 × 4 grid so all twelve months fit.
- Gregorian dates, Monday-first, English-only UI.
- Demo included: 13 sample images, sample PDF, PNG and HTML simulation.

## Quick start (Windows)

1. Install Python 3.10+ from https://www.python.org/downloads/ (enable **Add Python to PATH**).
2. Extract this repository to a writable folder.
3. Double-click `start_windows.bat`.
4. Select the year and click **Import 12 / 13 photos**.
5. Select all 12 or 13 photos in one file dialog, then click **Generate PDF**.
6. Click **Open Output** to access your generated files.

## Cross-platform / command line

```bash
python -m pip install -r requirements.txt
python calendar_lite.py
python calendar_lite.py --demo --year 2027
```

## Files

- `calendar_lite.py` — complete Python Tkinter application and rendering engine
- `start_windows.bat` — Windows installer/launcher
- `demo/sample_images/` — 13 demonstration images
- `demo/Wall_Calendar_Model01_2027_EN_14pages_DEMO.pdf` — sample PDF
- `demo/Wall_Calendar_Model01_2027_Preview.png` — sample image
- `demo/Wall_Calendar_Model01_2027_Simulation.html` — sample browser slideshow
- `output/` — generated documents (ignored by Git)
- `ABOUT.md` — project description
- `INSTALLATION.md` — installation and troubleshooting

## Scope

This is a standalone **Lite** release, not a patch to the commercial multilingual PHP/Python edition. It does not include Arabic shaping, Hijri conversion, photo collages or per-month multiple-image editing.

## License

MIT. See [LICENSE](LICENSE).
