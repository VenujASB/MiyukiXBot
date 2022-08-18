from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, Message
from pyrogram.errors.exceptions.bad_request_400 import ChatNotModified,ChatAdminRequired,UserNotParticipant
from pyrogram.types import ChatPermissions
from Miyuki.plugins.admin import current_chat_permissions, member_permissions
from lang import get_command
from Miyuki.utils.lang import *
from Miyuki.utils.filter_groups import *
from typing import Union
from Miyuki.plugins.protection import *
from Miyuki.mongo.approvedb import Approve
from Miyuki.mongo.locksdb import *
import os
from Miyuki import *
from pyrogram.types import MessageEntity
from Miyuki import BOT_ID, app as pbot, MONGO_URL as  MONGO_DB_URI
from Miyuki.plugins.admin import list_admins
approved_users = db.approve

client = MongoClient(MONGO_DB_URI)
dbd = client["miyukixbot"]
approved_users = dbd.approve
db = dbd

lockdb = db.lockdb1

LOCK = get_command("LOCK")
LOCKS = get_command("LOCKS")
LOCKTYPES = get_command("LOCKTYPES")

data = {
    "video": "vid",
    "audio": "aud",
    "document": "doc",
    "forward": "fwd",
    "photo": "pic",
    "sticker": "stc",
    "gif": "gif",
    "games": "game",
    "album": "albm",
    "voice": "voice",
    "video_note": "vnote",
    "contact": "contact",
    "location": "gps",
    "address": "address",
    "reply": "reply",
    "message": "message",
    "comment": "cmt",
    "edit": "edt",
    "mention": "mention",
    "inline": "inline",
    "polls": "poll",
    "dice": "dice",    
    "buttons": "button",
    "media": "media",
    "email": "emal", 
    "userbot":"ubot", 
    "url":"url",
    "spoiler":"spoiler",
    "anonchannel":"anonchannel",
    "porn":"porn",
    "spam":"spam",
}
incorrect_parameters = "Incorrect Parameters, Check Locks Section In Help."
permdata = {
    "send_messages": "can_send_messages",
    "send_stickers": "can_send_stickers",
    "send_gifs": "can_send_animations",
    "send_media": "can_send_media_messages",
    "send_games": "can_send_games",
    "send_inline": "can_use_inline_bots",
    "url_prev": "can_add_web_page_previews",
    "send_polls": "can_send_polls",
    "change_info": "can_change_info",
    "invite_user": "can_invite_users",
    "pin_messages": "can_pin_messages",
}
array1= ["spam","porn","anonchannel","spoiler","url","ubot","vid", "aud","doc", "fwd","pic", "stc", "gif", "game","albm", "voice", "vnote","contact","gps", "address", "reply","message","cmt","edt","mention","inline", "poll", "dice", "button", "media", "emal",]
array2= ["spam","porn","anonchannel","spoiler","url","userbot","video", "audio","document", "forward","photo", "sticker", "gif", "games","album", "voice", "video_note","contact","location", "address", "reply","message","comment","edit","mention","inline", "polls", "dice", "buttons", "media", "email",]
array3 =["send_messages","send_stickers","send_gifs","send_media","send_games","send_inline","url_prev","send_polls","change_info","invite_user", "pin_messages","all_permissions"]
array4=["can_send_messages","can_send_stickers","can_send_animations","can_send_media_messages","can_send_games","can_use_inline_bots","can_add_web_page_previews","can_send_polls","can_invite_users","can_change_info","can_pin_messages"]
array5=["send_messages","send_stickers","send_gifs","send_media","send_games","send_inline","url_prev","send_polls","invite_user","change_info","pin_messages"]


async def tg_lock(message, permissions: list, perm: str, lock: bool):
    if lock:
        if perm not in permissions:
            await message.reply_text("Already locked.")
            return
    else:
        if perm in permissions:
            await message.reply_text("Already Unlocked.")
            return
    (permissions.remove(perm) if lock else permissions.append(perm))
    permissions = {perm: True for perm in list(set(permissions))}
    try:
        await pbot.set_chat_permissions(message.chat.id, ChatPermissions(**permissions))
    except ChatNotModified:
        await message.reply_text("To unlock this, you have to unlock 'messages' first.")
        return
    #await message.reply_text((f"Locked {perm}." if lock else f"Unlocked {perm}."))

