import os
import asyncio
from twikit import Client

async def hunt_hot_tweets():
    print("🚀 [۱] بیدارباش شکارچی! اتصال به توییتر...")
    
    auth_token = os.environ.get("AUTH_TOKEN")
    ct0 = os.environ.get("CT0")
    twid = os.environ.get("TWID")  # کوکی کمکی واسه محکم‌کاری

    print(f"DEBUG: طول AUTH_TOKEN دریافتی = {len(auth_token) if auth_token else 'صفر یا هیچی (None)'}")
    print(f"DEBUG: طول CT0 دریافتی = {len(ct0) if ct0 else 'صفر یا هیچی (None)'}")
    
    if not auth_token or not ct0:
        print("❌ ای بابا! سکرت‌ها خالی هستند! گیت‌هاب چیزی تحویل نداد.")
        return

    client = Client(language='en-US')
    
    # تنظیم کوکی‌ها به صورت مشتی
    cookies = {
        'auth_token': auth_token,
        'ct0': ct0
    }
    if twid:
        cookies['twid'] = twid

    client.set_cookies(cookies)

    query = "lang:fa min_faves:1000"
    print(f"🔎 [۲] جستجو با فرمول جادویی: '{query}'")
    
    try:
        tweets = await client.search_tweet(query, product='Top')
    except Exception as e:
        print(f"💥 عه! توییتر پا رو سیم انداخت: {e}")
        return

    if not tweets:
        print("📭 [۳] صحرا خشکه! هیچ توییتی با این متر و معیار پیدا نشد.")
        return

    print(f"🎯 [۴] آمار اولیه: {len(tweets)} تا توییت تور شد! حالا وقت غربال‌گریه...")

    # خواندن تاریخچه
    history = set()
    if os.path.exists("history.txt"):
        with open("history.txt", "r", encoding="utf-8") as f:
            history = set(line.strip() for line in f if line.strip())

    reposted_count = 0
    for tweet in tweets:
        tweet_id_str = str(tweet.id)
        print(f"--- بررسی توییت {tweet_id_str}: لایک: {getattr(tweet, 'favorite_count', 0)} | کامنت: {getattr(tweet, 'reply_count', 0)}")
        
        if tweet_id_str in history:
            print(f"⏭️ توییت {tweet_id_str} تکراری بود، اسکیپ شد.")
            continue
            
        print(f"🔥 شکار شد! در حال ری‌پست کردن {tweet_id_str}...")
        try:
            # استفاده از متد مستقیم کلاینت واسه ری‌پست بی‌دردسر
            await client.retweet(tweet.id)
            
            with open("history.txt", "a", encoding="utf-8") as f:
                f.write(f"{tweet_id_str}\n")
            
            print("✅ با موفقیت ری‌پست شد!")
            reposted_count += 1
            break # فقط یک شکار در هر اجرا
        except Exception as err:
            print(f"🤦‍♂️ هنگام ری‌پست تو زرد از آب دراومد: {err}")

    if reposted_count == 0:
        print("🤷‍♂️ از بین تمام گزینه‌ها، هیچ کدوم استانداردهای سخت‌گیرانه‌ی ما رو پاس نکردن!")

if __name__ == "__main__":
    asyncio.run(hunt_hot_tweets())
