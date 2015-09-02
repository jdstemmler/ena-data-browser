# coding: utf-8

import matplotlib
matplotlib.use('Agg')
matplotlib.rcParams['figure.subplot.left'] = 0.1
matplotlib.rcParams['figure.subplot.right'] = 0.9
matplotlib.rcParams['figure.subplot.top'] = 0.95
matplotlib.rcParams['figure.subplot.bottom'] = 0.075

import matplotlib.pyplot as plt
import matplotlib.cm as cm
from mpl_toolkits.basemap import Basemap

import toolbox as tbx
import datetime
import numpy as np
import pandas as pd
import glob
import os

from PIL import Image
import urllib, cStringIO

#import seaborn as sns
#colors = sns.color_palette()

# set the base directory
base_directory = os.path.abspath('/Volumes/data/ENA/')
if not os.path.isdir(base_directory):
	base_directory = os.path.abspath('/Volumes/NiftyDrive/Research/data/ENA/')

plot_directory = os.path.join(os.getenv("HOME"),
					'Documents/htdocs/ena_data_browser/support-files/figures')
support_directory = os.path.join(os.getenv("HOME"),
					'Documents/htdocs/ena_data_browser/support-files')

# set the start date
start_date = datetime.date(2013, 10, 1)
today = datetime.datetime.now().date()

# Surface Meteorology
sfcmet = tbx.fileIO.NetCDFFolder(os.path.join(base_directory, 'met'))
sfcpat = 'enametC1.??.%Y%m%d.??????.*'
sfcvars = ['wspd_vec_mean', 'wdir_vec_mean', 'org_precip_rate_mean']
sfcmet.summary()

# CCN
ccndat = tbx.fileIO.NetCDFFolder(os.path.join(base_directory, 'ccn'))
ccnpat = 'enaaosccn100C1.??.%Y%m%d.??????.*'
ccnvars = ['N_CCN', 'ss', 'supersat']
ccnmap = {'N_CCN': 'CCN',
          'CCN_supersaturation_set_point': 'SS',
          'CCN_ss_set': 'SS'}
ccndat.summary()

# UHSAS
uhsas = tbx.fileIO.NetCDFFolder(os.path.join(base_directory, 'uhsas/aos'))
uhsaspat = 'enaaosuhsasC1.a1.%Y%m%d.??????.*'
uhsas.summary()

cndat = tbx.fileIO.NetCDFFolder(os.path.join(base_directory, 'cn'))
cnpat = 'enaaoscpcfC1.a1.%Y%m%d.??????.*'
cnvars = ['concentration',]
cndat.summary()

iter_date = start_date

