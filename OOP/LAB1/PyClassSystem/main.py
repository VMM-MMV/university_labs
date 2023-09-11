from Peasant import *
from King import *

if __name__ == "__main__":
    peasant = Peasant()
    king = King()
    if peasant.burriedWhere() == king.burriedWhere():
        print("Then who cares.")