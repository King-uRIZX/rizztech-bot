import os
import json
import urllib.request
import urllib.parse

BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
VERSION = "1.0.0"
DEVELOPER = "mr.rizzx"
TIKTOK = "@mr.rizzx.cts"


def telegram(method, data):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/{method}"
    payload = urllib.parse.urlencode(data).encode()
    req = urllib.request.Request(url, data=payload, method="POST")
    with urllib.request.urlopen(req, timeout=15) as response:
        return json.loads(response.read().decode())


def keyboard():
    return {
        "inline_keyboard": [
            [
                {"text": "🛡️ Cybersecurity", "callback_data": "cyber"},
                {"text": "💻 Programming", "callback_data": "programming"}
            ],
            [
                {"text": "📚 Learning", "callback_data": "learning"},
                {"text": "📰 Tech News", "callback_data": "news"}
            ],
            [
                {"text": "🛠️ Productivity", "callback_data": "productivity"},
                {"text": "🤖 AI", "callback_data": "ai"}
            ],
            [
                {"text": "💰 Sawer / Support", "callback_data": "donate"},
                {"text": "ℹ️ About", "callback_data": "about"}
            ]
        ]
    }


def main_menu_text():
    return (
        "🚀 RizzTech Bot\n\n"
        "Bot teknologi & pembelajaran untuk semua.\n\n"
        "Pilih menu di bawah untuk mulai."
    )


def send_menu(chat_id):
    return telegram(
        "sendMessage",
        {
            "chat_id": chat_id,
            "text": main_menu_text(),
            "reply_markup": json.dumps(keyboard())
        }
    )


def callback_menu(chat_id, message_id, data):
    texts = {
        "cyber": (
            "🛡️ CYBERSECURITY\n\n"
            "Materi edukasi keamanan siber:\n"
            "• Linux & networking\n"
            "• CTF\n"
            "• OSINT dasar\n"
            "• Web security\n"
            "• Defensive security\n\n"
            "Gunakan hanya pada sistem yang kamu miliki "
            "atau yang memang memberikan izin pengujian."
        ),
        "programming": (
            "💻 PROGRAMMING\n\n"
            "Materi yang tersedia:\n"
            "• Python\n"
            "• PHP & Laravel\n"
            "• JavaScript\n"
            "• HTML & CSS\n"
            "• Git & GitHub\n"
            "• Web development"
        ),
        "learning": (
            "📚 LEARNING\n\n"
            "• Tutorial pemrograman\n"
            "• Materi teknologi\n"
            "• Quiz\n"
            "• Catatan belajar\n"
            "• Panduan project"
        ),
        "news": (
            "📰 TECH NEWS\n\n"
            "Menu berita teknologi akan dikembangkan "
            "menggunakan sumber RSS/API yang sesuai.\n\n"
            "Tidak menggunakan scraping agresif."
        ),
        "productivity": (
            "🛠️ PRODUCTIVITY\n\n"
            "Fitur yang sedang disiapkan:\n"
            "• Reminder\n"
            "• Todo list\n"
            "• Notes\n"
            "• Project tracker"
        ),
        "ai": (
            "🤖 AI TOOLS\n\n"
            "Integrasi AI menggunakan API key yang "
            "disimpan sebagai environment variable.\n\n"
            "Jangan pernah memasukkan API key ke GitHub."
        ),
        "donate": (
            "💰 SUPPORT RIZZTECH\n\n"
            "Kalau bot ini membantu kamu, kamu bisa "
            "mendukung pengembangannya melalui link "
            "donasi yang dikonfigurasi oleh admin."
        ),
        "about": (
            f"ℹ️ ABOUT\n\n"
            f"RizzTech Bot\n"
            f"Version: v{VERSION}\n"
            f"Developer: {DEVELOPER}\n"
            f"TikTok: {TIKTOK}\n\n"
            "Dibuat untuk pembelajaran teknologi."
        )
    }

    text = texts.get(data, main_menu_text())

    buttons = {
        "inline_keyboard": [
            [{"text": "⬅️ Kembali", "callback_data": "home"}]
        ]
    }

    if data == "donate":
        links = []
        for key, label in [
            ("SAWERIA_URL", "Saweria"),
            ("TRAKTEER_URL", "Trakteer"),
            ("DONATION_URL", "Donation")
        ]:
            value = os.environ.get(key, "").strip()
            if value:
                links.append([{"text": f"💸 {label}", "url": value}])

        buttons["inline_keyboard"] = links + [
            [{"text": "⬅️ Kembali", "callback_data": "home"}]
        ]

    return telegram(
        "editMessageText",
        {
            "chat_id": chat_id,
            "message_id": message_id,
            "text": text,
            "reply_markup": json.dumps(buttons)
        }
    )


def handler(request):
    if request.get("httpMethod") != "POST":
        return {
            "statusCode": 200,
            "body": "RizzTech Bot webhook is running."
        }

    try:
        update = json.loads(request.get("body") or "{}")
    except Exception:
        return {"statusCode": 400, "body": "Invalid JSON"}

    message = update.get("message")
    callback = update.get("callback_query")

    if message:
        chat = message.get("chat", {})
        chat_id = chat.get("id")
        text = message.get("text", "")

        if text.startswith("/start") or text.startswith("/menu"):
            send_menu(chat_id)

        elif text.startswith("/about"):
            telegram(
                "sendMessage",
                {
                    "chat_id": chat_id,
                    "text": (
                        f"RizzTech Bot v{VERSION}\n\n"
                        f"Developer: {DEVELOPER}\n"
                        f"TikTok: {TIKTOK}"
                    )
                }
            )

        elif text.startswith("/help"):
            telegram(
                "sendMessage",
                {
                    "chat_id": chat_id,
                    "text": (
                        "📖 COMMANDS\n\n"
                        "/start - buka menu\n"
                        "/menu - buka menu\n"
                        "/about - informasi bot\n"
                        "/help - bantuan"
                    )
                }
            )

        else:
            telegram(
                "sendMessage",
                {
                    "chat_id": chat_id,
                    "text": "Gunakan /start untuk membuka menu RizzTech Bot."
                }
            )

    if callback:
        query_id = callback.get("id")
        callback_message = callback.get("message", {})
        chat = callback_message.get("chat", {})
        chat_id = chat.get("id")
        message_id = callback_message.get("message_id")
        data = callback.get("data", "")

        telegram(
            "answerCallbackQuery",
            {"callback_query_id": query_id}
        )

        if data == "home":
            telegram(
                "editMessageText",
                {
                    "chat_id": chat_id,
                    "message_id": message_id,
                    "text": main_menu_text(),
                    "reply_markup": json.dumps(keyboard())
                }
            )
        else:
            callback_menu(chat_id, message_id, data)

    return {
        "statusCode": 200,
        "body": "OK"
    }
