# Stamp Cropper

A lightweight batch image-processing tool designed to automate the cropping of stamp images while preserving customizable margins. This application was developed in Portuguese as a tailored solution for a client's daily workflow, helping eliminate repetitive manual image editing. The user interface and most of the in-app text are currently in Portuguese.

This software is actively being developed and will continue to improve based on the end user's evolving needs.

## Features

- **Drag-and-Drop Interface:** Easily add images and reorder the processing queue.
- **Batch Processing:** Process multiple images in one operation.
- **Custom Margins:** Adjust the top, bottom, left, and right padding to keep exactly the amount of background required.
- **Auto-Naming:** Automatically add prefixes, counters, and suffixes to output files.

## How to Run

### Option 1: Standalone Executable (Windows Only)

The easiest way to use the application is to download the pre-compiled executable:

1. Go to the [Releases](../../releases) page.
2. Download the latest `StampCropper.exe`.
3. Double-click the file to run the application.

### Option 2: Run from Source (All Operating Systems)

If you prefer to run the source code, or if you use macOS or Linux:

1. Make sure Python 3.8 or newer is installed.
2. Clone this repository.
3. From the project directory, install the dependencies listed in `requirements.txt`:

	```bash
	pip install -r requirements.txt
	```

4. Run the application:

	```bash
	python src/main.py
	```

## User Guide

<!-- Add a screenshot here:
![Interface Screenshot](imgs/screenshot1.png)
-->

1. **Add Images:** Click `+ Adicionar (ou arrastar)` or drag and drop stamp images into the application.
2. **Reorder Images:** Drag the `☰` icon next to an image to change its processing order.
3. **Set the Output Folder:** Click `Mudar` to select the folder where the cropped images will be saved.
4. **Configure Naming:** Set the desired prefix, starting counter (for example, `1`), and suffix.
5. **Adjust Margins (Optional):** Change the top, bottom, left, and right pixel values to leave more or less background around the stamp.
6. **Process Images:** Click the green `Recortar Selos` button.
7. **View Results:** The cropped stamps will be saved as individual high-quality images using your configured naming scheme, and the destination folder will open automatically.

## License

This project is licensed under the [Creative Commons Attribution-NonCommercial 4.0 International License](https://creativecommons.org/licenses/by-nc/4.0/).
