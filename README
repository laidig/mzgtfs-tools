# mzgtfs-tools
Python scripts for modifying GTFS data using the mapzen-gtfs lib. 

## Why use this?

These tools complement the [GTFS Transformer](http://developer.onebusaway.org/modules/onebusaway-gtfs-modules/1.3.3/onebusaway-gtfs-transformer-cli.html), but instead of using the OneBusAway library, it uses the mapzen-gtfs library.
Some things that mapzen-gtfs/Python does over OneBusAway-gtfs/Java:
1. Faster development cycles by not having to recompile
2. Allows inserting new column names without changing the underlying library (e.g. feed_id)

## Included Tools:

| Tool | Purpose |
| add_accessible.py | add accessible stops based upon a JSON array |
| add_fares.py | add fares to a GTFS by route ID or regex pattern of route ids | 
| add_feed_id.py | add a feed_id (for OpenTripPlanner) |
| headsign_fixer.py | replace the headsign of trips for all instances of a shape_id | 
| make_all_accessible.py | make trips and routes accessible by default | 
| prepend_agency_id.py | Prepend agency_id to stops/routes/trips (e.g. agency_1) | 
| route_splitter.py | Split one route into multiple routes |
| transfer_humanizer.py | Build a human readable transfer file | 

## Requirements:
 1. Python 2.7 (mzgtfs does not support Python 3) or Pypy 2.x

## Installation:
These tools are available via as a Python package in [pip](https://pypi.python.org/pypi/mzgtfs-tools). Some depend on a fork of mapzen-gtfs and not the original, to install it:

    pip install https://github.com/BusTechnology/mapzen-gtfs/zipball/master

    pip install mzgtfs-tools
