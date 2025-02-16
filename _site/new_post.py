import datetime;
import os;
import sys;
import yaml;
from yaml import SafeLoader

def getPossibleClasses():
    categories = []
    with open("./_data/navi.yml", 'r') as stream:
        try:
            navis = yaml.load(stream=stream, Loader=SafeLoader)
            for navi in navis:
                if navi['categories'] != "all":
                    categories.append(navi['categories'])
            return categories
        except yaml.YAMLError as exc:
            print("error")
            ##print(exc)

'''parse arguments'''
argn = len(sys.argv);
title = sys.argv[1];
category = sys.argv[2];


'''Calculate time diff and current time.'''
now = datetime.datetime.now();
utcnow = datetime.datetime.utcnow();
date_for_title = now.strftime("%Y-%m-%d");
time_zone_diff = int(round((now - utcnow).total_seconds()/3600));
sign = "+"
if time_zone_diff < 0:
    sign = "-"
if abs(time_zone_diff) < 10:
    time_zone_diff = sign + "0" + str(abs(time_zone_diff)) + ":00";
else:
    time_zone_diff = sign + str(abs(time_zone_diff)) + ":00";
datetime_for_md = str(utcnow.strftime("%Y-%m-%dT%H:%M:%S")) + str(time_zone_diff);


'''check if category is valid'''
categories = getPossibleClasses()
if category not in categories:
    print(category + " is not a valid category");
    print("Valid categories:");
    print(categories);
    sys.exit(0);

'''generate front_matter'''
front_matter = """---
layout: default
title: """ + title + """
modified: null
categories: """ + category + """
excerpt: null
tags: []
date: """ + datetime_for_md + """
---
"""

'''Try write to file'''
filename = "_posts/" + str(date_for_title) + "-" + title.replace(" ", "-").lower() + ".md";

if os.path.isfile(filename):
    print("File: " + filename + "already exists");
    sys.exit(0);
else:
    markdown_flie = open(filename, "w");
    markdown_flie.write(front_matter);
    markdown_flie.close();
    print(filename + " created with following front matter:");
    print(front_matter);
