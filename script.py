import time
import sys
from playwright.sync_api import sync_playwright

TARGET_URL = "https://smm8.com/free-telegram-members"
TELEGRAM_LINK = "https://t.me/razoravan" #

def run():
    with sync_playwright() as p:
        print("Starting Chromium Browser...")
        
        browser = p.chromium.launch(
            headless=True,
            args=[
                "--disable-blink-features=AutomationControlled",
                "--no-sandbox",
                "--disable-setuid-sandbox"
            ]
        )
        
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            viewport={"width": 1280, "height": 720}
        )
        
        page = context.new_page()
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

            # ۳. کلیک روی دکمه اولیه برای شروع تایمر
            print("Clicking initial submit button to start the timer...")
            submit_btn_selector = 'input#btnOptinLoggedIn, button[type="submit"], input[type="submit"]'
            page.click(submit_btn_selector)

            # ۴. انتظار کامل و زنده نگه داشتن صفحه تا پایان تایمر (۵ دقیقه و ۲۰ ثانیه)
            print("Successfully clicked! Now holding the page active for 320 seconds...")
            
            start_time = time.time()
            total_wait = 320  # ۵ دقیقه و ۲۰ ثانیه (کمی بیشتر از ۵ دقیقه برای اطمینان)
            
            while time.time() - start_time < total_wait:
                elapsed = int(time.time() - start_time)
                remaining = total_wait - elapsed
                
                # اسکرول تفننی صفحه برای جلوگیری از فریز شدن مرورگر یا غیرفعال شدن سشن
                if elapsed % 30 == 0:
                    page.evaluate("window.scrollBy(0, 30)")
                    time.sleep(1)
                    page.evaluate("window.scrollBy(0, -30)")
                
                print(f"Elapsed: {elapsed}s | Remaining: {remaining}s. Keeping connection alive...")
                time.sleep(10)

            # ۵. ثبت وضعیت نهایی پس از پایان تایمر
            print("Timer period finished! Waiting 15 more seconds for the auto-success message to render...")
            time.sleep(15)
            
            # ذخیره عکس نهایی از صفحه برای دیدن پیام موفقیت (Success)
            page.screenshot(path="final_result.png")
            print("Saved final result screenshot as 'final_result.png'")
            print("Process fully completed!")

        except Exception as e:
            print(f"An error occurred: {e}")
            try:
                page.screenshot(path="error_screenshot.png")
                print("Saved error screenshot.")
            except:
                pass
            browser.close()
            sys.exit(1)

        finally:
            browser.close()

if __name__ == "__main__":
    run()
