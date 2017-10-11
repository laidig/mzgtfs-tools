#!/usr/bin/python
"""
Replace trip_headsign in trips.txt with the name of the last stop
"""
import json
import shutil
import mzgtfs.feed
import util

def main(gtfs_file):
    """ load gtfs_file and replace headsign with last stop name"""
    gtfs_feed = mzgtfs.feed.Feed(filename=gtfs_file)
    gtfs_feed.preload()

    for t in gtfs_feed.trips():
        last_stop = t.stop_sequence()[-1].get('stop_id')
        new_headsign = gtfs_feed.stop(last_stop).get('stop_name')
        t.set('trip_headsign', new_headsign)

    gtfs_feed.write('trips.txt', gtfs_feed.trips())
    files = ['trips.txt']

    print "saving file"
    
    gtfs_feed.make_zip('output.zip', files=files, clone=gtfs_file)
    shutil.move('output.zip', gtfs_file)
    util.delete_temp_files(files)


if __name__ == "__main__":
   import plac
   plac.call(main)
