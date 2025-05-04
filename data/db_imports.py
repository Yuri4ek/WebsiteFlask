from data import db_session
from data.computer_cases import ComputerCases
from data.cooling_systems import CoolingSystems
from data.memory_types import MemoryTypes
from data.motherboards import MotherBoards
from data.power_supplies import PowerSupplies
from data.processors import Processors
from data.ram_modules import RamModules
from data.sockets import Sockets
from data.HDDs import HDDs
from data.SSDs import SSDs
from data.videocards import Videocards

components_types = {'computer_cases': ComputerCases,
                    'cooling_systems': CoolingSystems,
                    'memory_types': MemoryTypes,
                    'motherboards': MotherBoards,
                    'power_supplies': PowerSupplies,
                    'processors': Processors,
                    'ram_modules': RamModules,
                    'sockets': Sockets,
                    'HHDs': HDDs,
                    'SSDs': SSDs,
                    'videocards': Videocards}
