from selenium import webdriver
from selenium.webdriver.common.by import By
from PIL import Image, ImageFilter, ImageOps
import pytesseract
import time
import os
import schedule

# Đường dẫn tới Tesseract OCR
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Vào website đã chọn.
def open_browser():
    driver = webdriver.Chrome()
    driver.get("https://www.csgt.vn/tra-cuu-phuong-tien-vi-pham.html")
    time.sleep(2)
    return driver

# Nhập các thông tin Biển số xe, chọn loại phương tiện
def fill_license_plate(driver, plate="74-G113951"):
    driver.find_element(By.NAME, "BienKiemSoat").send_keys(plate)
    driver.find_element(By.CSS_SELECTOR, '#formBSX > div.bot > div:nth-child(2) > select > option:nth-child(2)').click()
    time.sleep(0.5)

# Chụp ảnh captcha từ trang web.
def capture_captcha(driver, path="captcha.png"):
    captcha_element = driver.find_element(By.ID, "imgCaptcha")
    captcha_element.screenshot(path)

# Phóng to và xử lý ảnh captcha để tăng độ chính xác OCR.
def preprocess_image(input_path, output_path):
    img = Image.open(input_path)
    img = img.resize((img.width * 5, img.height * 5), Image.LANCZOS)
    img = img.convert('L')  # Grayscale
    img = ImageOps.invert(img)
    img = img.point(lambda x: 0 if x < 140 else 255)
    img = img.filter(ImageFilter.MedianFilter())
    img.save(output_path)
    return img

# Xử lý ảnh captcha và nhận dạng văn bản bằng Tesseract OCR.
def extract_text_from_image(img):
    return pytesseract.image_to_string(
        img,
        config='--oem 3 --psm 7 -c tessedit_char_whitelist=0123456789abcdefghijklmnopqrstuvwxyz'
    ).strip()

# Nhập mã captcha và ấn nút tra cứu.
def submit_form(driver, captcha_text):
    driver.find_element(By.NAME, "txt_captcha").send_keys(captcha_text)
    driver.find_element(By.CLASS_NAME, "btnTraCuu").click()
    time.sleep(1)

# Kiểm tra kết quả trả về từ trang web.
def check_result(driver):
    result_text = driver.find_element(By.ID, "bodyPrint123").text
    result_text1 = driver.find_element(By.CLASS_NAME, "xe_texterror").text
    if "Mã xác nhận sai!" in result_text1:
        print("-> Mã xác nhận sai!")
    elif "Không tìm thấy kết quả" in result_text:
        print("-> Không tìm thấy kết quả!")
    else:
        print("-> Có kết quả!")

# Hàm chính để kiểm tra captcha và tra cứu vi phạm.
def check_captcha():
    driver = open_browser()
    try:
        fill_license_plate(driver)
        capture_captcha(driver)
        processed_img = preprocess_image("captcha.png", "captcha_processed.png")
        captcha_text = extract_text_from_image(processed_img)
        print("Captcha OCR:", captcha_text)
        submit_form(driver, captcha_text)
        check_result(driver)
    except Exception as e:
        print("Lỗi trong quá trình kiểm tra:", e)
    finally:
        time.sleep(5)
        driver.quit()


# Lên lịch chạy hàng ngày
schedule.every().day.at("06:00").do(check_captcha)
schedule.every().day.at("12:00").do(check_captcha)

# Vòng lặp kiểm tra lịch
while True:
    schedule.run_pending()
    time.sleep(1)
