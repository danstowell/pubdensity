#!/usr/bin/env python
# (c) Dan Stowell 2012
# See readme for usage etc.

import csv
from scipy import stats, mgrid, c_, reshape, rot90
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from colorsys import hsv_to_rgb

###########################
# user settings:
csvpath = "data/overpass_allpubs.csv"
fastdevmode = False


# load CSV
pubs = []
rdr = csv.DictReader(file(csvpath), delimiter="\t")
for row in rdr:
	row['lat'] = float(row['lat'])
	row['lon'] = float(row['lon'])
	pubs.append(row)

if fastdevmode:
	pubs = pubs[::10] # hack for fast render

lats = [datum['lat'] for datum in pubs]
lons = [datum['lon'] for datum in pubs]
latmin = min(lats)
latmax = max(lats)
lonmin = min(lons)
lonmax = max(lons)
extent=[lonmin, lonmax, latmin, latmax]

# we'll also put a few markers down for orientation purposes
placemarkers = [
	(51.4896, -0.0879, 'London'),
	(53.349307, -6.261177, 'Dublin'),
	(55.948339, -3.193272, 'Edinburgh'),
	(51.483529, -3.183686, 'Cardiff'),
	(53.44247, -2.233658, 'Manchester'),
	(54.596945, -5.930158, 'Belfast'),
	]

# fit kernel density to all data - and plot it
X, Y = mgrid[lonmin:lonmax:100j, latmin:latmax:100j]
positions = c_[X.ravel(), Y.ravel()]

values = c_[lons, lats]
kernel = stats.kde.gaussian_kde(values.T)
Z = reshape(kernel(positions.T).T, X.T.shape)

def plotmapheat(heat, title, outpath, plotdots=False):
	plt.figure(figsize=(4,5))
	plt.imshow(rot90(heat),
		    cmap=cm.gist_earth_r,
		    extent=extent,
		    aspect='auto')
	dpi = 150
	if plotdots:
		plt.plot(lons, lats, ',', markersize=0.2, color=(0,0,0,0.3))
		dpi = 300
	plt.title(title, fontsize=10)
	# city markers:
	plt.plot([pm[1] for pm in placemarkers], [pm[0] for pm in placemarkers], '.', markersize=2, color=(1,1,1,0.3))
	for pm in placemarkers:
		plt.text(pm[1], pm[0], pm[2], {'fontsize':4}, color=(0.95,0.95,0.75,0.3))
	plt.savefig(outpath, papertype='A4', format='png', dpi=dpi)

plotmapheat(Z, "UK/Eire pub density", "output/pubdensity.png", True)

# filters for getting the specific subtypes out
def filter_realale(datum):
	return datum['real_ale'] not in ['no', '']
def filter_wifi(datum):
	return datum['wifi'] in ['yes', 'free', 'customers']
def filter_toilets(datum):
	return datum['toilets'] not in ['no', '']
def filter_food(datum):
	return datum['food'] not in ['no', '']
def filter_the(datum):
	return datum['name'][:4].lower() == 'the ' \
	    or datum['name'][:3].lower() == 'ye ' \
	    or datum['name'][:2].lower() == 'y ' \
	    or datum['name'][:3].lower() == 'yr '
def filter_yeold(datum):
	return datum['name'][:6].lower() == 'ye old'
def filter_southern(datum):
	return datum['lat'] < 54

if fastdevmode:
	pubfilters = {'realale': filter_realale, 'southern': filter_southern}
else:
	pubfilters = {'realale': filter_realale, 'wifi': filter_wifi, 'toilets': filter_toilets, 'food': filter_food, 'the': filter_the, 'yeold': filter_yeold, 'southern': filter_southern}

min_main = np.min(Z)
max_main = np.max(Z)
mean_main = np.mean(Z)

def colormap2d(origval, subsetval, mean_rescaler):
	"Given a sampled density from the overall density and the resampled one, calcs a colour using 'value' for orig density and 'sat' for ratio"
	# 'value' is the density, simply mapped to 0--1
	density_rescaled = (origval - min_main) / (max_main - min_main)
	if density_rescaled < 0.005:
		density_rescaled = 0.0
	density_rescaled = (density_rescaled ** 0.25) # and warped a bit
	# the ratio is used to determine the 'hue' (just from polarity) and also the saturation
	rangescale = 1.0  # 0.1, but 10.1 gives nice clear margins
	if (origval == 0.0) or (subsetval == 0.0):
		ratio = 0.0
	else:
		ratio = np.log(mean_rescaler * subsetval / origval) * rangescale
	if ratio < 0.0:
		hue = 0
	else:
		hue = 0.5
	saturation = min(abs(ratio), 1.0)

	return hsv_to_rgb(hue, saturation, density_rescaled)

# now to work with specific reduced subsets
for label, pubfilter in pubfilters.items():
	pubs_subset = filter(pubfilter, pubs)
	lats_subset = [datum['lat'] for datum in pubs_subset]
	lons_subset = [datum['lon'] for datum in pubs_subset]

	values_subset = c_[lons_subset, lats_subset]
	kernel_subset = stats.kde.gaussian_kde(values_subset.T)
	#kernel_subset.covariance_factor = kernel.factor  # re-using the bandwidth factor from the first KDE, doesn't seem to help much though
	Z_subset = reshape(kernel_subset(positions.T).T, X.T.shape)

	min_subset = np.min(Z_subset)
	max_subset = np.max(Z_subset)
	mean_subset = np.mean(Z_subset)

	mean_rescaler = mean_main / mean_subset

	rgb = [[colormap2d(Z[indexA, indexB], subsetval, mean_rescaler) for indexB, subsetval in enumerate(row)] for indexA, row in enumerate(Z_subset)]

	plotmapheat(Z_subset, "Density: %s" % label, "output/pubdensity_%s.png" % label) #, True)
	plotmapheat(rgb, "Relative density: %s" % label, "output/pubdensityratio_%s.png" % label)