while iter_date <= today:
	sfcfile = iter_date.strftime(sfcpat)
	ccnfile = iter_date.strftime(ccnpat)
	uhsasfile = iter_date.strftime(uhsaspat)
	cnfile = iter_date.strftime(cnpat)

	sfc_matched = glob.glob(os.path.join(sfcmet.abspath, sfcfile))
	ccn_matched = glob.glob(os.path.join(ccndat.abspath, ccnfile))
	uhsas_matched = glob.glob(os.path.join(uhsas.abspath, uhsasfile))
	cn_matched = glob.glob(os.path.join(cndat.abspath, cnfile))


	if (len(sfc_matched) > 0) & (len(ccn_matched) > 0):
		print(iter_date)
		sfcframes = [tbx.fileIO.NetCDFFile(f)
					 .get_vars(varlist=sfcvars, exclude='qc')
					 .astype(np.float)
					 for f in sfc_matched]
		SFCDAT = pd.concat(sfcframes)

		ccnframes = [tbx.fileIO.NetCDFFile(f)
					 .get_vars(varlist=ccnvars, exclude='qc', mapping=ccnmap)
					 for f in ccn_matched]
		CCNDAT = pd.concat(ccnframes)

		if len(cn_matched > 0):
			cnframes = [tbx.fileIO.NetCDFFile(f)
						.get_vars(varlist=cnvars), exclude='qc'
						for f in cn_matched]
			CNDAT = pd.concat(cnframes)
		else:
			CNDAT = None

		if not np.isfinite(CNDAT).any():
			CNDAT = None
		elif (CNDAT == 0).all():
			CNDAT = None

		if len(uhsas_matched) > 0:
			UHSAS = tbx.fileIO.UHSAS(uhsas_matched[0])
		else:
			UHSAS = None

		CCN01 = CCNDAT[CCNDAT.SS == 0.2]['CCN'].resample('1Min', how='mean').astype(np.float)
		CCN05 = CCNDAT[CCNDAT.SS == 0.8]['CCN'].resample('1Min', how='mean').astype(np.float)

		CCN01.name = "CCN01"
		CCN05.name = "CCN05"

		DATA = SFCDAT.join([CCN01, CCN05])
		DATA.fillna(np.float('nan'), inplace=True)

		ycoords = (-0.06, 0.5)

		if UHSAS is not None:
			fig = plt.figure(figsize=(10, 15))
			n = 6

			ax = plt.subplot2grid((n, 1), (0,0), rowspan=2)

			image = ax.pcolormesh(UHSAS.datetimes,
				  np.array(UHSAS.lower_size_limit.tolist()+
				  		  [UHSAS.upper_size_limit[-1]]),
						  UHSAS.size_distribution.T,
						  vmin=0,
						  vmax=np.nanpercentile(UHSAS.size_distribution, 99),
						  cmap=cm.gist_earth)
			ax.set_title(iter_date.strftime('%A %B %d %Y'))
			ax.set_ylim(bottom=UHSAS.lower_size_limit[0])
			ax.set_yticks([UHSAS.lower_size_limit[0]] +
						   ax.get_yticks()[1:].tolist())
			ax.grid('on')
			ax.set_xticklabels('')
			ax.set_ylabel('Size Bin\n(nm)')
			ax.get_yaxis().set_label_coords(*ycoords)
			p = ax.get_position()

			rect = p.corners()[2].tolist() + [.02] + [p.height]
			rect[0] = rect[0] + .01
			cax = fig.add_axes(rect)
			clb = fig.colorbar(image, cax=cax)
			clb.set_label('Count')

			l = 2

			ax = plt.subplot2grid((n, 1), (l,0))
			ax.plot(UHSAS.datetimes, UHSAS.total_concentration, 'k')
			ax.set_ylabel("Total Aerosol\n(cm$^{-3}$)")
			ax.get_yaxis().set_label_coords(*ycoords)
			ax.grid('on')
			ax.set_xticklabels('')
			l+=1
			ax = plt.subplot2grid((n, 1), (l,0))

		elif UHSAS is None:
			fig = plt.figure(figsize=(10, 12))
			n=3
			l=0
			ax = plt.subplot2grid((n, 1), (l,0))
			ax.set_title(iter_date.strftime('%A %B %d %Y'))

		ax.plot(DATA.index, DATA.CCN01, '.', color='navy', label="0.1% SS")
		ax.plot(DATA.index, DATA.CCN05, '.', color='seagreen', label="0.8% SS")
		ax.set_ylabel("CCN\n(cm$^{-3}$)")
		ax.get_yaxis().set_label_coords(*ycoords)
		ll = ax.legend(loc='lower right', bbox_to_anchor=[1, 1],
				  numpoints=2, fontsize=8, ncol=2)
		ax.grid('on')
		ax.set_xticklabels('')

		if CNDAT is not None:
			bx = ax.twinx()
			CNPLOT = CNDAT.resample('5Min', how='mean')
			cnplt = bx.plot(CNPLOT.index, CNPLOT.concentration, '-', color='#8A2908', zorder=-10, label='CN 5-minute Mean')
			bx.get_yaxis().set_label_coords(1.08, 0.5)
			#bx.set_ylim(top=np.percentile(CNPLOT.concentration, 99.))
			bx.set_ylabel('CN Concentration\n(cm$^{-3}$)')
			bx.set_yscale('log')
			ll = bx.legend(loc='lower right', bbox_to_anchor=[1, 1],
			               numpoints=2, fontsize=8, ncol=2)

		l+=1

		ax = plt.subplot2grid((n, 1), (l,0))
		ax.plot(DATA.index, DATA.org_precip_rate_mean, '.', color='firebrick')
		ax.set_ylabel("Mean Precip Rate\n(mm hr$^{-1}$)")
		ax.get_yaxis().set_label_coords(*ycoords)
		ax.grid('on')
		ax.set_xticklabels('')
		l+=1

		ax = plt.subplot2grid((n, 1), (l, 0))
		sc = ax.scatter(DATA.index, DATA.wspd_vec_mean,
				   c=DATA.wdir_vec_mean, cmap=cm.hsv,
				   edgecolor='none',
				   s=10,
				   vmin=0, vmax=360)
		ax.set_ylabel('Wind Speed\n(m s$^{-1}$)')
		ax.get_yaxis().set_label_coords(*ycoords)
		ax.grid('on')
		ax.set_xlim(DATA.index[0], DATA.index[-1])
		ax.set_ylim(bottom=0)
		p = ax.get_position()

		rect = p.corners()[2].tolist() + [.02] + [p.height]
		rect[0] = rect[0] + .01
		cax = fig.add_axes(rect)
		clb = fig.colorbar(sc, cax=cax)
		clb.set_label('Wind Directon (deg)')

		l+=1

		# ax.set_xlabel(iter_date.strftime('%A %B %d %Y'))

		figout = os.path.join(plot_directory, 'main/')
		if not os.path.isdir(figout):
			os.makedirs(figout)

		fig.savefig(os.path.join(figout, iter_date.strftime('%Y-%m-%d')+'.png'),
		            transparent=False)

		fig, ax = tbx.plotting.windrose(direction=DATA['wdir_vec_mean'],
								speed=DATA['wspd_vec_mean'],
								#bins=[0, 4, 6, 7, 8])
								#colors=sns.color_palette("hls", 6)
								)

		figout = os.path.join(plot_directory, 'rose/')
		if not os.path.isdir(figout):
			os.makedirs(figout)

		fig.savefig(os.path.join(figout, iter_date.strftime('%Y-%m-%d')+'.png'))

		imgsrc = 'http://lance-modis.eosdis.nasa.gov/imagery/subsets/?subset=ARM_Azores.' \
            + iter_date.strftime('%Y%j') \
            + '.aqua.2km.jpg'

		#ENA - Graciosa Island, Azores
		#39° 5' 29.68" N, 28° 1' 32.34" W
		#Altitude: 30.48 meters

		#from shapelib import ShapeFile

		file = cStringIO.StringIO(urllib.urlopen(imgsrc).read())
		try:
			img = Image.open(file)
		except IOError:
			img = None

		#print(imgsrc)
		fig, ax = plt.subplots(figsize=(12,12))
		ax.set_title(iter_date.strftime('%A %B %d %Y'), y=1.05)
		m = Basemap(llcrnrlat=28.9951, llcrnrlon=-38.0039,
					urcrnrlat=48.9990, urcrnrlon=-18.000,
					resolution='c', ax=ax, area_thresh=0.1)

		#m.drawcoastlines()
		m.drawparallels(np.arange(-90, 90, 5), labels=[1,1,1,1])
		m.drawmeridians(np.arange(-180, 180, 5), labels=[1,1,1,1])
		if img is not None:
			m.imshow(img, origin='upper')

		m.plot(-28.02565, 39.091578, 'r*', markersize=20, latlon=True)

		m.readshapefile(os.path.join(support_directory, 'PRT_adm/PRT_adm0'),
									 'prt', drawbounds=True)

		if img is not None:
			img.close()
		figout = os.path.join(plot_directory, 'satellite/')
		if not os.path.isdir(figout):
			os.makedirs(figout)

		fig.savefig(os.path.join(figout, iter_date.strftime('%Y-%m-%d')+'.png'),
				    transparent=False)

		plt.close('all')
		#break

	iter_date = iter_date + datetime.timedelta(days=1)