@pbot.on_message(filters.command(LOCK) & ~filters.private)
async def locks_dfunc(_, message):
    #print("hmm fuck")
    try:
        user_id = message.from_user.id
        chat_id = message.chat.id
        if len(message.command) != 2:
            return await message.reply("Invalid lock types ")

        parameter = message.text.strip().split(None, 1)[1].lower()
        state = message.command[0].lower()

        permissions = await member_permissions(chat_id, user_id)
        if "can_restrict_members" not in permissions:
            await message.reply_text(f"{message.from_user.mention},You need to be an admin with **restrict members** permission.")
            return


        permissions = await current_chat_permissions(chat_id)
        
        if parameter in permdata:
            await tg_lock(
                message,
                permissions,
                permdata[parameter],
                True if state == "lock" else False,
            )
            await message.reply_text((f"Locked {parameter}." if state == "lock" else f"Unlocked {parameter}."))
            return        
        elif parameter == "all_permissions" and state == "lock":
            await _.set_chat_permissions(chat_id, ChatPermissions())
            await message.reply_text("Locked All Permissions.")
        elif parameter == "all_permissions" and state == "unlock":   
            for i in range (0,(len(array4))-2):
                await tg_lock(
                    message,
                    permissions,
                    array4[i],
                    True if state == "lock" else False,
                )
            await message.reply(f"All permissions unlocked")
            return
        elif parameter in data and state == "lock":
            okletsgo = lockdb.find_one({f"{data[parameter]}": message.chat.id})
            if okletsgo:
                await message.reply(f"{parameter} already locked")
              
            else:
                lockdb.insert_one({f"{data[parameter]}": message.chat.id})
                await message.reply(f"Locked {parameter}")
            return
        elif parameter in data and state == "unlock":
            okletsgo = lockdb.find_one({f"{data[parameter]}": message.chat.id})
            
            if not okletsgo:
                await message.reply(f"{parameter} already unlocked")
            
            else:
                lockdb.delete_one({f"{data[parameter]}": message.chat.id})
                await message.reply(f"Unocked {parameter}")
            return            
        elif parameter == "all" and state == "lock":
            for i in range (0,len(array1)):
                    isittrue = lockdb.find_one({f"{array1[i]}": message.chat.id})
                    if not isittrue:
                        lockdb.insert_one({f"{array1[i]}": message.chat.id})

            await message.reply_text("Locked Everything.")
            return
        elif parameter == "bots" and state == "lock":
            if await is_b_on(chat_id):
                await message.reply_text("Bots already locked.")
                return
            await b_on(chat_id)
            await message.reply_text("Locked bots.")    
        elif parameter == "url" and state == "lock":
            await b_on(chat_id)
            lol = add_chat(int(message.chat.id))
            if not lol:
                await message.reply_text("URL Block Already Activated In This Chat")
                return
            await message.reply_text("Locked Url.") 
        elif parameter == "bots" and state == "unlock":
            if await is_b_on(chat_id):
                await b_off(chat_id) 
                await message.reply_text("Unlocked bots.")  
            else:
                await message.reply_text("Bots not locked.") 
        elif parameter == "url" and state == "unlock":
            Escobar = remove_chat(int(message.chat.id))
            if not Escobar:
                await message.reply_text("URL Block Was Not Activated In This Chat")
                return
            await message.reply_text("Unlocked Url.")                    
        elif parameter == "all" and state == "unlock":
            for i in range (0,len(array1)):
                    isittrue = lockdb.find_one({f"{array1[i]}": message.chat.id})
                    if isittrue:
                        lockdb.delete_one({f"{array1[i]}": message.chat.id})
            if await is_b_on(chat_id):
                await b_off(chat_id) 
            Escobar = remove_chat(int(message.chat.id))
            if not Escobar:
                pass                
            await message.reply_text("unLocked all.")  
            return  
        else:
            await message.reply(incorrect_parameters)
            return
    except Exception as e:
        await app.send_message(
        chat_id=LOG_GROUP_ID,
        text=(f"{e}")
    )

@pbot.on_message(filters.command(LOCKS) & ~filters.private)
async def list_locks_dfunc(_, message):
    text = f"**These are the locks in this chat:**\n"
    for i in range (0,len(array1)):
            isittrue = lockdb.find_one({f"{array1[i]}": message.chat.id})
            if isittrue:
                text += f" • {array2[i]} = `Locked `\n" 
            else:
                text += f" • {array2[i]} = `None`\n" 
    await message.reply_text(text)      

@pbot.on_message(filters.command(LOCKTYPES) & ~filters.private)
async def wew(_, message):
    lol = "**Locktypes available for this chat:  ** \n"
    for i in range (0,len(array2)):
        lol += f" • {array2[i]}\n"
    lol += " • url\n • bots\n • all"
    await message.reply(lol)

