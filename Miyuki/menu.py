from Miyuki import bot as app
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton,InlineKeyboardMarkup
from Miyuki.utils.lang import *


keyboard = InlineKeyboardMarkup(
        [
        [
            InlineKeyboardButton(
                text="English🇬🇧", callback_data="languages_en"
            ),
            InlineKeyboardButton(
                text="සිංහල🇱🇰", callback_data="languages_si"
            )
        ],
        [
            InlineKeyboardButton(
                text="हिन्दी🇮🇳", callback_data="languages_hi"
            ),
            InlineKeyboardButton(
                text="Italiano🇮🇹", callback_data="languages_it"
            )
        ],
        [
            InlineKeyboardButton(
                text="👨‍💻Dᴇᴠᴇʟᴏᴘᴇʀ",
                url=f"https://t.me/Splash_Pro",
            )
        ],
        [
            InlineKeyboardButton("« Back", callback_data='startcq')
        ]
    ]
)

fbuttons =InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton(
                text="👥Support Group", url="https://t.me/acobot_Team"
            ),
            InlineKeyboardButton(
                text="✨News Channel", url="https://t.me/ACOBotsUpdates"
            )
        ], 
        [
            InlineKeyboardButton(
                text="⚙️Github", url="https://github.com/Splashpro/MiyukiX"
            ),
            InlineKeyboardButton(
                text="👨‍💻Dᴇᴠᴇʟᴏᴘᴇʀ", url="https://t.me/Splash_Pro"
            )
        ], 
        [
            InlineKeyboardButton("« Back", callback_data='startcq')
        ]
        ]
)

@app.on_callback_query(filters.regex("_langs"))
@languageCB
async def commands_callbacc(client, CallbackQuery, _):
    user = CallbackQuery.message.from_user.mention
    await app.send_message(
        CallbackQuery.message.chat.id,
        text= _["setting_1"].format(user),
        reply_markup=keyboard,
        disable_web_page_preview=True,
    )
    await CallbackQuery.message.delete()
    
@app.on_callback_query(filters.regex("_about"))
@languageCB
async def commands_callbacc(client, CallbackQuery, _):
    await app.send_message(
        CallbackQuery.message.chat.id,
        text=_["menu"],
        reply_markup=fbuttons,
        disable_web_page_preview=True,
    )
    await CallbackQuery.message.delete()

