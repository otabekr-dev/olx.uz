import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext

BACKEND_LOGIN_URL = "http://127.0.0.1:8000/auth/bot-login/"
BACKEND_REFRESH_URL = "http://127.0.0.1:8000/auth/refresh/"


user_temp_data = {}
user_tokens = {}

def start(update: Update, context: CallbackContext):
    user = update.effective_user

    update.message.reply_text(
        f"Salom {user.first_name}! 👋\n"
        "Rasm yuboring yoki /skip qiling."
    )

def handle_photo(update: Update, context: CallbackContext):
    user = update.effective_user
    photo_file = update.message.photo[-1].get_file()
    photo_url = photo_file.file_path

    payload = {
        "telegram_id": user.id,
        "first_name": user.first_name,
        "last_name": user.last_name or "",
        "username": user.username or "",
        "photo_url": photo_url
    }

    login_and_send_tokens(update, payload)

def handle_skip(update: Update, context: CallbackContext):
    user = update.effective_user
    payload = {
        "telegram_id": user.id,
        "first_name": user.first_name,
        "last_name": user.last_name or "",
        "username": user.username or "",
        "photo_url": None
    }
    login_and_send_tokens(update, payload)

def login_and_send_tokens(update: Update, payload):
    try:
        response = requests.post(BACKEND_LOGIN_URL, json=payload)
        response.raise_for_status()
    except Exception as e:
        update.message.reply_text(f"Backend xatolik: {e}")
        return

    data = response.json()
    access = data.get("access")
    refresh = data.get("refresh")

    
    user_tokens[update.effective_user.id] = {"access": access, "refresh": refresh}

    
    keyboard = [
        [InlineKeyboardButton("Refresh Token", callback_data="refresh_token")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text(
        f"Login muvaffaqiyatli!\nAccess token:\n{access}\n\nRefresh token:\n{refresh}",
        reply_markup=reply_markup
    )



def button_handler(update: Update, context: CallbackContext):
    
    query = update.callback_query
    user_id = query.from_user.id

    if query.data == "refresh_token":
        tokens = user_tokens.get(user_id)
        if not tokens:
            query.answer("Avval login qilishingiz kerak!")
            return

        payload = {"refresh": tokens["refresh"]}
        try:
            response = requests.post(BACKEND_REFRESH_URL, json=payload)
            response.raise_for_status()
        except Exception :
            query.edit_message_text(f"Token yangilanmadi")
            return

        new_access = response.json().get("access")
        
        user_tokens[user_id]["access"] = new_access

        query.edit_message_text(f"Yangi Access token:\n{new_access}")