
import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext

BACKEND_LOGIN_URL = "http://127.0.0.1:8000/auth/bot-login/"
BACKEND_REFRESH_URL = "http://127.0.0.1:8000/auth/refresh/"

user_states = {}
user_temp_data = {}
user_refresh_tokens = {}


def start(update: Update, context: CallbackContext):
    user = update.effective_user


    keyboard = [
        [InlineKeyboardButton("Refresh Token", callback_data="refresh_token")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text(
        f'''
Welcome, {user.first_name}! ✨
Login qilish uchun /login buyrug'idan foydalaning.Tokenlarni yangilash uchun quyidagi tugmani bosing.
''',
        reply_markup=reply_markup
    )


def login(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    user_states[user_id] = 'waiting_username'
    update.message.reply_text('Iltimos, username kiriting:')

def message_handler(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    text = update.message.text
    state = user_states.get(user_id)

    if state == 'waiting_username':
        user_temp_data[user_id] = {'username': text}   
        user_states[user_id] = 'waiting_password'      
        update.message.reply_text('Password kiriting:')

    elif state == 'waiting_password':
        user_temp_data[user_id]['password'] = text

        payload = {
            'username': user_temp_data[user_id]['username'],
            'password': user_temp_data[user_id]['password'],
            "telegram_id": user_id
        }

        try:
            response = requests.post(BACKEND_LOGIN_URL, json=payload)
        except Exception as e:
            update.message.reply_text(f'Backendga ulanishda xatolik')
            return

        if response.status_code == 200:
            data = response.json()
            access = data.get('access')
            refresh = data.get('refresh')
            user_refresh_tokens[user_id] = refresh


            update.message.reply_text(f"Access token:\n{access}")


            update.message.reply_text(f"Refresh token:\n{refresh}")
        else:
            try:
                error = response.json()
            except:
                error = response.text
            update.message.reply_text(f"Login xato : {error}")

        user_states[user_id] = None
        user_temp_data[user_id] = {}


def get_user_refresh_token(user_id):

    return user_refresh_tokens.get(user_id)


def button_handler(update: Update, context: CallbackContext):
    query = update.callback_query
    user_id = query.from_user.id

    if query.data == "refresh_token":

        refresh_token = get_user_refresh_token(user_id)


        payload = {"refresh": refresh_token}
        response = requests.post(BACKEND_REFRESH_URL, json=payload)

        if response.status_code == 200:
            new_access = response.json().get("access")
            query.edit_message_text(f"Yangi Access token:\n{new_access}")
        else:
            query.edit_message_text("Token yangilanmadi, xatolik yuz berdi")