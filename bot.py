import telebot
import random
import string
import json
from datetime import datetime, timedelta
from telegram import Update
from keep_alive import keep_alive
keep_alive()

BOT_TOKEN = "7423511373:AAEvyN0Kwl47WvzmHq-sRo5QdhR1-i8cRiU"
ADMIN_IDS = [7761915412]
bot = telebot.TeleBot(BOT_TOKEN)

history = []
profit = 0
user_turns = {}
DATA_FILE = "data.json"
now = datetime.now().strftime("%H:%M:%S - %d/%m/%Y")

def analyze_md5(md5_hash):
    global history

# ======== Thuật toán 1: 2 ký tự cuối =========
    algo1 = int(md5_hash[-2:], 16) % 2
    result1 = "Tài" if algo1 == 0 else "Xỉu"

# ======== Thuật toán 2: Tổng 4 byte đầu MD5 =========
    total_hex = sum(int(md5_hash[i:i+2], 16) for i in range(0, 8, 2))
    result2 = "Tài" if total_hex % 2 == 0 else "Xỉu"

# ======== Thuật toán 3: Tổng toàn bộ MD5 chia cho 5 =========
    full_sum = sum(int(md5_hash[i:i+2], 16) for i in range(0, 32, 2))
    result3 = "Tài" if full_sum % 5 < 3 else "Xỉu"

# ======== Tính Phiếu =========
    results = [result1, result2, result3]
    final_result = max(set(results), key=results.count)

    prediction = {
        "md5": md5_hash,
        "dự đoán": final_result,
        "thuật toán": {
            "thuật toán 1": result1,
            "thuật toán 2": result2,
            "thuật toán 3": result3,
        },
        "kết quả thực tế": None
    }
    history.append(prediction)

    return (f"✅ KẾT QUẢ PHÂN TÍCH PHIÊN TÀI XỈU MD5:\n"
            f"🔹 MD5: {md5_hash}\n\n"
            f"📊 Kết quả theo từng thuật toán:\n"
            f"   - Thuật toán 1 (2 ký tự cuối): {result1}\n"
            f"   - Thuật toán 2 (4 byte đầu): {result2}\n"
            f"   - Thuật toán 3 (Tổng toàn MD5): {result3}\n\n"
            f"✅ Kết luận cuối cùng: {final_result} | 🎯 Tín hiệu mạnh!\n"
            f"💡 Gợi ý: Cầu {final_result} đang lên mạnh!\n"
            f"🕒 {now} ")

def save_data():
    with open(DATA_FILE, "w") as f:
        json.dump({"user_turns": user_turns, "history": history, "profit": profit}, f)

def load_data():
    global user_turns, history, profit
    try:
        with open(DATA_FILE, "r") as f:            
            data = json.load(f)
            user_turns = data["user_turns"]
            history = data["history"]
            profit = data["profit"]
    except FileNotFoundError:
        save_data()

# ======== Thuật Toán 2 =========
def analyze_md5v1(md5_hash):
    global history

    value1 = int(md5_hash[:8], 16)
    value2 = int(md5_hash[8:16], 16)
    value3 = int(md5_hash[16:24], 16)
    value4 = int(md5_hash[24:32], 16)

    total_value = (value1 + value2 + value3 + value4) % 100
    avg_value = (value1 + value2 + value3 + value4) // 4
    last_digit = int(md5_hash[-1], 16)

    if total_value < 50:
        result = "🔴 Xỉu (Small) | 🎯 Xác suất cao!"
        clean_result = "Xỉu"
    else:
        result = "⚪ Tài (Big) | 🎯 Xác suất cao!"
        clean_result = "Tài"

    prediction = {
        "md5": md5_hash,
        "dự đoán": clean_result,
        "kết quả thực tế": None
    }
    history.append(prediction)

    return (f"✅ KẾT QUẢ PHÂN TÍCH PHIÊN TÀI XỈU MD5:\n"
            f"✨ PHÂN TÍCH CHI TIẾT ✨\n"
            f"🔹 MD5: {md5_hash}\n"
            f"   - Giá trị 8 ký tự đầu: {value1}\n"
            f"   - Giá trị 8 ký tự giữa: {value2}\n"
            f"   - Giá trị 8 ký tự tiếp theo: {value3}\n"
            f"   - Giá trị 8 ký tự cuối: {value4}\n"
            f"   - Tổng giá trị: {total_value}\n"
            f"   - Trung bình giá trị: {avg_value}\n"
            f"   - Chữ số cuối MD5: {last_digit}\n"
            f"   - Dự đoán: {result}\n"
            f"   - Nhận định: 🔥 Tín hiệu mạnh! Đặt {clean_result} ngay!\n"
            f"💡 Gợi ý: Cầu {clean_result} đang mạnh!\n"
            f"💎 VIP Signal - Dành cho anh em chuyên nghiệp! 💎")