@pbot.on_message(filters.incoming  & filters.audio  & ~filters.private  & ~filters.channel  & ~filters.bot)
async def audiolock(client, message):
    if lockdb.find_one({"aud": message.chat.id}):
        pass
    else:
        message.continue_propagation()
    # Go away anon admins you are allowed
    try:
        user_id = message.from_user.id
    except:
        return
    chat_id = message.chat.id
    try:
        if len(await member_permissions(message.chat.id, message.from_user.id)) > 1:
            return
    except:
        pass
    chat_id = message.chat.id
    sender = message.from_user.id
    iid = sender
    chats = approved_users.find({})
    for c in chats:
        if message.chat.id == c["id"] and iid == c["user"]:
            return         
    try:
        await message.delete()
    except:
        message.continue_propagation()
        
        # not deleting rpc error. or no logs


@pbot.on_message( filters.incoming & filters.video & ~filters.private & ~filters.channel & ~filters.bot)
async def videolock(client, message):
    if not message.chat:
      return    
    if lockdb.find_one({"vid": message.chat.id}):
        pass
    else:
        message.continue_propagation()

    try:
        user_id = message.from_user.id
    except:
        return
    chat_id = message.chat.id
    try:
        if len(await member_permissions(message.chat.id, message.from_user.id)) > 1:
            return
    except:
        pass
    chat_id = message.chat.id
    sender = message.from_user.id
    iid = sender
    chats = approved_users.find({})
    for c in chats:
        if message.chat.id == c["id"] and iid == c["user"]:
            return        
    try:
        await message.delete()
    except:
        message.continue_propagation()


@pbot.on_message(filters.incoming & filters.document & ~filters.private & ~filters.channel & ~filters.bot)
async def doclock(client, message):
    if not message.chat:
      return    
    if lockdb.find_one({"doc": message.chat.id}):
        pass
    else:
        message.continue_propagation()

    try:
        user_id = message.from_user.id
    except:
        return
    chat_id = message.chat.id
    try:
        if len(await member_permissions(message.chat.id, message.from_user.id)) > 1:
            return
    except:
        pass
    chat_id = message.chat.id
    sender = message.from_user.id
    iid = sender
    chats = approved_users.find({})
    for c in chats:
        if message.chat.id == c["id"] and iid == c["user"]:
            return         
    try:
        await message.delete()
    except:
        message.continue_propagation()
        
@pbot.on_message(filters.incoming & filters.text & ~filters.private & ~filters.channel & ~filters.bot)
async def emaeil(client, message):
    if not message.chat:
        message.continue_propagation()
    if lockdb.find_one({"email": message.chat.id}):
        pass
    else:
        message.continue_propagation()

    try:
        user_id = message.from_user.id
    except:
        return
    chat_id = message.chat.id
    try:
        if len(await member_permissions(message.chat.id, message.from_user.id)) > 1:
            return
    except:
        pass
    approved_userss = approved_users.find({})
    chat_id = message.chat.id
    sender = message.from_user.id
    iid = sender
    chats = approved_users.find({})
    for c in chats:
        if message.chat.id == c["id"] and iid == c["user"]:
            return     
    texct = message.text
 
    texct = str(texct)
    if "@gmail.com" in texct:
        try:
            await message.delete()
        except:
            message.continue_propagation()      
    if "@outlook.com" in texct:
        try:
            await message.delete()
        except:
            message.continue_propagation()  
    if "@hotmail.com" in texct:
        try:
            await message.delete()
        except:
            message.continue_propagation()  
    if "@hotmail.com" in texct:
        try:
            await message.delete()
        except:
            message.continue_propagation()    
    message.continue_propagation()
    
@pbot.on_message(filters.forwarded & ~filters.private  & ~filters.channel & ~filters.bot)
async def fwd(client, message):
    if not message.chat:
      return    
    if lockdb.find_one({"fwd": message.chat.id}):
        pass
    else:
        message.continue_propagation()

    try:
        user_id = message.from_user.id
    except:
        return
    chat_id = message.chat.id
    try:
        if len(await member_permissions(message.chat.id, message.from_user.id)) > 1:
            return
    except:
        pass
    chat_id = message.chat.id
    sender = message.from_user.id
    iid = sender
    chats = approved_users.find({})
    for c in chats:
        if message.chat.id == c["id"] and iid == c["user"]:
            return       
    try:
        await message.delete()
    except:
        message.continue_propagation()





@pbot.on_message(filters.sticker & ~filters.private & ~filters.channel & ~filters.bot)
async def slock(client, message):
    if not message.chat:
      return       
    if lockdb.find_one({"stc": message.chat.id}):
        pass
    else:
        message.continue_propagation()

    try:
        user_id = message.from_user.id
    except:
        return
    chat_id = message.chat.id
    try:
        if len(await member_permissions(message.chat.id, message.from_user.id)) > 1:
            return
    except:
        pass
    chat_id = message.chat.id
    sender = message.from_user.id
    iid = sender
    chats = approved_users.find({})
    for c in chats:
        if message.chat.id == c["id"] and iid == c["user"]:
            return         
    try:
        await message.delete()
    except:
        message.continue_propagation()


