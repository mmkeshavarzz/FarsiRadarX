"""
=============================================================================
*  Project: X Hot Posts Hunter 🔥 (COOKIE & USERBOT EDITION)
*  Features:
*    - 🍪 Zero API: بدون نیاز به کلید رسمی و دلارهای ایلان ماسک!
*    - 🕒 Midnight Run: اجرای شبانه راس ساعت ۲۳:۵۹ تهران
*    - 🎯 Strict Filter: حداقل ۱۰۰۰ لایک، ۱۰۰۰ ویو و ۱۰۰ کامنت فارسی
*    - 🛑 Anti-Ban Shield: وقفه ۱۲۰ ثانیه‌ای بین هر ری‌پست
=============================================================================
"""

import os
import asyncio
from twikit import Client

# 🔑 کوکی‌های دریافتی از اکانت مجزا
AUTH_TOKEN = os.environ.get("TWITTER_AUTH_TOKEN", "")
CT0 = os.environ.get("TWITTER_CT0", "")

# 🎯 فیلترهای شکار
MIN_LIKES = 1000
MIN_VIEWS = 1000
MIN_REPLIES = 100

async def main():
    print("🦉 جغد بیدار ایکس با هویت مخفی وارد می‌شود...")

    if not AUTH_TOKEN or not CT0:
        print("❌ کوکی‌های اکانت یافت نشد! auth_token و ct0 رو در Secrets ست کن.")
        return

    # راه‌اندازی کلاینت با کوکی
    client = Client(language='fa')
    client.set_cookies(
        auth_token=AUTH_TOKEN,
        ct0=CT0
    )

    try:
        # جستجوی توییت‌های پرطرفدار فارسی (حذف ری‌توییت‌ها)
        # فرمول سرچ پیشرفته توییتر برای پست‌های داغ
        search_query = f"lang:fa min_faves:{MIN_LIKES} min_replies:{MIN_REPLIES} -is:retweet"
        print(f"🔍 در حال کاوش در تایم‌لاین با کوئری: {search_query}")
        
        tweets = await client.search_tweet(search_query, product='Top')

        if not tweets:
            print("📭 امشب خبری نبوده! هیچ پستی از فیلترهای سنگین ما رد نشد.")
            return

        print(f"🔥 تعداد {len(tweets)} توییت داغ پیدا شد! آماده‌سازی برای ری‌پست...")

        for idx, tweet in enumerate(tweets):
            try:
                # بررسی شرط ویو (در صورت در دسترس بودن متریک)
                views = getattr(tweet, 'view_count', None) or 0
                try:
                    views = int(views)
                except ValueError:
                    views = 0

                # فیلتر نهایی
                if views < MIN_VIEWS and views != 0:
                    continue

                print(f"\n🎯 در حال ری‌پست کردن توییت از: @{tweet.user.screen_name}")
                print(f"❤️ لایک: {tweet.favorite_count} | 💬 کامنت: {tweet.reply_count} | 👁️ ویو: {views}")
                
                # ری‌پست کردن
                await tweet.retweet()
                print("✅ با موفقیت ری‌پست شد!")

                # ترمز ضد بن (۲ دقیقه استراحت)
                if idx < len(tweets) - 1:
                    print("🛑 ترمز اضطراری فعال شد: ۲ دقیقه استراحت برای حفظ امنیت اکانت...")
                    await asyncio.sleep(120)

            except Exception as e:
                print(f"⚠️ خطا در ری‌پست این مورد: {e}")

    except Exception as e:
        print(f"❌ خطای اساسی در ارتباط با ایکس: {e}")

    print("\n🏁 ماموریت امشب به پایان رسید. خسته نباشی دلاور!")

if __name__ == "__main__":
    asyncio.run(main())
