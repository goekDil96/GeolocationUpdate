import sys
import os
 
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from colimit import Connection as _Connection
from GeolocationUpdate.getconfig import get_config
from GeolocationUpdate.getlimit import get_limit

config = get_config()

def main():
    connect = _Connection(username=config["user"],
                          password=config["password"],
                          url=config["url"],
                          port=config["port"])

    pos_ways = connect.get_ways(latitude=47.644548,
                                longitude=-122.326897,
                                radius=20)
    
    # print(pos_ways[0].geometry[0].latitude)

    print(get_limit(latitude=49.901350,
                    longitude=8.655388,
                    speed=0,
                    direction=0,
                    get_ways=connect.get_ways))

if __name__ == "__main__":
    main()