@pbot.on_message(filters.animation & ~filters.private & ~filters.channel & ~filters.bot)
async def aalock(client, message):
    if not message.chat:
      return       
    if lockdb.find_one({"gif": message.chat.id}):
        pass
    else:
        message.continue_propagation()

    try:
        user_id = message.from_user.id
    except:
        return
    chat_id = message.chat.id
    try:
        if len(await member_permissions(message.chat.id, message.from_user.id)) > 1:
            return
    except:
        pass
    chat_id = message.chat.id
    sender = message.from_user.id
    iid = sender
    chats = approved_users.find({})
    for c in chats:
        if message.chat.id == c["id"] and iid == c["user"]:
            return        
    try:
        await message.delete()
    except:
        message.continue_propagation()



@pbot.on_message(filters.game & ~filters.private & ~filters.channel & ~filters.bot)
async def aggalock(client, message):
    if not message.chat:
      return       
    if lockdb.find_one({"game": message.chat.id}):
        pass
    else:
        message.continue_propagation()

    try:
        user_id = message.from_user.id
    except:
        return
    chat_id = message.chat.id
    try:
        if len(await member_permissions(message.chat.id, message.from_user.id)) > 1:
            return
    except:
        pass
    chat_id = message.chat.id
    sender = message.from_user.id
    iid = sender
    chats = approved_users.find({})
    for c in chats:
        if message.chat.id == c["id"] and iid == c["user"]:
            return          
    try:
        await message.delete()
    except:
        message.continue_propagation()




@pbot.on_message(filters.incoming & filters.media_group & ~filters.private & ~filters.channel & ~filters.bot)
async def alggsjalock(client, message):
    if not message.chat:
      return       
    if lockdb.find_one({"albm": message.chat.id}):
        pass
    else:
        message.continue_propagation()
    #print("media group coming")
    try:
        user_id = message.from_user.id
    except:
        return
    chat_id = message.chat.id
    try:
        if len(await member_permissions(message.chat.id, message.from_user.id)) > 1:
            return
    except:
        pass
    chat_id = message.chat.id
    sender = message.from_user.id
    iid = sender
    chats = approved_users.find({})
    for c in chats:
        if message.chat.id == c["id"] and iid == c["user"]:
            return         
    try:
        await message.delete()
    except Exception as e:
        print(e)
        message.continue_propagation()       
        
         
@pbot.on_message(filters.voice & ~filters.private & ~filters.channel & ~filters.bot)
async def alggalgossck(client, message):
    if not message.chat:
      return       
    if lockdb.find_one({"voice": message.chat.id}):
        pass
    else:
        message.continue_propagation()

    try:
        user_id = message.from_user.id
    except:
        return
    chat_id = message.chat.id
    try:
        if len(await member_permissions(message.chat.id, message.from_user.id)) > 1:
            return
    except:
        pass
    chat_id = message.chat.id
    sender = message.from_user.id
    iid = sender
    chats = approved_users.find({})
    for c in chats:
        if message.chat.id == c["id"] and iid == c["user"]:
            return          
    try:
        await message.delete()
    except:
        message.continue_propagation()     
        
@pbot.on_message(filters.video_note & ~filters.private & ~filters.channel & ~filters.bot)
async def alggalock(client, message):
    if not message.chat:
      return       
    if lockdb.find_one({"vnote": message.chat.id}):
        pass
    else:
        message.continue_propagation()

    try:
        user_id = message.from_user.id
    except:
        return
    chat_id = message.chat.id
    try:
        if len(await member_permissions(message.chat.id, message.from_user.id)) > 1:
            return
    except:
        pass
    chat_id = message.chat.id
    sender = message.from_user.id
    iid = sender
    chats = approved_users.find({})
    for c in chats:
        if message.chat.id == c["id"] and iid == c["user"]:
            return        
    try:
        await message.delete()
    except:
        message.continue_propagation()                                 
        
        
@pbot.on_message(filters.contact & ~filters.private & ~filters.channel & ~filters.bot)
async def alggalololck(client, message):
    if not message.chat:
      return       
    if lockdb.find_one({"contact": message.chat.id}):
        pass
    else:
        message.continue_propagation()

    try:
        user_id = message.from_user.id
    except:
        return
    chat_id = message.chat.id
    try:
        if len(await member_permissions(message.chat.id, message.from_user.id)) > 1:
            return
    except:
        pass
    chat_id = message.chat.id
    sender = message.from_user.id
    iid = sender
    chats = approved_users.find({})
    for c in chats:
        if message.chat.id == c["id"] and iid == c["user"]:
            return     
    try:
        await message.delete()
    except:
        message.continue_propagation()             
        
