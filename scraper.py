import os
import asyncio
from twikit import Client

async def hunt_hot_tweets():
    print("🚀 [۱] بیدارباش شکارچی! اتصال به توییتر...")
    
    # واکشی کوکی‌ها
    auth_token = os.environ.get("GAPGPTMASKTOKEN6yqe276tx2dX1X")
    ct0 = os.environ.get("CT0")
    
    if not auth_token or not ct0:
        print("❌ ای بابا! سکرت‌ها خالی هستند! گیت‌هاب چیزی تحویل نداد.")
        return

    client = Client(language='en-US')
    client.set_cookies({
        'auth_token': auth_token,
        'ct0': ct0
    })

    query = "lang:fa min_faves:1000" # یا کوئری دقیق خودت
    print(f"🔎 [۲] جستجو با فرمول جادویی: '{query}'")
    
    try:
        # جستجو در تب پرطرفدارترین‌ها (Top)
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
            history = set(line.strip() for line in f)

    reposted_count = 0
    for tweet in tweets:
        print(f"--- بررسی توییت {tweet.id}: لایک: {tweet.favorite_count} | کامنت: {tweet.reply_count} | ویو: {getattr(tweet, 'view_count', 'نامشخص')}")
        
        if tweet.id in history:
            print(f"⏭️ توییت {tweet.id} تکراری بود، اسکیپ شد.")
            continue
            
        # اگر همه شروط پاس شد:
        print(f"🔥 شکار شد! در حال ری‌پست کردن {tweet.id}...")
        try:
            await tweet.retweet()
            # ثبت در تاریخچه
            with open("history.txt", "a", encoding="utf-8") as f:
                f.write(f"{tweet.id}\n")
            print("✅ با موفقیت ری‌پست شد!")
            reposted_count += 1
            break # فقط یک شکار در هر اجرا
        except Exception as err:
            print(f"🤦‍♂️ هنگام ری‌پست تو زرد از آب دراومد: {err}")

    if reposted_count == 0:
        print("🤷‍♂️ از بین تمام گزینه‌ها، هیچ کدوم استانداردهای سخت‌گیرانه‌ی ما رو پاس نکردن!")

if __name__ == "__main__":
    asyncio.run(hunt_hot_tweets())
