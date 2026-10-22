import asyncio
import hashlib
import os
from telethon import TelegramClient, events

BOT_TOKEN = os.environ.get('BOT_TOKEN', '8457775995:AAEECriY33rEK66iU9wzQ8I3yNt8ms0')
MY_CHANNEL = '@halyava_tut_skidki'

DONORS = [
    '@skidki_promokody',
    '@wowskidka1',
    '@sliv_halyavy',
    '@halyava_please',
    '@top_skidki',
    '@skidki_wb_ozon',
    '@besfree',
    '@family_skidki_tg'
]

KEYWORDS = ['ozon', 'wildberries', 'wb', 'скидка', 'промокод', 'халява', 'акция', 'ошибка цены']

seen_messages = set()

client = TelegramClient('halyava_session', api_id=2040, api_hash='b18441a1ff607e10a989891a5462e627')

@client.on(events.NewMessage(chats=DONORS))
async def handler(event):
    if not event.raw_text:
        return
        
    text = event.raw_text
    text_lower = text.lower()
    
    if any(keyword in text_lower for keyword in KEYWORDS):
        text_hash = hashlib.md5(text.encode('utf-8')).hexdigest()
        
        if text_hash in seen_messages:
            print("⏭️ Дубликат пропущен!")
            return
            
        seen_messages.add(text_hash)
        
        if len(seen_messages) > 5000:
            seen_messages.clear()
            
        print(f"✅ Найдена уникальная скидка! Публикуем...")
        await event.forward_to(MY_CHANNEL)

print("🤖 Бот запущен!")
print(f"📢 Канал: {MY_CHANNEL}")
print(f"📡 Отслеживаем: {len(DONORS)} каналов")

client.start(bot_token=BOT_TOKEN)
client.run_until_disconnected()
