# https://huzunluartemis.github.io/MailruDownBot/

import os

class Config:
    
    BOT_TOKEN = os.environ.get('BOT_TOKEN', '')
    APP_ID = int(os.environ.get('APP_ID', 1111111))
    API_HASH = os.environ.get('API_HASH', '')
    OWNER_ID = int(os.environ.get('OWNER_ID', 0)) # give your owner id # if given 0 shell will not works
    FORCE_SUBSCRIBE_CHANNEL = os.environ.get('FORCE_SUBSCRIBE_CHANNEL','') # force subscribe channel link.
    if FORCE_SUBSCRIBE_CHANNEL == "" or FORCE_SUBSCRIBE_CHANNEL == " " or FORCE_SUBSCRIBE_CHANNEL == None: FORCE_SUBSCRIBE_CHANNEL = None # bu satıra dokunmayın.
    CHANNEL_OR_CONTACT = os.environ.get('CHANNEL_OR_CONTACT', "HuzunluArtemis") # give your public channel or contact username
    JOIN_CHANNEL_STR = os.environ.get('JOIN_CHANNEL_STR',
        "Merhaba / Hi {}\n\n" + \
        "🇬🇧 First subscribe my channel from button, try again.\n" + \
        "🇹🇷 Önce butondan kanala abone ol, tekrar dene.")
    YOU_ARE_BANNED_STR = os.environ.get('YOU_ARE_BANNED_STR',
        "🇬🇧 You are Banned to use me.\n🇹🇷 Banlanmışsın ezik.\n\nDestek / Support: {}")
    JOIN_BUTTON_STR = os.environ.get('JOIN_BUTTON_STR', "🇬🇧 Join / 🇹🇷 Katıl")
