import pandas as pd
from obspy import UTCDateTime, read_events
from obspy.clients.fdsn import Client

# df = pd.read_csv('IB.csv')
# df['Start'] = df['Start'].astype('datetime64[ns]')
# df['End'] = df['End'].astype('datetime64[ns]')

# client = Client("IRIS")

# t1 = UTCDateTime(df['Start'].max())
# t2 = UTCDateTime(df['End'].min())

# cat = client.get_events(starttime=t1, endtime=t2, minmagnitude=6,maxmagnitude=7.5,catalog="USGS")
cat = read_events('usgs.xml')
cat.plot(outfile='usgs.png',show=False,dpi=300,figsize=(16,9))