def save_data():
    with open(DATA_FILE, "w") as f:
        json.dump({"user_turns": user_turns, "history": history, "profit": profit}, f)

def load_data():
    global user_turns, history, profit
    try:
        with open(DATA_FILE, "r") as f:
            data = json.load(f)
            user_turns = data["user_turns"]
            history = data["history"]
            profit = data["profit"]
    except FileNotFoundError:
        save_data()

load_data()

# ======== Thuật Toán Tổng Hợp (Gộp thuật toán 1 với thuật toán 2) =========
def analyze_md5v2(md5_hash):
    global history

    # Thuật toán 1: 2 ký tự cuối ( thuật toán 1 )
    algo1 = int(md5_hash[-2:], 16) % 2
    result1 = "Tài" if algo1 == 0 else "Xỉu"

    # Thuật toán 2: Tổng 4 byte đầu MD5 ( thuật toán 1 )
    total_hex = sum(int(md5_hash[i:i+2], 16) for i in range(0, 8, 2))
    result2 = "Tài" if total_hex % 2 == 0 else "Xỉu"

    # Thuật toán 3: Tổng toàn bộ MD5 chia cho 5 ( thuật toán 1 )
    full_sum = sum(int(md5_hash[i:i+2], 16) for i in range(0, 32, 2))
    result3 = "Tài" if full_sum % 5 < 3 else "Xỉu"

    # Tính phiếu ( thuật toán 1 )
    results = [result1, result2, result3]
    final_result = max(set(results), key=results.count)
    
    # Thuật toán 2    
    value1 = int(md5_hash[:8], 16)
    value2 = int(md5_hash[8:16], 16)
    value3 = int(md5_hash[16:24], 16)
    value4 = int(md5_hash[24:32], 16)

    total_value = (value1 + value2 + value3 + value4) % 100
    avg_value = (value1 + value2 + value3 + value4) // 4
    last_digit = int(md5_hash[-1], 16)

    if total_value < 50:
        result = "🔴 Xỉu (Small) | 🎯 Xác suất cao!"
        final_result = "Xỉu"
    else:
        result = "⚪ Tài (Big) | 🎯 Xác suất cao!"
        final_result = "Tài"
    prediction = {
        "md5": md5_hash,
        "dự đoán": final_result,
        "thuật toán": {
            "thuật toán 1": result1,
            "thuật toán 2": result2,
            "thuật toán 3": result3,
        },
        "kết quả thực tế": None
    }
    history.append(prediction)
    
    return (f"✅ KẾT QUẢ PHÂN TÍCH PHIÊN TÀI XỈU MD5:\n"
            f"✨ PHÂN TÍCH CHI TIẾT ✨\n"
            f"🔹 MD5: {md5_hash}\n"
            f"   - Thuật toán 1 (2 ký tự cuối): {result1}\n"
            f"   - Thuật toán 2 (4 byte đầu): {result2}\n"
            f"   - Thuật toán 3 (Tổng toàn MD5): {result3}\n"
            f"   - Thuật toán 4 (8 ký tự đầu): {value1}\n"
            f"   - Thuật toán 5 (8 ký tự giữa): {value2}\n"
            f"   - Thuật toán 6 (8 ký tự tiếp theo): {value3}\n"
            f"   - Thuật Toán 7 (8 ký tự cuối): {value4}\n"
            f"   - Tổng giá trị: {total_value}\n"
            f"   - Trung bình giá trị: {avg_value}\n"
            f"   - Chữ số cuối MD5: {last_digit}\n"
            f"   - Dự đoán: {result}\n"
            f"   - Nhận định: 🔥 Tỉ lệ thắng cao! Đặt {final_result} ngay!\n"
            f"💡 Gợi ý: Cầu {final_result} đang mạnh!\n"
            f"💎 VIP Signal - Dành cho anh em chuyên nghiệp! 💎")
            
