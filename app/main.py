from fastapi import FastAPI, Request, BackgroundTasks
import uvicorn
from telebot import types
from dotenv import load_dotenv
load_dotenv()
from app.config import PORT, WEBHOOK_URL
from app.handler import bot


app = FastAPI()

@app.post("/webhook")
async def webhook(req: Request, background_tasks: BackgroundTasks):
    update = types.Update.de_json(await req.json())
    background_tasks.add_task(bot.process_new_updates, [update])
    return {"ok": True}

@app.on_event("startup")
def on_startup():
    bot.remove_webhook()
    if WEBHOOK_URL:
        bot.set_webhook(url=WEBHOOK_URL)
    else:
        print("Внимание: WEBHOOK_URL не задан, вебхук не установлен (это нормально для теста и при запуске без туннеля)")
    
if __name__ == '__main__':
    uvicorn.run("app.main:app", host="0.0.0.0", port=PORT)