@pbot.on_message(filters.location & ~filters.private & ~filters.channel & ~filters.bot)
async def alggalololck(client, message):
    if not message.chat:
      return       
    if lockdb.find_one({"gps": message.chat.id}):
        pass
    else:
        message.continue_propagation()

    try:
        user_id = message.from_user.id
    except:
        return
    chat_id = message.chat.id
    try:
        if len(await member_permissions(message.chat.id, message.from_user.id)) > 1:
            return
    except:
        pass
    chat_id = message.chat.id
    sender = message.from_user.id
    iid = sender
    chats = approved_users.find({})
    for c in chats:
        if message.chat.id == c["id"] and iid == c["user"]:
            return         
    try:
        await message.delete()
    except:
        message.continue_propagation() 
        
@pbot.on_message(filters.venue & ~filters.private & ~filters.channel & ~filters.bot)
async def alggalololck(client, message):
    if not message.chat:
      return       
    if lockdb.find_one({"address": message.chat.id}):
        pass
    else:
        message.continue_propagation()

    try:
        user_id = message.from_user.id
    except:
        return
    chat_id = message.chat.id
    try:
        if len(await member_permissions(message.chat.id, message.from_user.id)) > 1:
            return
    except:
        pass
    chat_id = message.chat.id
    sender = message.from_user.id
    iid = sender
    chats = approved_users.find({})
    for c in chats:
        if message.chat.id == c["id"] and iid == c["user"]:
            return         
    try:
        await message.delete()
    except:
        message.continue_propagation()     
        
                                                                                                                          
                                                                                                                                                                             
@pbot.on_message(filters.reply & ~filters.private & ~filters.channel & ~filters.bot)
async def reply(client, message):
    if not message.chat:
      return       
    if lockdb.find_one({"reply": message.chat.id}):
        pass
    else:
        message.continue_propagation()

    try:
        user_id = message.from_user.id
    except:
        return
    chat_id = message.chat.id
    try:
        if len(await member_permissions(message.chat.id, message.from_user.id)) > 1:
            return
    except:
        pass
    chat_id = message.chat.id
    sender = message.from_user.id
    iid = sender
    chats = approved_users.find({})
    for c in chats:
        if message.chat.id == c["id"] and iid == c["user"]:
            return       
    try:
        await message.delete()
    except:
        message.continue_propagation()                                                                                                                                    
              
@pbot.on_message(filters.text & ~filters.private & ~filters.channel & ~filters.bot)
async def messages(client, message):
    if not message.chat:
      return   
    if lockdb.find_one({"message": message.chat.id}):
        pass
    else:
        message.continue_propagation()

    try:
        user_id = message.from_user.id
    except:
        return
    chat_id = message.chat.id
    try:
        if len(await member_permissions(message.chat.id, message.from_user.id)) > 1:
            return
    except:
        pass
    approved_userss = approved_users.find({})
    chat_id = message.chat.id
    sender = message.from_user.id
    iid = sender
    chats = approved_users.find({})
    for c in chats:
        if message.chat.id == c["id"] and iid == c["user"]:
            return     
    
    
    try:
        await message.delete()
    except:
        message.continue_propagation()    
    
    
    
@pbot.on_message(filters.incoming & ~filters.private &  ~filters.channel & ~filters.bot)
async def cmt11(client, message):
    if not message.chat:
      return       
    if lockdb.find_one({"cmt": message.chat.id}):
        pass
    else:
        message.continue_propagation()

    try:
        user_id = message.from_user.id
    except:
        return
    chat_id = message.chat.id
    try:
        if len(await member_permissions(message.chat.id, message.from_user.id)) > 1:
            return
    except:
        pass
    approved_userss = approved_users.find({})
    chat_id = message.chat.id
    sender = message.from_user.id
    iid = sender
    chats = approved_users.find({})
    for c in chats:
        if message.chat.id == c["id"] and iid == c["user"]:
            return 
    try:
        await client.get_chat_member(message.chat.id, user_id)
    except UserNotParticipant:
        try:
            await message.delete()
        except:
            message.continue_propagation()

    except ChatAdminRequired:
        message.continue_propagation()

@pbot.on_message(filters.edited & ~filters.private  & ~filters.channel & ~filters.bot)
async def edt(client, message):
    if not message.chat:
      return   
    if lockdb.find_one({"edt": message.chat.id}):
        pass
    else:
        message.continue_propagation()

    try:
        user_id = message.from_user.id
    except:
        return
    chat_id = message.chat.id
    try:
        if len(await member_permissions(message.chat.id, message.from_user.id)) > 1:
            return
    except:
        pass
    approved_userss = approved_users.find({})
    chat_id = message.chat.id
    sender = message.from_user.id
    iid = sender
    chats = approved_users.find({})
    for c in chats:
        if message.chat.id == c["id"] and iid == c["user"]:
            return      
    
    
    try:
        await message.delete()
    except:
        message.continue_propagation()     


