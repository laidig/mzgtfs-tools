#!/usr/bin/python

"""
Adds wheelchair_boarding =1 for stops, with stop_ids sourced from a JSON array, like so
["stop_id1","stop_id2"]

Also adds wheelchair_accessible=1 for all trips
usage: python add_accessibility.py {gtfs_feed} {accessible_stops.json}
"""

from collections import defaultdict
import json
import shutil
import mzgtfs.feed
import util

def main(gtfs_file, input_json_file):
    """ load gtfs_file and instructions from JSON"""
    gtfs_feed = mzgtfs.feed.Feed(filename=gtfs_file)
    feed_stops = gtfs_feed.stops()

    with open(input_json_file,'rb') as jsonfile:
        accessible_stops = json.load(jsonfile)
        accessible_stop_count = len(accessible_stops)

    added_accessible_stop_count = 0
    added_accessible_parent_count = 0 

    parent_to_child_stations = defaultdict(set)

    for stop in feed_stops:
        if stop.id() in accessible_stops:
            stop.set('wheelchair_boarding', '1')
            added_accessible_stop_count += 1
        
        parent = stop.get('parent_station')
        if (parent and parent.strip()):
            parent_to_child_stations[parent].add(stop.id())

    # if the stop is a parent station and all substations are accessible, parent station is accessible, too
    for parent, children in parent_to_child_stations.iteritems():
        child_count = len(children)
        accessible_count = 0
        for c in children:
            stop = gtfs_feed.stop(c)
            if stop.get('wheelchair_boarding') == '1':
                accessible_count += 1

        if child_count is accessible_count:
            gtfs_feed.stop(parent).set('wheelchair_boarding', '1')

    make_accessible_trips(gtfs_feed)

    files = ['stops.txt', 'trips.txt']

    # nicely ordered output columns
    cols = ['stop_id','stop_lat','stop_lon','stop_name','wheelchair_boarding']
    
    # if there are any additional columns in the source data, add them here
    all_columns = {column for s in feed_stops for column in s.keys()}
    for c in all_columns:
        if c not in cols:
            cols.append(c)


    gtfs_feed.write('stops.txt', gtfs_feed.stops(), columns=cols)

    print "added accessibility to {} stops from an input list of {}".format(added_accessible_stop_count, accessible_stop_count)
    if added_accessible_parent_count > 0:
        print "and {} parent stations made accessible".format(added_accessible_parent_count)

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