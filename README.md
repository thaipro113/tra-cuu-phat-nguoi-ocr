# tra-cuu-phat-nguoi-ocr
Tự động tra cứu phương tiện vi phạm giao thông và OCR captcha
# Yêu cầu hệ thống
Python >= 3.8

Google Chrome đã cài sẵn

ChromeDriver (phiên bản tương thích với Chrome)

Tesseract OCR
# Cài đặt
git clone https://github.com/thaipro113/tra-cuu-phat-nguoi-ocr.git
cd tra-cuu-phat-nguoi-ocr
# Cài đặt thư viện Python
pip install -r requirements.txt
# Cài đặt Tesseract OCR
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
# Cách sử dụng
python BTL.py