def save_data():
    with open(DATA_FILE, "w") as f:
        json.dump({"user_turns": user_turns, "history": history, "profit": profit}, f)

def load_data():
    global user_turns, history, profit
    try:
        with open(DATA_FILE, "r") as f:
            data = json.load(f)
            user_turns = data["user_turns"]
            history = data["history"]
            profit = data["profit"]
    except FileNotFoundError:
        save_data()
        
# ======== Lệnh /start =========
@bot.message_handler(commands=['start'])
def send_welcome(message):
    
    user_id = message.from_user.id
    bot.reply_to(message, f"👋 Chào mừng đến với BOT TÀI XỈU VIP!\n"
                          f"🔹 /tx <mã MD5> → Dự đoán kết quả (mỗi lần trừ 1 lượt)\n"
                          f"🔹 /tx1 <mã MD5> → Dự đoán kết quả (mỗi lần trừ 1 lượt)\n"
                          f"🔹 /tx2 <mã MD5> → Dự đoán kết quả (mỗi lần trừ 1 lượt)\n"
                          f"🔹 /nap <số tiền> → Mua lượt dùng\n"
                          f"🔹 /dabank <số tiền> <nội dung> → Gửi thông tin giao dịch ngân hàng để admin duyệt\n"
                          f"🔹 /history → Xem lịch sử & lãi/lỗ\n"
                          f"🔹 /support → Liên hệ hỗ trợ\n"
                          f"🔹 /id → lấy id của bạn\n"
                          f"🔹 /report <nội dung> → Báo lỗi về bot\n"
                          f"🚫 Lệnh cho Quản Trị Viên.\n"
                          f"🔹 /congluot <id/tun> → Cấp lượt dùng\n"
                          f"🔹 /truluot <id/tun> → Trừ lượt dùng\n"
                          f"🔹 /result <tài/xỉu> → Nhập kết quả thực tế (Admin)\n"
                          f"🆔️ ID của bạn là: {user_id}\n")

# ======== lệnh /id =========
@bot.message_handler(commands=['id'])
def handle_id(message):
    user_id = message.from_user.id
    turns = user_turns.get(user_id, 0)
    bot.reply_to(message, f"🆔️ ID của bạn là: {user_id}\n🎫 Lượt còn lại: {turns}")
    

# ======== lệnh /tx =========
@bot.message_handler(commands=['tx'])
def get_tx_signal(message):
    user_id = message.from_user.id
    parts = message.text.split()
    if len(parts) < 2 or len(parts[1]) != 32:
        bot.reply_to(message, "❌ Vui lòng nhập mã MD5 hợp lệ!\n🔹 Ví dụ: /tx d41d8cd98f00b204e9800998ecf8427e")
        return

    turns = user_turns.get(user_id, 0)
    if turns <= 0:
        bot.reply_to(message, "⚠️ Bạn đã hết lượt dùng! Vui lòng dùng lệnh /nap <số tiền> để mua thêm.")
        return

    user_turns[user_id] = turns - 1
    save_data()
    md5_hash = parts[1]
    result_analysis = analyze_md5(md5_hash)
    bot.reply_to(message, result_analysis + f"\n\n🆔️ ID của bạn: {user_id}\n🎫 Lượt còn lại của bạn: {turns}")
    

