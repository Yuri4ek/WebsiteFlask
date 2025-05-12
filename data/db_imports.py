from data import db_session
from data.computer_cases import ComputerCases
from data.air_coolers import AirCoolers
from data.water_coolers import WaterCoolers
from data.memory_types import MemoryTypes
from data.motherboards import MotherBoards
from data.power_supplies import PowerSupplies
from data.processors import Processors
from data.ram_modules import RamModules
from data.sockets import Sockets
from data.HDDs import HDDs
from data.SSDs import SSDs
from data.videocards import Videocards

from data.user import User
from data.configuration import Configuration
from data.forum import Forum
from data.comment import Comment

components_types = {'computer_cases': ComputerCases,
                    'air_coolers': AirCoolers,
                    'water_coolers': WaterCoolers,
                    'memory_types': MemoryTypes,
                    'motherboards': MotherBoards,
                    'power_supplies': PowerSupplies,
                    'processors': Processors,
                    'ram_modules': RamModules,
                    'sockets': Sockets,
                    'HDDs': HDDs,
                    'SSDs': SSDs,
                    'videocards': Videocards}
