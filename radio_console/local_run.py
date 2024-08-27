from utils import redefine_env

redefine_env('.local_env')

from console import *
from database import *
from env import *
from meta import *
from server import *
from tests import *
from utils import *

# MetadataParser.run()

EntryPoint.start()