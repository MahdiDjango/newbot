# Create a new config.py file in same dir and import, then extend this class.
from tg_bot.sample_config import Config


class Development(Config):
    OWNER_ID = 727451676  # my telegram ID
    OWNER_USERNAME = "@RosenBlack"  # my telegram username
    # my api key, as provided by the botfather
    #API_KEY = "2036745331:AAHHLNM3sTp2kevEaD4TLMOwkwkUYTqz83A"
    #SQLALCHEMY_DATABASE_URI = 'postgresql://djghjcfyuthroj:186c684af62049d99c9f50a99487f124b8d1363686b31bbb43eff83cc992fc3f@ec2-35-174-118-71.compute-1.amazonaws.com:5432/d4oeb647ivdgbm'  # sample db credentials
    #SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:72S4oFdjxZrMKjbdT2RK@containers-us-west-16.railway.app:8038/railway'
    API_KEY = "2071942377:AAGaNx4Fi0AgJNHy2mt890f7hiZa_RL9QQo"
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:l2zo1TXnsqRTUvh7GukU@containers-us-west-20.railway.app:7809/railway'
    MESSAGE_DUMP = '-1234567890'  # some group chat that your bot is a member of
    USE_MESSAGE_DUMP = True
    # List of id's for users which have sudo access to the bot.
    SUDO_USERS = [1312603083]
    LOAD = []
    NO_LOAD = ['rss', 'sed', 'afk', 'backups', 'notes']
    # BAN_STICKER = 'CAADAgADQwEAAladvQqAw7j2H1heUhYE'
    # banhammer marie sticker
    BAN_STICKER = 'CAACAgMAAxkBAAEB7E1gOKBAMiHpzjuTJ9Xgdu9jizQ14gACygMAAr-MkASqcLD1QeTS9R4E'
    UNBAN_STICKER = 'CAACAgEAAxkBAAEB7E9gOKDelWJWMLJngUFO8OHiU0cqqgACxgUAAr-MkARS0m8_8yItoR4E'
    MUTE_STICKER = 'CAACAgMAAxkBAAEB7FNgOKEefLUtWhozkuK_K-OtEMDfHgACuAQAAr-MkAQEWcBChk9nFR4E'
    UNMUTE_STICKER = 'CAACAgMAAxkBAAEB7FdgOKFXE6jg3dweaXClvbaNQUV4dgACzAUAAr-MkAQdi6X60cRhBR4E'
    WELCOME_STICKER = 'CAACAgMAAxkBAAEB7FdgOKFXE6jg3dweaXClvbaNQUV4dgACzAUAAr-MkAQdi6X60cRhBR4E'
    GOODBYE_STICKER = 'CAACAgMAAxkBAAEB7FlgOKGineIEHWFmQiHZwH6lXgnfzwAC5wQAAr-MkARY4Gt1LYVUxR4E'
    GBAN_STICKER = 'CAACAgMAAxkBAAEB7RNgOTL7JlOi1szvblxt5HsNFbJ5WAACPAQAAr-MkARSjCITLU2U1B4E'
    UNGBAN_STICKER = 'CAACAgMAAxkBAAEB7RVgOTMc1NFBWsXlNfzC_yKmJxNYhQAC7QQAAr-MkAQ0ixdo8OOiWB4E'
    WARN_STICKER = 'CAACAgMAAxkBAAEB7bJgOhe8nOM1ci2VNsH4iUCSH9HFeQACtAQAAr-MkAT3vljza3FA0B4E'
    ALLOW_EXCL = True