@pbot.on_message(filters.incoming  & ~filters.private & ~filters.channel & ~filters.bot)
async def mnsn(client, message):
    if not message.chat:
      return   
    if lockdb.find_one({"mention": message.chat.id}):
        pass
    else:
        message.continue_propagation()
    textl = message.text
    textl = str(textl)
    if not "@" in textl:
        return message.continue_propagation()
    try:
        user_id = message.from_user.id
    except:
        return
    chat_id = message.chat.id
    try:
        if len(await member_permissions(message.chat.id, message.from_user.id)) > 1:
            return 
    except:
        pass
    approved_userss = approved_users.find({})
    chat_id = message.chat.id
    sender = message.from_user.id
    iid = sender
    chats = approved_users.find({})
    for c in chats:
        if message.chat.id == c["id"] and iid == c["user"]:
            return 
    

    try:
        await message.delete()
    except:
        message.continue_propagation()            

@pbot.on_message(filters.via_bot & ~filters.private & ~filters.channel & ~filters.bot)
async def inln(client, message):
    if not message.chat:
      return      
    if lockdb.find_one({"inline": message.chat.id}):
        pass
    else:
        message.continue_propagation()

    try:
        user_id = message.from_user.id
    except:
        return
    chat_id = message.chat.id
    try:
        if len(await member_permissions(message.chat.id, message.from_user.id)) > 1:
            return
    except:
        pass
    approved_userss = approved_users.find({})
    chat_id = message.chat.id
    sender = message.from_user.id
    iid = sender
    chats = approved_users.find({})
    for c in chats:
        if message.chat.id == c["id"] and iid == c["user"]:
            return     
    
    
    try:
        await message.delete()
    except:
        message.continue_propagation()       

@pbot.on_message(filters.poll & ~filters.private & ~filters.channel & ~filters.bot)
async def poll(client, message):
    if not message.chat:
      return       
    if lockdb.find_one({"poll": message.chat.id}):
        pass
    else:
        message.continue_propagation()

    try:
        user_id = message.from_user.id
    except:
        return
    chat_id = message.chat.id
    try:
        if len(await member_permissions(message.chat.id, message.from_user.id)) > 1:
            return
    except:
        pass
    approved_userss = approved_users.find({})
    chat_id = message.chat.id
    sender = message.from_user.id
    iid = sender
    chats = approved_users.find({})
    for c in chats:
        if message.chat.id == c["id"] and iid == c["user"]:
            return     
    
    
    try:
        await message.delete()
    except:
        message.continue_propagation()               


@pbot.on_message(filters.incoming & filters.dice & ~filters.private & ~filters.channel & ~filters.bot)
async def diced(client, message):
    if not message.chat:
      return       
    if lockdb.find_one({"dice": message.chat.id}):
        pass
    else:
        message.continue_propagation()

    try:
        user_id = message.from_user.id
    except:
        return
    chat_id = message.chat.id
    try:
        if len(await member_permissions(message.chat.id, message.from_user.id)) > 1:
            return
    except:
        pass
    approved_userss = approved_users.find({})
    chat_id = message.chat.id
    sender = message.from_user.id
    iid = sender
    chats = approved_users.find({})
    for c in chats:
        if message.chat.id == c["id"] and iid == c["user"]:
            return       
    
    
    try:
        await message.delete()
    except:
        message.continue_propagation()             


@pbot.on_message(filters.inline_keyboard & ~filters.private & ~filters.channel & ~filters.bot)
async def button(client, message):
    if not message.chat:
      return       
    if lockdb.find_one({"button": message.chat.id}):
        pass
    else:
        message.continue_propagation()

    try:
        user_id = message.from_user.id
    except:
        return
    chat_id = message.chat.id
    try:
        if len(await member_permissions(message.chat.id, message.from_user.id)) > 1:
            return
    except:
        pass
    approved_userss = approved_users.find({})
    chat_id = message.chat.id
    sender = message.from_user.id
    iid = sender
    chats = approved_users.find({})
    for c in chats:
        if message.chat.id == c["id"] and iid == c["user"]:
            return       
    
    
    try:
        await message.delete()
    except:
        message.continue_propagation()
             
