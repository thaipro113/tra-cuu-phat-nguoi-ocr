from selenium import webdriver
from selenium.webdriver.common.by import By
from PIL import Image, ImageFilter, ImageOps
import pytesseract
import time
import os
import schedule
# Chỉ định đường dẫn tesseract.exe
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
def check_captcha():
    driver = webdriver.Chrome()
    driver.get("https://www.csgt.vn/tra-cuu-phuong-tien-vi-pham.html")
    time.sleep(2)

    # Nhập biển số và chọn tỉnh
    driver.find_element(By.NAME, "BienKiemSoat").send_keys("74-G113951")
    driver.find_element(By.CSS_SELECTOR, '#formBSX > div.bot > div:nth-child(2) > select > option:nth-child(2)').click()
    time.sleep(0.5)

    # 1) Chụp ảnh captcha
    captcha_element = driver.find_element(By.ID, "imgCaptcha")
    captcha_element.screenshot("captcha.png")

    # 2) Phóng to ảnh lên gấp 3 lần
    img = Image.open("captcha.png")
    img = img.resize((img.width * 5, img.height * 5), Image.LANCZOS)
    img.save("captcha_resized.png")   # Lưu ảnh phóng to để kiểm tra

    # 3) Tiền xử lý ảnh phóng to
    img = img.convert('L')                                   # grayscale
    img = ImageOps.invert(img)                               # đảo màu nếu cần
    img = img.point(lambda x: 0 if x < 140 else 255)         # nhị phân
    img = img.filter(ImageFilter.MedianFilter())             # lọc nhiễu nhẹ
    img.save("captcha_processed.png")                        # Lưu ảnh xử lý để kiểm tra

    # 4) OCR captcha
    captcha_text = pytesseract.image_to_string(
        img,
        config='--oem 3 --psm 7 -c tessedit_char_whitelist=0123456789abcdefghijklmnopqrstuvwxyz'
    ).strip()
    print("Captcha OCR:", captcha_text)

    # 5) Nhập captcha và submit
    driver.find_element(By.NAME, "txt_captcha").send_keys(captcha_text)
    driver.find_element(By.CLASS_NAME, "btnTraCuu").click()
    result_text = driver.find_element(By.ID, "bodyPrint123").text
    if "Không tìm thấy kết quả" in result_text:
        print("-> Không tìm thấy kết quả!")
    time.sleep(5)
    driver.quit()


schedule.every().day.at("15:53").do(check_captcha)


while True:
    schedule.run_pending()
    time.sleep(1)  # Kiểm tra mỗi giây
