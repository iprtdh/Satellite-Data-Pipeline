from astropy.io import fits
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
from astropy.stats import sigma_clipped_stats
from photutils.detection import DAOStarFinder, find_peaks
from photutils.aperture import CircularAperture, CircularAnnulus, ApertureStats, aperture_photometry
import math as m

date = '2002-12-03'
detector = 'WFC'
filter = 'F814W'
extime = 161270.0
zeropoint = 25.954
distance_m31_pc = 778000
L_sun = 3.839e26
Mag_sun = 4.14

def stats(section):
    mean, median, std = sigma_clipped_stats(section, sigma=11.00)
    return mean, median, std

def daofind(section):
    mean, median, std = stats(section)
    return DAOStarFinder(fwhm=2.0, threshold=7.0 * std)

def sources(section):
    mean, median, std = stats(section)
    sources_ = daofind(section)((section - median))
    for col in sources_.colnames:
        if col not in ('id', 'npix'):
            sources_[col].info.format = '%.2f'
    return sources_

def positions(section):
    positions_ = np.transpose((sources(section)['xcentroid'], sources(section)['ycentroid']))
    return positions_

def apertures(section):
    return CircularAperture(positions(section), r = 10.45)

def peak_aperture(section):
    mean, median, std = stats(section)
    threshold = median + 7.0 * std
    peaks = find_peaks(section, threshold, box_size=11)
    peaks['peak_value'].info.format = '%8g'
    peak_position = np.transpose((peaks['x_peak'], peaks['y_peak']))
    return CircularAperture(peak_position, r=10.45)

def annulus_apertures(section):
    return CircularAnnulus(positions(section), r_in=20.45, r_out=30.45)

def stars_data(section):
    aperstats = ApertureStats(section, annulus_apertures(section))
    bkg_mean = aperstats.mean
    aperture_area = apertures(section).area_overlap(section)
    total_bkg = bkg_mean * aperture_area
    star_data = aperture_photometry(section, apertures(section))
    star_data['total_bkg'] = total_bkg
    for col in star_data.colnames:
        star_data[col].info.format = '%.8g'
    magnitudes = []
    for line in star_data:
        magnitudes.append(zeropoint - 2.5 * (m.log10(abs(line[3] - line[4]) / extime)))
    star_data['magnitude'] = magnitudes
    return star_data