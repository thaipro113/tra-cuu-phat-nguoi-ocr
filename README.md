# Tra Cứu Phạt Nguội Bằng OCR Tự Động
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
pip install selenium pillow pytesseract schedule
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
# 🚀 Tính năng

- Tự động mở trình duyệt, điền biển số và loại xe.
- Tự động chụp ảnh captcha từ website.
- Xử lý ảnh captcha bằng thư viện `Pillow`.
- Giải mã captcha bằng `pytesseract` (OCR).
- Gửi form và kiểm tra kết quả vi phạm.
- Lên lịch chạy tự động 2 lần mỗi ngày (6h và 12h).
- Dễ dàng tùy chỉnh lịch chạy, biển số, hoặc tích hợp thêm gửi email, lưu log.
# Cấu trúc code
open_browser(): Mở Chrome và truy cập trang tra cứu.

fill_license_plate(): Nhập biển số xe và chọn loại xe.

capture_captcha(): Chụp ảnh captcha từ trang web.

preprocess_image(): Phóng to và xử lý ảnh captcha (lọc nhiễu, nhị phân...).

extract_text_from_image(): Giải mã ảnh captcha thành văn bản bằng OCR.

submit_form(): Gửi form với mã captcha đã giải mã.

check_result(): Kiểm tra kết quả trả về từ website.

check_captcha(): Hàm chính gọi các bước trên.
# Cách sử dụng
python BTL.py
