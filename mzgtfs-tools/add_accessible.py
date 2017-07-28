#!/usr/bin/python

"""
Adds wheelchair_boarding =1 for stops, with stop_ids sourced from a JSON array, like so
["stop_id1","stop_id2"]

Also adds wheelchair_accessible=1 for all trips
usage: python add_accessibility.py {gtfs_feed} {accessible_stops.json}
"""

import json
import shutil
import mzgtfs.feed
import util

def main(gtfs_file, input_json_file):
    """ load gtfs_file and instructions from JSON"""
    gtfs_feed = mzgtfs.feed.Feed(filename=gtfs_file)
    feed_stops = gtfs_feed.stops()

    with open(input_json_file) as jsonfile:
        accessible_stops = json.load(jsonfile)

    for stop in feed_stops:
        if stop.id() in accessible_stops:
            stop.set('wheelchair_boarding', '1')
    
    make_accessible_trips(gtfs_feed)

    files = ['stops.txt', 'trips.txt']

    cols = ['stop_id','stop_lat','stop_lon','stop_name','wheelchair_boarding']
    gtfs_feed.write('stops.txt', gtfs_feed.stops(), columns=cols)

    cols = ['route_id','trip_id','service_id','direction_id','trip_headsign','shape_id','wheelchair_accessible']
    gtfs_feed.write('trips.txt', gtfs_feed.trips(), columns=cols)

    gtfs_feed.make_zip('output.zip', files=files, clone=gtfs_file)
    shutil.move('output.zip', gtfs_file)

    util.delete_temp_files(files)
    

def make_accessible_trips(gtfs_feed):
    for trip in gtfs_feed.trips():
        trip.set('wheelchair_accessible', 1) 

if __name__ == "__main__":
   import plac
   plac.call(main)