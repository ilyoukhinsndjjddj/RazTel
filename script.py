import time
import sys
from playwright.sync_api import sync_playwright

# تنظیمات دقیق بر اساس اطلاعات ارسالی شما
TARGET_URL = "https://smm8.com/free-telegram-members"
TELEGRAM_LINK = "https://t.me/razoravan"

def run():
    with sync_playwright() as p:
        print("Starting Chromium Browser...")
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        try:
            # ۱. ورود به سایت
            print(f"Navigating to {TARGET_URL}...")
            page.goto(TARGET_URL, timeout=60000)
            page.wait_for_load_state("networkidle")

            # ۲. وارد کردن لینک تلگرام در فیلد مربوطه
            print(f"Entering Telegram Link: {TELEGRAM_LINK}")
            input_selector = 'input[type="url"], input[placeholder*="Link"], input[name*="link"]'
            page.wait_for_selector(input_selector, timeout=15000)
            page.fill(input_selector, TELEGRAM_LINK)

            # ۳. کلیک روی دکمه ثبت اولیه برای شروع تایمر
            print("Clicking initial submit button...")
            initial_btn = 'input#btnOptinLoggedIn, button[type="submit"], input[type="submit"]'
            page.click(initial_btn)

            # ۴. انتظار ۵ دقیقه‌ای (۳۰۰ ثانیه) برای اتمام تایمر
            print("Waiting 5 minutes (310 seconds) for the countdown timer to finish...")
            time.sleep(310)

            # ۵. پیدا کردن و کلیک روی دکمه نهایی فعال شده
            print("Looking for the active final confirmation button...")
            
            # در این بخش به دنبال دکمه‌ای می‌گردیم که بعد از اتمام تایمر فعال و قابل دیدن (visible) شده است
            # معمولاً متن آن به چیزی مثل "Get" یا "Order" یا "Confirm" تغییر می‌کند یا کلاس disabled آن برداشته می‌شود.
            final_btn_selector = 'button:not([disabled]):has-text("Get"), button:not([disabled]):has-text("Order"), input#btnOptinLoggedIn, button[type="submit"]'
            
            # منتظر می‌شویم تا دکمه نهایی کاملاً قابل دیدن و کلیک کردن شود
            page.wait_for_selector(final_btn_selector, state="visible", timeout=30000)
            
            print("Clicking final confirmation button...")
            page.click(final_btn_selector)
            
            # چند ثانیه صبر می‌کنیم تا فرآیند ثبت نهایی در سایت انجام شود
            print("Waiting for success message...")
            time.sleep(15)
            print("Process completed successfully!")

        except Exception as e:
            print(f"An error occurred during execution: {e}")
            # یک عکس از صفحه در لحظه خطا می‌گیریم تا اگر باز هم خطا داد بتوانیم ببینیم مشکل از چیست
            try:
                page.screenshot(path="error_screenshot.png")
                print("Screenshot of error saved as 'error_screenshot.png'")
            except:
                pass
            browser.close()
            sys.exit(1)

        finally:
            browser.close()

if __name__ == "__main__":
    run()
