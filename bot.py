from telegram import Update, InputFile
from telegram.ext import Application, CommandHandler, ContextTypes
import random
import string
import os
import psutil
import time
import aiohttp
from keep_alive import keep_alive
keep_alive()

start_time = time.time()

# Hàm tạo key ngẫu nhiên
def generate_key():
    characters = string.ascii_letters + string.digits
    return "key" + "".join(random.choice(characters) for _ in range(15))

# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Xin chào! 👋\n"
        "Lệnh hỗ trợ:\n"
        "• /random <số lượng>\n"
        "• /randomfile <số lượng>\n"
        "• /system (check Uptime, Delay, Ping, CPU, RAM, Disk)"
    )

# /random <count>
async def random_key(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        count = int(context.args[0]) if context.args else 1
        if count <= 0:
            await update.message.reply_text("❌ Số lượng phải lớn hơn 0.")
            return
        if count > 100:
            await update.message.reply_text("⚠️ Giới hạn tối đa 100 key/lần.")
            return

        keys = [generate_key() for _ in range(count)]
        await update.message.reply_text("\n".join(keys))
    except ValueError:
        await update.message.reply_text("❌ Vui lòng nhập số hợp lệ.\nVí dụ: /random 10")

# /randomfile <count>
async def random_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        count = int(context.args[0]) if context.args else 10
        if count <= 0:
            await update.message.reply_text("❌ Số lượng phải lớn hơn 0.")
            return
        if count > 1000:
            await update.message.reply_text("⚠️ Giới hạn tối đa 1000 key/lần.")
            return

        keys = [generate_key() for _ in range(count)]
        filename = f"keys_{count}.txt"

        with open(filename, "w", encoding="utf-8") as f:
            f.write("\n".join(keys))

        await update.message.reply_document(InputFile(filename))
        os.remove(filename)

    except ValueError:
        await update.message.reply_text("❌ Vui lòng nhập số hợp lệ.\nVí dụ: /randomfile 50")

# /system
async def system_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # delay (bot xử lý tin nhắn)
    start = time.time()
    msg = await update.message.reply_text("🔍 Đang kiểm tra hệ thống...")
    delay = round((time.time() - start) * 1000, 2)

    # uptime
    elapsed = int(time.time() - start_time)
    hours, rem = divmod(elapsed, 3600)
    minutes, seconds = divmod(rem, 60)

    # CPU
    cpu_usage = psutil.cpu_percent(interval=1)

    # RAM
    memory = psutil.virtual_memory()
    ram_total = round(memory.total / (1024**3), 2)
    ram_used = round(memory.used / (1024**3), 2)

    # Disk
    disk_usage = psutil.disk_usage('/')
    disk_total = round(disk_usage.total / (1024**3), 2)
    disk_used = round(disk_usage.used / (1024**3), 2)

    # Ping (Telegram API)
    try:
        async with aiohttp.ClientSession() as session:
            start_ping = time.time()
            async with session.get("https://api.telegram.org") as resp:
                await resp.text()
            ping = round((time.time() - start_ping) * 1000, 2)
    except:
        ping = "❌ Lỗi"

    # Soạn kết quả dạng bảng đẹp
    result = (
        "*📊 System Info:*\n\n"
        f"⏱ *Uptime:* `{hours}h {minutes}m {seconds}s`\n"
        f"📡 *Delay:* `{delay} ms`\n"
        f"📶 *Ping:* `{ping} ms`\n"
        f"⚙️ *CPU:* `{cpu_usage}%`\n"
        f"💾 *RAM:* `{ram_used}/{ram_total} GB ({memory.percent}%)`\n"
        f"📀 *Disk:* `{disk_used}/{disk_total} GB ({disk_usage.percent}%)`"
    )

    await msg.edit_text(result, parse_mode="Markdown")

def main():
    application = Application.builder().token("YOUR_BOT_TOKEN").build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("random", random_key))
    application.add_handler(CommandHandler("randomfile", random_file))
    application.add_handler(CommandHandler("system", system_info))

    application.run_polling()

if __name__ == "__main__":
    main()
    
