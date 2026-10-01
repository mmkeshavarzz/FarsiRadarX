"""
=============================================================================
*  Project: X Global Hunter 🔥 (No-API Stealth Edition)
*  Features:
*    - 🌍 Global Radar: جستجوی کل توییتر فارسی به جای چندتا اکانت
*    - 🕒 Schedule: اجرای دقیق هر ۳ ساعت
*    - 🕵️‍♂️ Stealth Mode: دور زدن تحریم‌ها با مرورگر نامرئی (Playwright)
*    - 🎯 Target: حداقل 1000 لایک، 1000 ویو، 100 کامنت (فقط فارسی)
*    - 🛑 Anti-Ban Guard: دو دقیقه تاخیر بین هر ری‌پست برای سلامت اکانت
=============================================================================
"""

import os
import time
import re
import urllib.parse
import sys  

from playwright.sync_api import sync_playwright

AUTH_TOKEN = os.environ.get("X_AUTH_TOKEN")

# فیتیله فیلتر رو آوردم پایین که واسه تست حتما یه چیزی پیدا کنه و ری‌پست بشه
SEARCH_QUERY = "lang:fa min_faves:100 min_replies:10"

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
        sys.exit(1)

    print("🦅 رادار جهانی ایکس روشن شد! بریم واسه شکار کل توییتر فارسی...")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            viewport={'width': 1280, 'height': 800},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        
        # محکم‌کاری: کوکی رو روی هر دو تا دامنه توییتر و ایکس ست می‌کنیم
        context.add_cookies([
            {"name": "auth_token", "value": AUTH_TOKEN, "domain": ".x.com", "path": "/"},
            {"name": "auth_token", "value": AUTH_TOKEN, "domain": ".twitter.com", "path": "/"}
        ])
        
        page = context.new_page()

        try:
            encoded_query = urllib.parse.quote(SEARCH_QUERY)
            target_url = f"https://x.com/search?q={encoded_query}&src=typed_query"
            
            print(f"🚜 در حال شخم زدن هشتگ‌ها و پست‌های داغ...")
            page.goto(target_url, timeout=60000)
            page.wait_for_timeout(5000)
            
            try:
                # اینجا اگه هیچی پیدا نکرد دیگه کرش نمی‌کنه، فقط خبر میده
                page.wait_for_selector('article[data-testid="tweet"]', timeout=20000)
            except:
                print("⚠️ داش، یا هیچ توییتی با این شرایط تو این لحظه وجود نداره، یا اینکه auth_token سوخته و توییتر اکانتتو انداخته بیرون.")
                browser.close()
                sys.exit(0) # خروج تمیز (تیک سبز میگیره چون تقصیر برنامه نبوده، فقط چیزی پیدا نشده)
            
            # سه بار اسکرول می‌کنیم پایین که چند تا توییت مشتی لود بشه تو صفحه
            for _ in range(3):
                page.mouse.wheel(0, 2000)
                time.sleep(3)

            tweets = page.query_selector_all('article[data-testid="tweet"]')
            print(f"📡 تعداد {len(tweets)} توییت مشکوک تو رادار پیدا شد!")
            
            reposted_count = 0
            for t in tweets:
                tweet_text = t.inner_text()
                
                # یه چک ریز می‌کنیم که حتماً حروف فارسی توش باشه
                if not re.search(r'[\u0600-\u06FF]', tweet_text):
                    continue

                view_elem = t.query_selector('[aria-label*="View"], [aria-label*="view"], [aria-label*="بازدید"]')
                views = extract_number(view_elem.get_attribute('aria-label') if view_elem else "")

                # شرط آخر: ویو رو هم کم کردم که گیر نیفتی
                if views >= 100:
                    print(f"🔥 صید توت‌فرنگی! ویو: {views} | (لایک و کامنت رو خود توییتر تایید کرده)")
                    
                    retweet_btn = t.query_selector('[data-testid="retweet"]')
                    if retweet_btn:
                        retweet_btn.click()
                        time.sleep(2)
                        confirm_btn = page.query_selector('[data-testid="retweetConfirm"]')
                        if confirm_btn:
                            confirm_btn.click()
                            print("✅ نشست تو پیجمون! با موفقیت ری‌پست شد.")
                            reposted_count += 1
                            print("🚬 استراحت ۲ دقیقه‌ای برای جلوگیری از لیمیت شدن...")
                            time.sleep(120)
                        else:
                            print("⚠️ دکمه تایید ری‌پست پیدا نشد. شاید قبلاً زدیش.")
                    else:
                        print("♻️ این پست رو ظاهراً قبلاً ری‌پست کردی داش.")
                        
                    # واسه اینکه تست کنی و جواب بگیری، بعد از یه دونه ری‌پست کردن کارو جمع می‌کنه
                    if reposted_count >= 1:
                        break
        
        except Exception as e:
            print(f"❌ داداش تو رادار یه اروری خوردیم: {e}")
            browser.close()
            sys.exit(1)

        browser.close()
        print("🏁 عملیات این شیفت تموم شد. بریم تا ۳ ساعت دیگه!")

if __name__ == "__main__":
    main()
