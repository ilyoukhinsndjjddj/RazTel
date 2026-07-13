import time
import sys
from playwright.sync_api import sync_playwright

TARGET_URL = "https://smm8.com/free-telegram-members"
TELEGRAM_LINK = "https://t.me/razoravan"

def run():
    with sync_playwright() as p:
        print("Starting Chromium Browser with anti-detect settings...")
        
        # استفاده از یک مرورگر با مشخصات واقعی تر برای جلوگیری از بلاک شدن تایمر
        browser = p.chromium.launch(
            headless=True,
            args=[
                "--disable-blink-features=AutomationControlled",
                "--no-sandbox",
                "--disable-setuid-sandbox"
            ]
        )
        
        # ساخت یک Context با مشخصات یک مرورگر واقعی (User-Agent عادی)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            viewport={"width": 1280, "height": 720}
        )
        
        page = context.new_page()
        
        # غیرفعال کردن کامل پرچم webdriver برای سایت
        page.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

        try:
            # ۱. ورود به سایت
            print(f"Navigating to {TARGET_URL}...")
            page.goto(TARGET_URL, timeout=60000)
            page.wait_for_load_state("networkidle")

            # ۲. وارد کردن لینک تلگرام
            print(f"Entering Telegram Link: {TELEGRAM_LINK}")
            input_selector = 'input[type="url"], input[placeholder*="Link"], input[name*="link"]'
            page.wait_for_selector(input_selector, timeout=15000)
            page.fill(input_selector, TELEGRAM_LINK)

            # ۳. کلیک روی دکمه ثبت اولیه برای شروع تایمر
            print("Clicking initial submit button...")
            submit_btn_selector = 'input#btnOptinLoggedIn, button[type="submit"], input[type="submit"]'
            page.click(submit_btn_selector)

            # ۴. پایش فعال تایمر به جای انتظار کورکورانه
            print("Waiting and monitoring the countdown...")
            
            # ما حداکثر ۳۶۰ ثانیه (۶ دقیقه) منتظر می‌مانیم و هر ۵ ثانیه وضعیت را چک می‌کنیم
            start_time = time.time()
            countdown_finished = False
            
            while time.time() - start_time < 360:
                # بررسی می‌کنیم که آیا دکمه نهایی قابل مشاهده یا فعال شده است؟
                is_visible = page.is_visible(submit_btn_selector)
                
                # همچنین چک می‌کنیم آیا دکمه کلاس disabled دارد یا خیر
                is_disabled = page.eval_on_selector(
                    submit_btn_selector, 
                    "el => el.disabled || el.classList.contains('disabled')"
                ) if page.locator(submit_btn_selector).count() > 0 else True
                
                if is_visible and not is_disabled:
                    print(f"Detected active button after {int(time.time() - start_time)} seconds!")
                    countdown_finished = True
                    break
                
                # برای اینکه مرورگر زنده بماند و تایمر جلو برود، صفحه را کمی اسکرول می‌کنیم
                page.evaluate("window.scrollBy(0, 10)")
                time.sleep(5)
                page.evaluate("window.scrollBy(0, -10)")
                time.sleep(5)
                
                print(f"Elapsed time: {int(time.time() - start_time)}s. Button visible: {is_visible}, disabled: {is_disabled}")

            # ۵. کلیک نهایی (اگر تایمر تمام شده باشد یا حتی اگر دکمه هنوز مخفی باشد، با زور جاوااسکریپت کلیک می‌کنیم)
            print("Attempting to click the final confirmation button...")
            try:
                # ابتدا تلاش برای کلیک عادی
                page.click(submit_btn_selector, timeout=5000)
                print("Clicked normally!")
            except Exception:
                # اگر کلیک عادی خطا داد، دکمه را با جاوااسکریپت مستقیم تحریک (Click) می‌کنیم
                print("Normal click failed. Executing click via JavaScript...")
                page.eval_on_selector(submit_btn_selector, "el => el.click()")
                print("Clicked via JavaScript!")

            # چند ثانیه صبر برای لود شدن موفقیت‌آمیز
            print("Waiting 15 seconds for confirmation response...")
            time.sleep(15)
            print("Process completed successfully!")

        except Exception as e:
            print(f"An error occurred during execution: {e}")
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
