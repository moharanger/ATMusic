from SafoneAPI import SafoneAPI

from ATMusic.core.bot import ATBot
from ATMusic.core.dir import dirr
from ATMusic.core.git import git
from ATMusic.core.userbot import Userbot
from ATMusic.misc import dbb, heroku, sudo

from .logging import LOGGER

# Directories
dirr()

# Check Git Updates
git()

# Initialize Memory DB
dbb()

# Heroku APP
heroku()

# Load Sudo Users from DB
sudo()
api = SafoneAPI()
# Bot Client
app = ATBot()

# Assistant Client
userbot = Userbot()

from .platforms import *

YouTube = YouTubeAPI()
Carbon = CarbonAPI()
Spotify = SpotifyAPI()
Apple = AppleAPI()
Resso = RessoAPI()
SoundCloud = SoundAPI()
Telegram = TeleAPI()
HELPABLE = {}
