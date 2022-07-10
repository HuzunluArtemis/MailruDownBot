# https://huzunluartemis.github.io/MailruDownBot/

import os
from pyrogram import Client, filters
from pyrogram.types.messages_and_media.message import Message
from helper_funcs.auth_user_check import AuthUserCheck
from helper_funcs.force_sub import ForceSub

@Client.on_message(filters.command("save"))
def save_thumb(client:Client, message:Message):
    if not AuthUserCheck(message): return
    if ForceSub(client, message) == 400: return
    thumbnail_location = "thumbnails"
    if not os.path.isdir(thumbnail_location): os.mkdir(thumbnail_location)
    thumb_image_path = os.path.join(thumbnail_location, str(message.from_user.id) + ".jpg")
    if message.reply_to_message is not None:
        try:
            client.download_media( message=message.reply_to_message, file_name=thumb_image_path)
            message.reply_text(f"✅\n\n🇬🇧 Custom thumbnail saved.\nThis image will be used in the upload." + \
                f" Clear: /clear"+ \
                f"\n\n🇹🇷 Özel küçük resim kaydedildi.\nBu resim, yükleme işlemlerinde kullanılacak." + \
                f" Temizle: /clear")
        except:
            message.reply_text("❌\n\n🇬🇧 Reply to a photo with this command to save custom thumbnail\n" + \
                "🇹🇷 Özel küçük resmi kaydetmek için bir fotoğrafı bununla yanıtlayın")
    else:
        message.reply_text("❌\n\n🇬🇧 Reply to a photo with this command to save custom thumbnail\n" + \
            "🇹🇷 Özel küçük resmi kaydetmek için bir fotoğrafı bununla yanıtlayın")

@Client.on_message(filters.command("clear"))
def clear_thumb(client:Client, message:Message):
    if not AuthUserCheck(message): return
    if ForceSub(client, message) == 400: return
    thumbnail_location = "thumbnails"
    thumb_image_path = os.path.join(thumbnail_location, str(message.from_user.id) + ".jpg")
    if os.path.exists(thumb_image_path):
        os.remove(thumb_image_path)
        message.reply_text("✅\n\n🇬🇧 Custom thumbnail cleared successfully.\n🇹🇷 Özel küçük resim başarıyla temizlendi.")
    else:
        message.reply_text("❌\n\n🇬🇧 Nothing to clear\n🇹🇷 Temizlenecek bir şey yok. Sensin pis")

@Client.on_message(filters.command("show"))
def show_thumb(client:Client, message:Message):
    if not AuthUserCheck(message): return
    if ForceSub(client, message) == 400: return
    thumbnail_location = "thumbnails"
    thumb_image_path = os.path.join(thumbnail_location, str(message.from_user.id) + ".jpg")
    if os.path.exists(thumb_image_path):
        message.reply_photo(thumb_image_path,
        caption = "🇬🇧 Here is your curent thumbnail.\n🇹🇷 Bu senin küçük şeyin... resmin",
        )
    else:
        message.reply_text(f"🇬🇧 You have not set a thumbnail. Reply your photo with /save\n" + \
        f"🇹🇷 Küçük resim ayarlamamışsın ki? bir fotoğrafı /save diye yanıtla")
