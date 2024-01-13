# Screenshot2text
Performs OCR on image screenshot (Windows + Shift + S) and copy it to clipboard using Python

## Technology
The application make use of `PIL` and `pytesseract`. Please install whatever necessary.

## Method
The application actively scan clipboard at certain interval, if it is an image, it will performs OCR image to string, and replace the image with actual text.
It will run indefinitely until you stop the application. It will only performs OCR image to string once. 

## Limitation
It is depends on how `pytesseract` performs, if it is not up to your expectation, you might want to start from there.
