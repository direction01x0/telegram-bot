from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
from flask import Flask
import threading

TOKEN = "8608644995:AAEmElAWdweqkgnh9mEBj9eBQdgkxBnzOrQ"


# ==============================
# 시작 메시지
# ==============================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    keyboard = [
        [InlineKeyboardButton("💰 상품 구매", callback_data="buy_menu")],
        [InlineKeyboardButton("⚠️ 주의사항", callback_data="notice")],
        [InlineKeyboardButton("📞 고객센터", url="https://t.me/FLASHTRC20CS")]
    ]

    await update.message.reply_text(
        "━━━━━━━━━━━━━━━━━━━\n"
        "🔶 디지털 자판기에 오신 것을 환영합니다.\n"
        "🔶 24시간 자동 구매 가능\n"
        "🔶 하단 메뉴 혹은 /start로 시작하세요.\n"
        "🔶 결제 시 안내에 따라 진행해주세요.\n"
        "━━━━━━━━━━━━━━━━━━━\n\n"
        "문의사항이 있으실 경우 하단 메뉴의 고객센터를 이용해주세요.\n"
        "⚠️ 구매 전 주의사항을 꼭 확인하세요 ⚠️\n"
        "━━━━━━━━━━━━━━━━━━━",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


# ==============================
# 상품 버튼
# ==============================
def product_keyboard():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("3만테더 = $250", callback_data="buy_30000"),
            InlineKeyboardButton("7만테더 = $500", callback_data="buy_70000"),
        ],
        [
            InlineKeyboardButton("10만테더 = $700", callback_data="buy_100000"),
            InlineKeyboardButton("20만테더 = $1000", callback_data="buy_200000"),
        ],
        [
            InlineKeyboardButton("50만테더 = $1500", callback_data="buy_500000"),
            InlineKeyboardButton("100만테더 = $2000", callback_data="buy_1000000"),
        ],
        [InlineKeyboardButton("🔙 처음으로", callback_data="go_start")]
    ])


# ==============================
# 결제 버튼
# ==============================
def payment_keyboard(product_code):
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("USDT-TRC20 (TRON)", callback_data=f"pay_trc20_{product_code}")],
        [InlineKeyboardButton("USDT-BEP20 (BSC)", callback_data=f"pay_bep20_{product_code}")],
        [InlineKeyboardButton("USDT-ERC20 (Ethereum)", callback_data=f"pay_erc20_{product_code}")],
        [InlineKeyboardButton("🔙 상품 다시 선택", callback_data="buy_menu")]
    ])


# ==============================
# 버튼 처리
# ==============================
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()
    data = query.data

    # 상품 메뉴
    if data == "buy_menu":
        await query.message.reply_text(
            "💰 구매하실 상품을 선택해주세요.",
            reply_markup=product_keyboard()
        )

    # 상품 선택
    elif data.startswith("buy_"):

        product_code = data.replace("buy_", "")

        price_map = {
            "30000": ("30,000 Flash USDT", "$250"),
            "70000": ("70,000 Flash USDT", "$500"),
            "100000": ("100,000 Flash USDT", "$700"),
            "200000": ("200,000 Flash USDT", "$1000"),
            "500000": ("500,000 Flash USDT", "$1500"),
            "1000000": ("1,000,000 Flash USDT", "$2000"),
        }

        amount, price = price_map.get(product_code, ("", ""))

        await query.message.reply_text(
            f"🔶 {amount} 구매를 선택하셨습니다.\n"
            f"🔶 해당 상품의 가격은 {price} USDT 입니다.\n"
            f"🔶 결제하실 네트워크를 선택해주세요.",
            reply_markup=payment_keyboard(product_code)
        )

    # ==============================
    # 네트워크별 결제 안내
    # ==============================
    elif data.startswith("pay_"):

        parts = data.split("_")
        network_type = parts[1]

        if network_type == "trc20":

            message = (
                "💳 결제 네트워크: USDT-TRC20 (TRON)\n\n"
                "📌 아래 주소로 정확한 금액을 전송해주세요.\n\n"
                "━━━━━━━━━━━━━━━━━━\n"
                "TXbk9M6dASJUBtTXGYxmjcKiFAM8H6mvLb\n"
                "━━━━━━━━━━━━━━━━━━\n\n"
                "⚠️ TRC20 네트워크 외 다른 코인을 전송하실 경우 입금 확인이 불가능합니다.\n\n"
                "🔸결제 후 TXID와 전송받으실 지갑주소를 고객센터로 보내주세요.\n\n"
                "🔵 고객센터 : @FLASHTRC20CS 🔵\n\n"
                "🟣 홈페이지 : https://flash-trc20.com/ 🟣"
            )

        elif network_type == "bep20":

            message = (
                "💳 결제 네트워크: USDT-BEP20 (BSC)\n\n"
                "📌 아래 주소로 정확한 금액을 전송해주세요.\n\n"
                "━━━━━━━━━━━━━━━━━━\n"
                "0x6700639e0c478BE0026Ee1304779a9E85C77b75d\n"
                "━━━━━━━━━━━━━━━━━━\n\n"
                "⚠️ BEP20 네트워크 외 다른 코인을 전송하실 경우 입금 확인이 불가능합니다.\n\n"
                "결제 후 TXID와 전송받으실 지갑주소를 고객센터로 보내주세요.\n\n"
                "🔵 고객센터 : @FLASHTRC20CS 🔵\n\n"
                "🟣 홈페이지 : https://flash-trc20.com/ 🟣"
            )

        elif network_type == "erc20":

            message = (
                "💳 결제 네트워크: USDT-ERC20 (Ethereum)\n\n"
                "📌 아래 주소로 정확한 금액을 전송해주세요.\n\n"
                "━━━━━━━━━━━━━━━━━━\n"
                "0x6700639e0c478BE0026Ee1304779a9E85C77b75d\n"
                "━━━━━━━━━━━━━━━━━━\n\n"
                "⚠️ ERC20 네트워크 외 다른 코인을 전송하실 경우 입금 확인이 불가능합니다.\n\n"
                "🔸결제 후 TXID와 전송받으실 지갑주소를 고객센터로 보내주세요.\n\n"
                "🔵 고객센터 : @FLASHTRC20CS 🔵\n\n"
                "🟣 홈페이지 : https://flash-trc20.com/ 🟣"
            )

        await query.message.reply_text(message)


    elif data == "notice":
        await query.message.reply_text(
            "⚠️ 주의사항\n\n"
            "1. 네트워크를 정확히 선택하세요.\n"
            "2. 잘못 전송 시 복구 불가합니다.\n"
            "3. 결제 후 반드시 TXID를 보내주세요.\n"
            "4. 디지털 상품 특성상 환불 불가입니다."
        )

    elif data == "go_start":
        await start(update, context)


# ==============================
# 실행
# ==============================
app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button_handler))

print("✅ 봇 실행 중...")
app.run_polling()

import threading
from flask import Flask

app_web = Flask(__name__)

@app_web.route('/')
def home():
    return "Bot is running!"

def run_web():
    app_web.run(host="0.0.0.0", port=10000)

threading.Thread(target=run_web).start()