@pbot.on_message(filters.photo & ~filters.private & ~filters.channel & ~filters.bot)
async def mediwa(client, message):
    if not message.chat:
      return       
    if lockdb.find_one({"pic": message.chat.id}):
        pass
    else:
        message.continue_propagation()

    try:
        user_id = message.from_user.id
    except:
        return
    chat_id = message.chat.id
    try:
        if len(await member_permissions(message.chat.id, message.from_user.id)) > 1:
            return
    except:
        pass
    approved_userss = approved_users.find({})
    chat_id = message.chat.id
    sender = message.from_user.id
    iid = sender
    chats = approved_users.find({})
    for c in chats:
        if message.chat.id == c["id"] and iid == c["user"]:
            return       
    
    
    try:
        await message.delete()
    except:
        message.continue_propagation()     

@pbot.on_message(filters.media & ~filters.private & ~filters.channel & ~filters.bot)
async def mediwa(client, message):
    if not message.chat:
      return       
    if lockdb.find_one({"media": message.chat.id}):
        pass
    else:
        message.continue_propagation()

    try:
        user_id = message.from_user.id
    except:
        return
    chat_id = message.chat.id
    try:
        if len(await member_permissions(message.chat.id, message.from_user.id)) > 1:
            return
    except:
        pass
    approved_userss = approved_users.find({})
    chat_id = message.chat.id
    sender = message.from_user.id
    iid = sender
    chats = approved_users.find({})
    for c in chats:
        if message.chat.id == c["id"] and iid == c["user"]:
            return       
    
    
    try:
        await message.delete()
    except:
        message.continue_propagation()

#userbit
@app.on_message(
        filters.edited  
        | ~filters.linked_channel,
        group=url
)
async def ubot(client, message):
    if not message.chat:
      return   
    if lockdb.find_one({"ubot": message.chat.id}):
        pass
    else:
        message.continue_propagation()
    try:
        user_id = message.from_user.id
    except:
        return
    chat_id = message.chat.id
    try:
        if len(await member_permissions(message.chat.id, message.from_user.id)) > 1:
            return
    except:
        pass
    chat_id = message.chat.id
    sender = message.from_user.id
    iid = sender
    try:
        await message.delete()
        await message.reply_text(f"""
{sender}, Your message was deleted (s). \n ❗️ edit are not allowed here""",
            )
    except:
        message.continue_propagation()   


@app.on_message(
        filters.incoming 
        | ~filters.linked_channel,
        group=url
)
async def urls(client, message):  
    if not message.chat:
        return    
    lel = get_url(message)
    user_id = message.from_user.id if message.from_user else message.sender_chat.id
    if lel:
        if not lockdb.find_one({"url": message.chat.id}):
           return
        if user_id in await list_admins(message.chat.id):
            return  
        try:
         await message.delete()
         sender = message.from_user.mention()
         lol = await pbot.send_message(
                message.chat.id,
                f"""
{sender}, Your message was deleted as it contain a link(s). \n ❗️ Links are not allowed here""",
            )
         await asyncio.sleep(7)
         await lol.delete()   
        except:
             message.continue_propagation()
    else:
            message.continue_propagation()


@app.on_message(filters.incoming  & ~filters.linked_channel, group=channel)
async def channel(client, message):
    chat_id = message.chat.id
    if message.sender_chat:
      sender = message.sender_chat
      if message.forward_from_chat and not message.from_user : return
      if not lockdb.find_one({"anonchannel": message.chat.id}):
         return 
      if chat_id == sender.id:
        return
      await message.delete()
      ti = await message.reply_text(f"""
{sender.title}, Your message was deleted as it from channel(s). \n ❗️ channel are not allowed here""",
            )
      await asyncio.sleep(10)
      await ti.delete()
    

@app.on_message(
        ~filters.private
        | ~filters.linked_channel
        | filters.text,
        group=spoiler
)
async def spoiler(client, message):
    if not message.chat:
      return  
    user_id = message.from_user.id if message.from_user else message.sender_chat.id
    if not lockdb.find_one({"spoiler": message.chat.id}):
        return
    if user_id in await list_admins(message.chat.id):
        return
    if message.entities:     
     for entity in message.entities:
        if entity.type == "spoiler":
            try:
               await message.delete()  
               sender = message.from_user.mention()
               lol = await pbot.send_message(
                message.chat.id,
                f"""
{sender}, Your message was deleted as it contain a spoiler(s). \n ❗️ spoilers are not allowed here""",
            )
               await asyncio.sleep(10)
               await lol.delete()   
            except:
              message.continue_propagation() 


#url lock help
def get_url(message_1: Message) -> Union[str, None]:
    messages = [message_1]

    if message_1.reply_to_message:
        messages.append(message_1.reply_to_message)

    text = ""
    offset = None
    length = None

    for message in messages:
        if offset:
            break

        if message.entities:
            for entity in message.entities:
                if entity.type == "url":
                    text = message.text or message.caption
                    offset, length = entity.offset, entity.length
                    break

    if offset in (None,):
        return None

    return text[offset : offset + length]





