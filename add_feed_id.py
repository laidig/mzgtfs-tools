#!/usr/bin/python
"""Add a feed_info with feed_id to the gtfs
"""

import sys, os, shutil
import mzgtfs.feed
import mzgtfs.util


def add_feed_id(gtfs_feed, gtfs_file, feed_id = None):
    if len(gtfs_feed.agencies()) > 1:
        raise ValueError('cannot process feed with more than one agency') 

    agency_id = gtfs_feed.agencies()[0].id()
    url = gtfs_feed.agency(agency_id).get('agency_url')
    lang = gtfs_feed.agency(agency_id).get('agency_lang')
    feed_id = feed_id or agency_id

    print "adding feed_id " + feed_id +" to " + gtfs_file
        
    if lang: 
        feed_lang = lang
    else:
        feed_lang = 'en'

    if 'feed_info' not in gtfs_feed.by_id:
        gtfs_feed.by_id['feed_info'] = {}
        cls = gtfs_feed.FACTORIES['feed_info']
        info = cls.from_row({
            'feed_publisher_name' : agency_id,
            'feed_publisher_url' : url ,
            'feed_lang' : feed_lang,
            'feed_id' : feed_id
            })
        gtfs_feed.by_id['feed_info']['a'] = info



    files = ["feed_info.txt"]
    for f in files:
        if os.path.exists(f):
            os.remove(f)

    gtfs_feed.write('feed_info.txt', gtfs_feed.feed_infos())
    gtfs_feed.make_zip('output.zip', files=files, clone=gtfs_file)
    

def main(argv):
    if len(argv) < 2:
        print "usage: add_feed_id.py gtfs_file <optional replacement feed_id>"
        sys.exit(0)

    if len(argv) > 2:
        feed_id = argv[2]
    else:
        feed_id = None

    gtfs_file = argv[1]
    gtfs_feed = mzgtfs.feed.Feed(filename=gtfs_file)
    
    try:
        add_feed_id(gtfs_feed, gtfs_file, feed_id)
    except Exception as e:
        print(repr(e))

    shutil.move('output.zip', gtfs_file)
    os.remove('feed_info.txt')

if __name__ == "__main__":
   main(sys.argv)