# ======== Lệnh /tx1 =========
@bot.message_handler(commands=['tx1'])
def get_tx_signal(message):
    user_id = message.from_user.id
    parts = message.text.split()
    if len(parts) < 2 or len(parts[1]) != 32:
        bot.reply_to(message, "❌ Vui lòng nhập mã MD5 hợp lệ!\n🔹 Ví dụ: /tx d41d8cd98f00b204e9800998ecf8427e")
        return

    turns = user_turns.get(user_id, 0)
    if turns <= 0:
        bot.reply_to(message, "⚠️ Bạn đã hết lượt dùng! Vui lòng dùng lệnh /nap <số tiền> để mua thêm.")
        return

    user_turns[user_id] = turns - 1
    save_data()
    md5_hash = parts[1]
    result_analysis = analyze_md5v1(md5_hash)
    bot.reply_to(message, result_analysis + f"\n\n🆔️ ID của bạn: {user_id}\n🎫 Lượt còn lại của bạn: {turns}")

# ======== Lệnh /tx2 =========
@bot.message_handler(commands=['tx2'])
def get_tx_signal(message):
    user_id = message.from_user.id
    parts = message.text.split()
    if len(parts) < 2 or len(parts[1]) != 32:
        bot.reply_to(message, "❌ Vui lòng nhập mã MD5 hợp lệ!\n🔹 Ví dụ: /tx d41d8cd98f00b204e9800998ecf8427e")
        return

    turns = user_turns.get(user_id, 0)
    if turns <= 0:
        bot.reply_to(message, "⚠️ Bạn đã hết lượt dùng! Vui lòng dùng lệnh /nap <số tiền> để mua thêm.")
        return

    user_turns[user_id] = turns - 1
    save_data()
    md5_hash = parts[1]
    result_analysis = analyze_md5v2(md5_hash)
    bot.reply_to(message, result_analysis + f"\n\n🆔️ ID của bạn: {user_id}\n🎫 Lượt còn lại của bạn: {turns}")
    
# ======== Lệnh /result =========
@bot.message_handler(commands=['result'])
def set_actual_result(message):
    global profit
    if message.from_user.id not in ADMIN_IDS:
        bot.reply_to(message, "⛔ Bạn không có quyền sử dụng lệnh này!")
        return

    parts = message.text.split()
    if len(parts) < 2 or parts[1].lower() not in ["tài", "xỉu"]:
        bot.reply_to(message, "❌ Nhập kết quả hợp lệ! (tài/xỉu)")
        return

    actual_result = parts[1].capitalize()
    if not history:
        bot.reply_to(message, "⚠️ Chưa có dự đoán nào!")
        return

    last_prediction = history[-1]
    last_prediction["kết quả thực tế"] = actual_result

    if last_prediction["dự đoán"] == actual_result:
        profit += 1
        status = "✅ Thắng kèo! 📈 (+1 điểm)"
    else:
        profit -= 1
        status = "❌ Thua kèo! 📉 (-1 điểm)"

    save_data()
    bot.reply_to(message, f"📢 Cập nhật kết quả: {actual_result}\n{status}\n💰 Tổng lãi/lỗ: {profit} điểm")

# ======== Lệnh /history =========
@bot.message_handler(commands=['history'])
def show_history(message):
    if not history:
        bot.reply_to(message, "📭 Chưa có dữ liệu lịch sử!")
        return

    history_text = "📜 LỊCH SỬ DỰ ĐOÁN & KẾT QUẢ:\n"
    for idx, entry in enumerate(history[-5:], start=1):
        history_text += f"🔹 Lần {idx}:\n"
        history_text += f"   - 📊 Dự đoán: {entry['dự đoán']}\n"
        history_text += f"   - 🎯 Kết quả thực tế: {entry['kết quả thực tế'] or '❓ Chưa có'}\n"

    user_id = message.from_user.id
    turns = user_turns.get(user_id, 0)
    history_text += f"\n💰 Tổng lãi/lỗ: {profit} điểm\n🎫 Lượt còn lại: {turns}"
    bot.reply_to(message, history_text)

