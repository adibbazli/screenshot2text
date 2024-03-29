from PIL import ImageGrab, Image
import win32clipboard
import hashlib
import time
from io import BytesIO
import pytesseract

# Set the path to the Tesseract OCR executable
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Adjust the path as needed

def is_clipboard_image():
    try:
        # Open the clipboard for reading
        win32clipboard.OpenClipboard()

        # Check if the clipboard has CF_DIB (Device Independent Bitmap) format
        is_image = win32clipboard.IsClipboardFormatAvailable(win32clipboard.CF_DIB)

        if is_image:
            # Get clipboard data as bytes
            data = win32clipboard.GetClipboardData(win32clipboard.CF_DIB)

            # Hash the clipboard content using SHA-256
            sha256_hash = hashlib.sha256(data).hexdigest()

            # Get image using PIL
            image = Image.open(BytesIO(data))

            return is_image, sha256_hash, image

        return is_image, None, None

    finally:
        # Close the clipboard
        win32clipboard.CloseClipboard()

def ocr_image(image):
    # Convert the image to RGB format
    image = image.convert("RGB")

    # Use pytesseract to perform OCR on the image
    text = pytesseract.image_to_string(image)

    return text

def set_clipboard_text(text):
    # Open the clipboard for writing
    win32clipboard.OpenClipboard()

    # Clear the clipboard content
    win32clipboard.EmptyClipboard()

    # Set the clipboard data as text
    win32clipboard.SetClipboardText(text)

    # Close the clipboard
    win32clipboard.CloseClipboard()

if __name__ == "__main__":
    previous_hash = None

    while True:
        is_image, sha256_hash, image = is_clipboard_image()

        if is_image:
            print("Clipboard contains an image.")
            print("SHA-256 hash:", sha256_hash)

            if sha256_hash == previous_hash:
                print("Hash is the same as the previous iteration.")
            else:
                print("Hash is different from the previous iteration.")
                previous_hash = sha256_hash

                # Perform OCR on the image
                text_result = ocr_image(image)
                print("OCR Result:")
                print(text_result)

                # Set the clipboard to the OCR result
                set_clipboard_text(text_result)
                print("Clipboard set to OCR result.")

            print("Sleeping for 0.1 seconds.")
            time.sleep(0.1)
        else:
            print("Clipboard does not contain an image.")

        # Adjust the sleep duration based on your requirements
        time.sleep(1)  # Adjust the sleep duration as needed