@app.on_message(
    filters.incoming & ~filters.private,
    group=porn,
)
async def detect_nsfw(_, message):
    global dl_limit
    try:
        if not lockdb.find_one({"porn": message.chat.id}):
            return message.continue_propagration()
        if dl_limit > 8:
            return message.continue_propagration()
        chat_id = message.chat.id
        try:
            user_id = message.from_user.id
        except:
            return    
        permissions = await member_permissions(chat_id, user_id)
        if "can_change_info" in permissions:
            return
        if "can_promote_members" in permissions:
            return
        if "can_pin_messages" in permissions:
            return  
        if not message.from_user:
            return
        try:
            file_id = await get_file_id_from_message(message)
        except:
            return
        if not file_id:
            return
        dl_limit=dl_limit+1
        try:
            file = await app.download_media(file_id)
        
        except:
            dl_limit=dl_limit-1
            return
        dl_limit=dl_limit-1        
        try:
            results = await arq.nsfw_scan(file=file)
        except Exception:
            return
        if not results.ok:
            return
        results = results.result
        remove(file)
        nsfw = results.is_nsfw
        if not nsfw:
            return
        try:
            if results.porn < 0.5 and results.sexy < 0.5:
              return
        except:
            pass
        try:
            await message.delete()
        except Exception:
            return
        await message.reply_text(
            f"""
    Miyuki deleted {message.from_user.mention}'s message as it contain NSFW contaent
    _________________________
    **Nsfw Sender :** {message.from_user.mention}
    **Porn:** `{results.porn} %`
    **Adult:** `{results.sexy} %`
    **Hentai:** `{results.hentai} %`
    ________________________
    """
        )
    except:
        return message.continue_propagation()

@app.on_message(
        filters.document
        | filters.photo
        | filters.sticker
        | filters.animation
        | filters.video
        | filters.text,
        group=antispam_group
)
async def spam(client, message):
    if not message.chat:
      return 
    text = message.text or message.caption
    if not text:
        return
    resp = await arq.nlp(text)
    if not resp.ok:
        return
    result = resp.result[0]
    if not result.is_spam:
        return
    user_id = message.from_user.id        
    if user_id in await list_admins(message.chat.id):
        return   
    try:
        await message.delete()  
        sender = message.from_user.mention()
        lol = await pbot.send_message(
        message.chat.id,
                f"""
{sender}, Your message was deleted as it contain a spam(s). \n ❗️ spam are not allowed here""",
            )
        await asyncio.sleep(10)
        await lol.delete()   
    except:
        message.continue_propagation() 

#helpers

async def get_file_id_from_message(message):
    file_id = None
    if message.document:
        if int(message.document.file_size) > 3145728:
            return
        mime_type = message.document.mime_type
        if mime_type != "image/png" and mime_type != "image/jpeg":
            return
        file_id = message.document.file_id

    if message.sticker:
        if message.sticker.is_animated:
            if not message.sticker.thumbs:
                return
            file_id = message.sticker.thumbs[0].file_id
        else:
            file_id = message.sticker.file_id

    if message.photo:
        if int(message.photo.file_size) > 3145728:
            return
        file_id = message.photo.file_id

    if message.animation:
        if not message.animation.thumbs:
            return
        file_id = message.animation.thumbs[0].file_id

    if message.video:
        if not message.video.thumbs:
            return
        file_id = message.video.thumbs[0].file_id
    return file_id
  

async def admins(chat_id: int):
    return [ member.user.id
        async for member in app.iter_chat_members(
            chat_id, filter="administrators"
        )]

def get_file_unique_id(message):
    m = message
    m = m.sticker or m.video or m.document or m.animation or m.photo
    if not m:
        return
    return m.file_unique_id


























__MODULE__ = "Locks"
__HELP__ = """
**Locks**
Do stickers annoy you? or want to avoid people sharing links? or pictures? You're in the right place!
The locks module allows you to lock away some common items in the telegram world; the bot will automatically delete them!

**Admin commands:**
- /lock <item(s)>: Lock one or more items. Now, only admins can use this type!
- /unlock <item(s)>: Unlock one or more items. Everyone can use this type again!
- /locks: List currently locked items.
- /locktypes: Show the list of all lockable items.

**Examples:**
- Lock stickers with:
• `/lock sticker`
- You can lock/unlock multiple items by chaining them:
• `/lock sticker photo gif video`
"""
__helpbtns__ = (
        [[
            InlineKeyboardButton
                (
                    " Lock Types", callback_data="_ucd"
                ),            
            InlineKeyboardButton
                (
                    "Permissions Locks", callback_data="_kcd"
                ) 
        ],
        [
            InlineKeyboardButton
                (
                    "Examples", callback_data="_lcd"
                )
        ]]
)