# ======== Lệnh /nep =========
@bot.message_handler(commands=['nap'])
def handle_nap(message):
    parts = message.text.split()
    if len(parts) < 2 or not parts[1].isdigit():
        bot.reply_to(message, "❌ Vui lòng nhập số tiền hợp lệ! Ví dụ: /nap 100000")
        return

    amount = int(parts[1])
    user_id = message.from_user.id
    turns = amount // 500
    if turns < 20 or turns > 20000:
        bot.reply_to(message, "⚠️ Bạn chỉ được mua từ 20 đến 20000 lượt (tương ứng từ 10,000đ đến 10,000,000đ).")
        return

    code = generate_nap_code()
    reply = (f"💳 HƯỚNG DẪN NẠP TIỀN MUA LƯỢT\n\n"
             f"➡️ Số tài khoản: 19073770977019\n"
             f"➡️ Ngân hàng: Techcombank \n"
             f"➡️ Số tiền: {amount} VNĐ\n"
             f"➡️ Nội dung chuyển khoản: NAP{code}\n"
             f"⏳ Sau khi chuyển khoản, admin sẽ duyệt và cộng {turns} lượt cho bạn.\n"
             f"🔹 Bạn có thể lấy id sau đó gửi bill và id của bạn cho @qqaassdd1231 để được duyệt nhanh hơn\n"
             f"🆔️ ID của bạn là: {user_id}")

    for admin_id in ADMIN_IDS:
        bot.send_message(admin_id, f"📥 YÊU CẦU NẠP TIỀN\n"
                                   f"👤 User ID: {user_id}\n"
                                   f"💰 Số tiền: {amount} VNĐ\n"
                                   f"🎫 Lượt mua: {turns}\n"
                                   f"📝 Nội dung: NAP{code}\n\n"
                                   f"📥 Duyệt bằng lệnh: /congluot {user_id} {turns}")

    bot.reply_to(message, reply)

# ======== Lệnh /congluot =========
@bot.message_handler(commands=['congluot'])
def congluot_nap(message):
    if message.from_user.id not in ADMIN_IDS:
        bot.reply_to(message, "⛔ Bạn không có quyền sử dụng lệnh này!")
        return

    parts = message.text.split()
    if len(parts) < 3 or not parts[1].isdigit() or not parts[2].isdigit():
        bot.reply_to(message, "❌ Sai cú pháp. Dùng /congluot <user_id> <số lượt>")
        return

    uid = int(parts[1])
    turns = int(parts[2])
    user_turns[uid] = user_turns.get(uid, 0) + turns

    save_data()
    bot.send_message(uid, f"✅ Bạn đã được cộng {turns} lượt dùng!\n🎫 Lượt mới của bạn: {turns}\n🎯 Dùng lệnh /tx <md5> để dự đoán")
    bot.reply_to(message, f"📥 Đã cộng {turns} lượt cho user {uid}.")

# ======== Lệnh /truluot =========
@bot.message_handler(commands=['truluot'])
def truluot_nap(message):
    if message.from_user.id not in ADMIN_IDS:
        bot.reply_to(message, "⛔ Bạn không có quyền sử dụng lệnh này!")
        return

    parts = message.text.split()
    if len(parts) < 3 or not parts[1].isdigit() or not parts[2].isdigit():
        bot.reply_to(message, "❌ Sai cú pháp. Dùng /truluot <user_id> <số lượt>")
        return

    uid = int(parts[1])
    turns = int(parts[2])
    user_turns[uid] = user_turns.get(uid, 0) - turns

    save_data()
    bot.send_message(uid, f"🚫OOPS. Bạn đã bị trừ lượt dùng!\n🎫 Số lượt mới của bạn sau khi bị trừ là: {turns}\n🎲 Nếu bạn thắc mắc tại sao bị trừ. Vui lòng liên hệ @qqaassdd1231")
    bot.reply_to(message, f"📥 Đã trừ {turns} lượt của user {uid}.")

