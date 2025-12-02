📝 Handwritten Text Recognition using EasyOCR (Python 3.10)

This project performs handwritten text recognition using EasyOCR in Python 3.10.
It supports multiple languages and works on images, scanned documents, and handwritten notes.

🚀 Features

📷 Image-to-text extraction

✍️ Handwritten text recognition

🌍 Multi-language OCR (English, Hindi)

🧠 Uses EasyOCR + OpenCV + PyTorch

🗂 Supports single images & datasets

📦 Installation
1️⃣ Clone this repository
git clone https://github.com/nikhi0201/Minor-Project.git
cd Minor-Project

2️⃣ Create virtual environment (Python 3.10)
python3.10 -m venv venv


Activate it:

Windows

venv\Scripts\activate


Linux / Mac

source venv/bin/activate

3️⃣ Install dependencies
pip install -r requirements.txt


🧪 Usage Example
Run OCR on an image
import easyocr
import cv2

reader = easyocr.Reader(['en'])   # add ['en','hi'] for Hindi, ['en','te'] for Telugu
result = reader.readtext("image.jpg")

for box, text, confidence in result:
    print(text)

Sample output
Hello World

📂 Project Structure
📁 handwritten-ocr
 ┣ 📄 predict.py        # OCR script
 ┗ 📄 README.md

▶️ Running the Project
python main.py

🔮 Future Enhancements

Add Streamlit-based UI

Create dataset-based batch OCR

Train custom model for Hindi handwriting

Export OCR results to CSV/JSON

🤝 Contributing

Contributions are welcome!
Create a pull request or open an issue for discussion.
