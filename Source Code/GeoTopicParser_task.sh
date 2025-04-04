# Warning: takes 3 hours to run through the whole dataset
# set up lucene-geo-gazetteer and connect to tika
#! /bin/bash
# start lucene server
lucene-geo-gazetter -server

# open new terminal tab and run python file
python3 ./get-geotopic.py