# ======== Lệnh /dabank =========
@bot.message_handler(commands=['dabank'])
def handle_dabank(message):
    parts = message.text.split()
    if len(parts) < 3:
        bot.reply_to(message, "❌ Vui lòng nhập đầy đủ thông tin giao dịch.\nVí dụ: /dabank 100000 Nội dung chuyển tiền hoặc mã giao dịch")
        return

    amount = parts[1]
    content = " ".join(parts[2:])
    user_id = message.from_user.id

    for admin_id in ADMIN_IDS:
        bot.send_message(admin_id, f"📥 YÊU CẦU NẠP TIỀN (GIAO DỊCH NGÂN HÀNG)\n"
                                   f"👤 User ID: {user_id}\n"
                                   f"💰 Số tiền: {amount} VNĐ\n"
                                   f"📝 Nội dung: {content}\n\n"
                                   f"Duyệt bằng lệnh: /congluot {user_id} {amount}")

    bot.reply_to(message, f"⏳ Đang chờ admin duyệt giao dịch.\n"
                          f"📥 Sau khi admin duyệt, bạn sẽ nhận được lượt dùng.\n"
                          f"💰 Số tiền: {amount} VNĐ\n"
                          f"📝 Nội dung:{content}\n"
                          f"🔹 Bạn có thể lấy id sau đó gửi bill và id của bạn cho @qqaassdd1231 để được duyệt nhanh hơn\n"
                          f"🆔️ ID của bạn là: {user_id}")

# ======== Lệnh /report =========
@bot.message_handler(commands=['report'])
def handle_report(message):
    parts = message.text.split()
    if len(parts) < 3:
        bot.reply_to(message, "❌ Vui lòng nhập lỗi mà bạn muốn báo\n 📝 Nhập theo lệnh /report <tiêu đề/thông tin chi tiết>\n✨️ Lưu ý: Tiêu đề phải cách nhau bằng 1 dấu (Vd: Tiêu đề là Lỗi trừ lượt thì viết Lỗi-trừ-lượt)")
        return
        
    title = parts[1]
    content = " ".join(parts[3:])
    user_id = message.from_user.id

    for admin_id in ADMIN_IDS:
        bot.send_message(admin_id, f"🚀 Thông báo lỗi từ người dùng\n"
                                   f"👤 User ID: {user_id}\n"
                                   f"📝 Tiêu dề: {title}\n"
                                   f"📝 Nội dung: {content}\n\n"
                                   f"👾 Sử dụng lệnh /sendmessage để thông báo tời người dùng báo lỗi")

    bot.reply_to(message, f"⏳ Đang chờ admin phản hồi\n"
                          f"📥 Sau khi admin phản hồi, lỗi của bạn sẽ được admin hỗ trợ fix\n"
                          f"📝 Tiêu đề: {title}\n"
                          f"📝 Nội dung:{content}\n"
                          f"🔹 Bạn có thể báo lỗi cho admin tại @qqaassdd để được hỗ trợ nhanh hơn\n"
                          f"🆔️ ID của bạn là: {user_id}")

# ======== Lệnh /sendmessage =========
@bot.message_handler(commands=['sendmessage'])
def send_message(message):
    if message.from_user.id not in ADMIN_IDS:
        bot.reply_to(message, "⛔ Bạn không có quyền sử dụng lệnh này!")
        return

    parts = message.text.split()
    if len(parts) < 3:
        bot.reply_to(message, "❌ Sai cú pháp\n✒️ Vui lòng nhập theo lệnh /sendmessage <id/tiêu đề/nội dung>\n\n✨️ Lưu ý: Tiêu đề phải cách nhau bằng 1 dấu (Vd: Tiêu đề là Lỗi trừ lượt thì viết Lỗi-trừ-lượt)")
        return

    uid = int(parts[1])
    title = parts[2]
    content = " ".join(parts[3:])
    user_id = message.from_user.id

    save_data()
    bot.send_message(uid, f"✉️ Phản hồi từ admin\n👾 Tiêu đề: {title}\n✒️Nội Dung: {content} ")
    bot.reply_to(message, f"📥 Đã phản hồi report đến người dùng {uid}\n👾 Tiêu đề: {title}\n✉️ Nội dung: {content}")

# ======== Lệnh /support =========
@bot.message_handler(commands=['support'])
def handle_support(message):
    bot.reply_to(message, "📩 Nếu bạn cần hỗ trợ, vui lòng liên hệ với ctv tại: @nghuypha\n📩 Nếu bạn có thắc mắc về bot vui lòng liên hệ với quản trị viên bot tại: @hoanglong3703\n\n👾 Note: chúng tôi chuẩn bị cập nhật trang hỗ trợ thành live chat")

bot.polling()
