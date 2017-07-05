#!/usr/bin/python

import sys, os, shutil
import mzgtfs.feed
import mzgtfs.util
import util


def trip_shape_validate(gtfs_feed, gtfs_file):
    files = ["trips.txt", "stop_times.txt"]
    try:
        len(gtfs_feed.shapes())
    except KeyError:
        print "no shapes found, exiting"
        return

    #remove empty shapes
    print "removing any trips with no shapes / invalid shapes"

    shapes = list()
    for s in gtfs_feed.shapes():
        s = str(s).strip()
        if len(s) > 0:
            shapes.append(s)

    removed_trips = list()
    vtrips = {}
    i=0
    trips = gtfs_feed.trips()
    for t in trips:
        if t.get('shape_id') in shapes:
            cls = gtfs_feed.FACTORIES['trips']
            info = cls.from_row(t)
            vtrips[i]=info
            i=i+1
        else:
            removed_trips.append(t.get('trip_id'))
            print "REMOVING trip id %s from the trips because it didn't have a shape id of %s" % (t.get('trip_id'), t.get('shape_id'))

    print "opening stop times"
    gtfs_feed.stop_times()   
 
    print "processing"

    vstops = {}
    i = 0
    if len(removed_trips) > 0:
        for s in gtfs_feed.stop_times():
           if i%100000 == 0:
               print "processed another 100000 rows, at "+str(i)
           if s.get('trip_id') in trips:
               print "removing stoptime with stop %s because of removed trip %s" % (s.get('stop_id'), s.get('trip_id'))
           else:
               cls = gtfs_feed.FACTORIES['stop_times']
               info = cls.from_row(s)
               vstops[i] = info
               i = i + 1

    print "writing out results"

    gtfs_feed.by_id['trips'] = vtrips
    gtfs_feed.write('trips.txt', gtfs_feed.trips())
    gtfs_feed.by_id['stop_times'] = vstops
    gtfs_feed.write('stop_times.txt', gtfs_feed.stop_times())
    #gtfs_feed.make_zip('output.zip', files=files, clone=gtfs_file)
    #shutil.move('output.zip', gtfs_file)
    #util.delete_temp_files(files)

def main(argv):
    if len(argv) < 2:
        print "usage: validate_trips_have_shapes.py gtfs_file"
        sys.exit(0)
    print "Warning, this script doesn't do anything anymore, left as legacy"
    #gtfs_file = argv[1]
    #gtfs_feed = mzgtfs.feed.Feed(filename=gtfs_file)
    
    # try:
    #     trip_shape_validate(gtfs_feed, gtfs_file)

    # except Exception as e:
    #     print(repr(e))


if __name__ == "__main__":
   main(sys.argv)
