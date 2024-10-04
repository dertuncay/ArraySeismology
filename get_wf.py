from obspy import read,UTCDateTime,read_events
from obspy.clients.fdsn.client import Client
from obspy.clients.fdsn import RoutingClient
from obspy.taup import TauPyModel
from obspy.geodetics import locations2degrees
from tqdm import tqdm
import pandas as pd
import numpy as np
import os
# Earth Model
model = TauPyModel(model="iasp91")
# Quake ML
quakeml = read_events('usgs.xml')
# Events of Interest
# events = ['73666231','7000gj2g','6000gdgn','7000gdwz','7000gg3w']
events = ['usp000hrky','usp000h4wq','usp000h1tv','usp000hqdx']
stas = ['E'+str(i).zfill(3) for i in np.arange(67,106)]
# Seismic Network
nw = 'IB'
df = pd.read_csv(f'{nw}.csv')
# df = df[df['Station Code'].isin(stas)]
# Waveform Service Provider
client = RoutingClient("eida-routing", credentials={'EIDA_TOKEN': 'eidatoken'})
for event in quakeml:
	evid = event.resource_id.id.split('=')[1].split('&')[0]#[2:]
	if evid in events:
		event.write(f'{evid}.xml', format="QUAKEML") 
		try:
			os.mkdir(f'Waveform/{evid}')
		except:
			pass
		evla = event['origins'][0].latitude
		evlo = event['origins'][0].longitude
		evdp = event['origins'][0].depth
		evti = event['origins'][0].time
		for i, row in tqdm(df.iterrows()):
			sta = row['Station Code']
			stla= row['Latitude']
			stlo= row['Longitude']
			dist = locations2degrees(evla,evlo,stla,stlo)
			arrivals = model.get_travel_times(source_depth_in_km=evdp/1000,
                                  distance_in_degree=dist)
			t1 = arrivals[0].time
			ts = evti + t1 - 20 # P - 20 seconds
			te = evti + t1 + 15*60 # P + 15 minutes
			try:
				st = client.get_waveforms(network=nw, station=sta, location ='*', channel ='*', starttime=ts, endtime=te)
				# inv = client.resp(nw, sta, t1)
				if len(st) > 0:
					st.write(f'Waveform/{evid}/{nw}.{sta}.mseed',format='MSEED')
			except:
				pass