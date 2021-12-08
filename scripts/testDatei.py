import sys
import os
import gpxpy
import gpxpy.gpx
 
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from colimit import Connection as _Connection, way
from GeolocationUpdate.getconfig import get_config
from GeolocationUpdate.getlimit import get_limit


filename = 'around_hda.gpx'
config = get_config()


def read_gpx_file(filename):
    gpx_file = open(config["path_to_gpx"] + filename, 'r')
    gpx = gpxpy.parse(gpx_file)
    return gpx


def main():
    connect = _Connection(username=config["user"],
                          password=config["password"],
                          url=config["url"],
                          port=config["port"])

    # pos_ways = connect.get_ways(latitude=47.644548,
    #                             longitude=-122.326897,
    #                             radius=20)
    # print(pos_ways[0].geometry[0].latitude)

    gpx = read_gpx_file(filename=filename)
    for track in gpx.tracks:
        for segment in track.segments:
            for waypoint in segment.points:
                # print(waypoint)
                # print(waypoint.latitude)
                # print(waypoint.longitude)
                lat = waypoint.latitude
                lon = waypoint.longitude
                print(get_limit(latitude=lat,
                                longitude=lon,
                                speed=0,
                                direction=0,
                                get_ways=connect.get_ways))


if __name__ == "__main__":
    main()
