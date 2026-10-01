"""
=============================================================================
*  Project: X Hot Hunter 🔥 (No-API Stealth Edition)
*  Features:
*    - 🕒 Schedule: اجرای دقیق هر ۳ ساعت
*    - 🕵️‍♂️ Stealth Mode: دور زدن تحریم‌ها با مرورگر نامرئی (Playwright)
*    - 🎯 Target: حداقل 1000 لایک، 1000 ویو، 100 کامنت (فقط فارسی)
*    - 🛑 Anti-Ban Guard: دو دقیقه تاخیر بین هر ری‌پست برای سلامت اکانت
=============================================================================
"""

import os
import time
import re
from playwright.sync_api import sync_playwright

TARGET_ACCOUNTS = ["Elnaz_x", "persian_twt", "khabarfarsi"] # آیدی‌ها رو اینجا بذار
AUTH_TOKEN = os.environ.get("X_AUTH_TOKEN")

def convert_persian_nums(text):
    """تبدیل اعداد فارسی به انگلیسی واسه اینکه ربات قاطی نکنه"""
    translation_table = str.maketrans('۰۱۲۳۴۵۶۷۸۹', '0123456789')
    return text.translate(translation_table)

def extract_number(text):
    """کشیدن بیرون عدد خالص از متن‌هایی مثل 1.5K Likes یا ۱ هزار پسند"""
    if not text: return 0
    text = convert_persian_nums(text)
    match = re.search(r'([\d\.,]+)([KkMmهزارمیلیون]*)', text, re.IGNORECASE)
    if not match: return 0
    
    num_str = match.group(1).replace(',', '')
    mult = match.group(2).lower()
    
    try: val = float(num_str)
    except: return 0
        
    if 'k' in mult or 'هزار' in mult: val *= 1000
    elif 'm' in mult or 'میلیون' in mult: val *= 1000000
    return int(val)

def main():
    if not AUTH_TOKEN:
        print("❌ داداش کوکی auth_token رو نذاشتی تو تنظیمات گیت‌هاب!")
        return

    print("🦅 عقاب نامرئی ایکس به پرواز درآمد...")

    with sync_playwright() as p:
        # باز کردن مرورگر مخفی
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            viewport={'width': 1280, 'height': 800},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        
        # تزریق شاه‌کلید واسه ورود بی‌صدا
        context.add_cookies([{
            "name": "auth_token", "value": AUTH_TOKEN, "domain": ".x.com", "path": "/"
        }])
        
        page = context.new_page()

        for account in TARGET_ACCOUNTS:
            print(f"\n🚜 در حال شخم زدن پیج: @{account}")
            try:
                page.goto(f"https://x.com/{account}", timeout=60000)
                page.wait_for_selector('article[data-testid="tweet"]', timeout=30000)
                time.sleep(5) # یه استراحت ریز تا توییت‌ها کامل لود بشن

                tweets = page.query_selector_all('article[data-testid="tweet"]')
                
                for t in tweets[:10]: # بررسی ۱۰ توییت آخر
                    tweet_text = t.inner_text()
                    
                    # شرط اول: داشتن حروف فارسی
                    if not re.search(r'[\u0600-\u06FF]', tweet_text):
                        continue

                    # درآوردن آمار از روی دکمه‌های زیر پست
                    reply_btn = t.query_selector('[data-testid="reply"]')
                    replies = extract_number(reply_btn.get_attribute('aria-label') if reply_btn else "")
                    
                    like_btn = t.query_selector('[data-testid="like"], [data-testid="unlike"]')
                    likes = extract_number(like_btn.get_attribute('aria-label') if like_btn else "")
                    
                    view_elem = t.query_selector('[aria-label*="View"], [aria-label*="view"], [aria-label*="بازدید"]')
                    views = extract_number(view_elem.get_attribute('aria-label') if view_elem else "")

                    # شروط سنگین شما
                    if likes >= 1000 and replies >= 100 and views >= 1000:
                        print(f"🔥 صید مشتی! لایک: {likes} | کامنت: {replies} | ویو: {views}")
                        
                        retweet_btn = t.query_selector('[data-testid="retweet"]')
                        if retweet_btn:
                            retweet_btn.click()
                            time.sleep(2)
                            confirm_btn = page.query_selector('[data-testid="retweetConfirm"]')
                            if confirm_btn:
                                confirm_btn.click()
                                print("✅ با موفقیت ری‌پست شد!")
                                print("🚬 استراحت ۲ دقیقه‌ای برای جلوگیری از بن...")
                                time.sleep(120)
                            else:
                                print("⚠️ دکمه تایید ری‌پست پیدا نشد.")
                        else:
                            print("♻️ این پست ظاهراً قبلاً ری‌پست شده.")
            
            except Exception as e:
                print(f"❌ ارور تو بررسی اکانت @{account}: {e}")

        browser.close()

if __name__ == "__main__":
    main()
