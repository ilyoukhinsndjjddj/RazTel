import time
import sys
from playwright.sync_api import sync_playwright

# تنظیمات دقیق بر اساس اطلاعات ارسالی شما
TARGET_URL = "https://smm8.com/free-telegram-members"
TELEGRAM_LINK = "https://t.me/razoravan"

def run():
    with sync_playwright() as p:
        print("Starting Chromium Browser...")
        # اجرای مرورگر
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        try:
            # ۱. ورود به سایت
            print(f"Navigating to {TARGET_URL}...")
            page.goto(TARGET_URL, timeout=60000)
            page.wait_for_load_state("networkidle")

            # ۲. وارد کردن لینک تلگرام در فیلد مربوطه
            # فیلد ورودی در این سایت معمولاً یک input از نوع url یا با آیدی خاص است.
            print(f"Entering Telegram Link: {TELEGRAM_LINK}")
            input_selector = 'input[type="url"], input[placeholder*="Link"], input[name*="link"]'
            page.wait_for_selector(input_selector, timeout=15000)
            page.fill(input_selector, TELEGRAM_LINK)

            # ۳. کلیک روی دکمه ثبت اولیه برای شروع تایمر
            # دکمه ثبت اولیه معمولاً متن "Get" یا "Submit" یا کلاس خاصی دارد.
            print("Clicking initial submit button...")
            submit_btn_selector = 'button[type="submit"], input[type="submit"]'
            page.click(submit_btn_selector)

            # ۴. انتظار ۵ دقیقه‌ای (۳۰۰ ثانیه) برای اتمام تایمر
            print("Waiting 5 minutes (300 seconds) for the countdown timer to finish...")
            # اضافه کردن ۱۰ ثانیه بیشتر برای اطمینان از پایان کامل انیمیشن تایمر سایت
            time.sleep(310)

            # ۵. کلیک روی دکمه نهایی پس از اتمام تایمر
            print("Clicking final confirmation button...")
            # در این سایت‌ها دکمه نهایی معمولاً بعد از اتمام تایمر فعال یا ظاهر می‌شود.
            # برای اطمینان مجدداً روی همان دکمه یا دکمه جدید کلیک می‌کنیم.
            page.click(submit_btn_selector)
            
            # چند ثانیه صبر می‌کنیم تا پیام موفقیت‌آمیز بودن ثبت سفارش لود شود
            time.sleep(10)
            print("Process completed successfully!")

        except Exception as e:
            print(f"An error occurred during execution: {e}")
            browser.close()
            sys.exit(1)

        finally:
            browser.close()

if __name__ == "__main__":
    run()
