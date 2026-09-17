import time
import requests

BOT_TOKEN = "8971974581:AAEtYQUjZzBc6Xms4DgOj8BphM4Zy1rUW3k"
CHANNEL_ID = "@MASSIVELOOTA2Z"
EK_ID = "5643252"

posted_deals = set()

def fetch_and_post():
    api_url = "https://api.earnkaro.com/deals/feed"
    
    try:
        res = requests.get(api_url, timeout=15)
        data = res.json().get("data", [])
        
        for deal in data:
            d_id = deal.get("id")
            if d_id in posted_deals:
                continue
            
            mrp = float(deal.get("mrp", 0))
            price = float(deal.get("selling_price", 0))
            
            if mrp > 0:
                discount = ((mrp - price) / mrp) * 100
                
                if 75 <= discount <= 99:
                    title = deal.get("title")
                    link = f"https://earnkaro.com/deal?url={deal.get('url')}&affid={EK_ID}"
                    photo = deal.get("image")
                    
                    caption = (
                        f"🔥 *MEGA LOOT DEAL ({int(discount)}% OFF)*\n\n"
                        f"🛍️ *Product:* {title}\n"
                        f"❌ *MRP:* ~₹{int(mrp)}~\n"
                        f"🟢 *Deal Price:* *₹{int(price)}*\n"
                        f"🏷️ *Discount:* {int(discount)}% Off!\n\n"
                        f"🔗 *Buy Link:* [Click Here]({link})\n\n"
                        f"⚡ *Hurry Up! Limited Stock.*"
                    )
                    
                    requests.post(
                        f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto",
                        data={
                            "chat_id": CHANNEL_ID,
                            "caption": caption,
                            "photo": photo,
                            "parse_mode": "Markdown"
                        }
                    )
                    
                    posted_deals.add(d_id)
                    time.sleep(2)
                    
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    while True:
        fetch_and_post()
        time.sleep(120)
