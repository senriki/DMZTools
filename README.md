# Utility Scripts

Three helper scripts live in this folder:

- `merge_pdf.py` merges two source PDFs into a new file using `PyPDF2`.
- `make_qr.py` generates a QR code PNG for a single URL using the `qrcode` library (Pillow backend).
- `convert_to_ico.py` converts PNG/JPG artwork into Windows `.ico` files so you can brand DMZTools.
- `app_gui.py` provides the DMZTools tkinter interface that wraps both features and is ready to package into an `.exe`.

## About DMZTools

DMZTools is a lightweight desktop helper for day-to-day document prep: merge two recipe PDFs into a timestamped bundle and generate shareable QR codes for download links. Everything runs locally on Windows, so no files or URLs leave your machine, and you can ship a single `.exe` to teammates who do not have Python installed.

## Requirements

- Python 3.10+ on Windows.
- Virtual environment (recommended) with the packages listed in `requirements.txt`:

```powershell
pip install -r requirements.txt
```

This installs `PyPDF2`, `qrcode[pil]`, `pyinstaller`, and `pillow` (Pillow powers QR generation, icon work, and the GUI branding).

## Setup (first run)

1. Open PowerShell and go to the project folder:
   ```powershell
   cd C:\projects\dmztools
   ```
2. Create a virtual environment (one time):
   ```powershell
   python -m venv .venv
   ```
3. Activate it (PowerShell):
   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```
   If activation is blocked, run `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` first.
4. Install dependencies:
   ```powershell
   pip install -r requirements.txt
   ```

## Using `merge_pdf.py`

1. Edit the file paths in `merge_pdf.py` so `pdf_a`, `pdf_b`, and `merged_pdf` point to the files you want. (Or import `merge_pdfs` and pass a list/tuple of any length.)
2. With the virtual environment active, run:
   ```powershell
   python merge_pdf.py
   ```
3. The merged PDF is written to the output path you configured (overwrites existing files).

## Using `make_qr.py`

1. Update `make_qr.py` so `url` is the link to encode and `output_path` is where to save the PNG.
2. Run:
   ```powershell
   python make_qr.py
   ```
3. Open the generated PNG to verify it scans correctly (phone camera or QR reader app).

## Using `convert_to_ico.py`

Turn any logo into an icon for the DMZTools window and PyInstaller build:

```powershell
python convert_to_ico.py .\logo.png --output .\logo.ico --sizes 256,128,64,32,16
```

- `--output` is optional; if omitted the script replaces the extension with `.ico`.
- `--sizes` controls which resolutions are embedded inside the `.ico`. Provide a comma-separated list; defaults to `256,128,64,32,16`.

## Using DMZTools (`app_gui.py`)

1. Launch the interface:
   ```powershell
   python app_gui.py
   ```
2. **Merge PDFs** tab:
   - Click **Add PDFs** to select as many PDFs as you need (order matters; add them in sequence or remove/re-add to adjust).
   - Use **Remove Selected** or **Clear List** to fix mistakes.
   - Optionally type the merged filename (without extension). The app appends a timestamp (e.g., `myname-20250211-153000.pdf`); blank defaults to `merged-<timestamp>.pdf` inside the first PDF's folder. The folder is created automatically if it does not exist.
   - Click **Merge PDFs**; a message box confirms success or shows any errors.
3. **Create QR** tab:
   - Enter the URL to encode.
   - Optionally type a file name (no extension needed). The app saves it as `<name>-<timestamp>.png` in the project folder; blank defaults to `qr-<timestamp>.png`. If the folder is missing it is created automatically.
   - Click **Generate QR** to create the image.
4. The GUI handles validation and shows message boxes if something is missing.

## Building a standalone `.exe`

PyInstaller is already included in `requirements.txt`. After activating the venv:

```powershell
pyinstaller --onefile --windowed --name DMZTools --icon logo.ico --add-data "logo.ico;." app_gui.py
```

- `--icon logo.ico` sets the Windows icon, and `--add-data "logo.ico;."` bundles the image so the app can still display it at runtime.
- The executable and supporting files appear in `dist\DMZTools.exe`.
- Copy the `.exe` anywhere along with any assets it needs (Pillow embeds its dependencies automatically).
- For a custom icon, add `--icon path\to\icon.ico`.

## Re-running later

1. `cd C:\projects\dmztools`
2. Activate the venv: `.\.venv\Scripts\Activate.ps1`
3. Run `python merge_pdf.py`, `python make_qr.py`, or `python app_gui.py` as needed (or rebuild the exe with PyInstaller).
