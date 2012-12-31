pubdensity - exploring pub attributes using OpenStreetMap, XSLT and Python
==========

Simple code for analysing the distribution of pubs' attributes around the UK, as recorded in OpenStreetMap.

Note that the data is not included. This readme, and the scripts included, help you to download the data,
transform it into a simple format, and analyse the density.

Requirements
------------

* A unixy commandline (e.g. linux terminal, or mac Terminal.app)
* Python, with the modules numpy scipy and matplotlib. I used Python 2.7.
* Commandline tools:
   * xsltproc
   * curl

How to run
----------

Run these things from a commandline:

1. Make the folders where our data and output will go:

         mkdir data
         mkdir output

2. Download the XML data from OpenStreetMap (you can change the bounding box if you like):

         curl -g "http://www.overpass-api.de/api/xapi?*[amenity=pub][bbox=-8.61328,50.48547,1.71387,58.7682]" > data/overpass_allpubs.xml

3. Transform the XML into CSV:

         xsltproc osm_pub_csv.xslt data/overpass_allpubs.xml > data/overpass_allpubs.csv

4. Run the python density-estimation-and-plotting script:

         python pubdensity.py

Copyright
---------
(c) Dan Stowell 2012

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

