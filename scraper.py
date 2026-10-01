"""
=============================================================================
*  Project: X Hot Posts Hunter 🔥 (3-HOUR SHIFT EDITION)
*  Features:
*    - 🍪 Zero API: دور زدن محدودیت‌های توییتر!
*    - 🕒 3-Hour Patrol: اجرای گشت هر ۳ ساعت یک‌بار
*    - 🧠 Smart Memory: ثبت تاریخچه در history.txt برای جلوگیری از تکرار
*    - ⏳ Time Filter: فقط و فقط توییت‌های ۳ ساعت اخیر!
=============================================================================
"""

import os
import asyncio
from datetime import datetime, timedelta, timezone
from twikit import Client

# 🔑 کوکی‌های دریافتی از اکانت مجزا (دقیقاً هم‌اسم با محیط سیستم)
AUTH_TOKEN = os.environ.get("AUTH_TOKEN", "")
CT0 = os.environ.get("CT0", "")
HISTORY_FILE = "history.txt"

# 🎯 فیلترهای شکار
MIN_LIKES = 1000
MIN_VIEWS = 1000
MIN_REPLIES = 100

def load_history():
    # باز کردن دفترچه خاطرات ربات 📖
    if not os.path.exists(HISTORY_FILE):
        return set()
    with open(HISTORY_FILE, "r") as f:
        return set(line.strip() for line in f)

def save_history(tweet_id):
    # ثبت کردن اسم مجرم (آیدی توییت) تو لیست سیاه 🏴‍☠️
    with open(HISTORY_FILE, "a") as f:
        f.write(f"{tweet_id}\n")

async def main():
    print("🦅 عقاب تیزپرواز ایکس وارد می‌شود... (شیفت ۳ ساعته)")

    # چک می‌کنیم نگهبان‌ها سر پستشون باشن!
    if not AUTH_TOKEN or not CT0:
        print("❌ ای بابا! کوکی‌ها کجان؟ توی Secrets ست نکردی یا آدرس اشتباهه؟")
        return

    client = Client(language='fa')
    # اینجا هم اسم‌های درست رو به کلاینت پاس می‌دیم
    client.set_cookies(auth_token=AUTH_TOKEN, ct0=CT0)
    
    history = load_history()
    print(f"📚 تعداد {len(history)} توییت قبلاً شکار شده و تو حافظه‌ست.")

    # محاسبه دقیق زمان ۳ ساعت پیش (توییتر به وقت UTC کار می‌کنه)
    three_hours_ago = datetime.now(timezone.utc) - timedelta(hours=3)
    
    search_query = f"lang:fa min_faves:{MIN_LIKES} min_replies:{MIN_REPLIES} -is:retweet"
    print(f"🔍 در حال بو کشیدن تایم‌لاین...")
    
    try:
        tweets = await client.search_tweet(search_query, product='Top')
        
        if not tweets:
            print("📭 تو این شیفت پرنده‌ای پر نزده! میریم تا ۳ ساعت دیگه.")
            return

        repost_count = 0
        for tweet in tweets:
            # ۱. چک کردن حافظه (نکنه قبلاً ری‌پستش کرده باشیم؟) 🤔
            if str(tweet.id) in history:
                continue
            
            # ۲. بررسی تاریخ تولد توییت (فقط ۳ ساعت اخیر باشه) ⏳
            try:
                # تبدیل فرمت عجیب توییتر به فرمت قابل فهم برای پایتون
                tweet_date = datetime.strptime(tweet.created_at, '%a %b %d %H:%M:%S +0000 %Y').replace(tzinfo=timezone.utc)
                if tweet_date < three_hours_ago:
                    print(f"تاریخ گذشته: توییت {tweet.id} بیات شده! اسکیپ شد ⏭️")
                    continue
            except Exception as e:
                print(f"⚠️ مشکل در خوندن تاریخ این توییت: {e}")
                continue

            # ۳. بررسی ویو (در صورت وجود) 👀
            views = int(getattr(tweet, 'view_count', 0) or 0)
            if views < MIN_VIEWS and views != 0:
                continue

            print(f"\n✅ شکار موفق! ری‌پست کردن: {tweet.id} از @{tweet.user.screen_name}")
            try:
                await tweet.retweet()
                save_history(tweet.id)
                repost_count += 1
                
                print("🛑 صبر تاکتیکی (۲ دقیقه) تا الگوریتم‌های توییتر بهمون شک نکنن...")
                await asyncio.sleep(120)
            except Exception as e:
                print(f"⚠️ نشد که بشه (احتمالاً لیمیت شدیم یا پاک شده): {e}")

        print(f"\n🏁 شیفت تموم شد! تو این دور {repost_count} تا پست جدید شکار کردیم.")
            
    except Exception as e:
        print(f"❌ ای داد بر من! خطا خوردیم: {e}")

if __name__ == "__main__":
    asyncio.run(main())
