from obspy import read_events
# Quake ML
quakeml = read_events('usgs.xml')
# Events of Interest
# events = ['73666231','7000gj2g','6000gdgn','7000gdwz','7000gg3w']
events = ['usp000hrky','usp000h4wq','usp000h1tv','usp000hqdx']
# Plotting
import cartopy.crs as ccrs
import matplotlib.pyplot as plt

ax = plt.axes(projection=ccrs.Mollweide())
ax.stock_img()
for event in quakeml:
	evid = event.resource_id.id.split('=')[1].split('&')[0]#[2:]
	if evid in events:
		evla = event['origins'][0].latitude
		evlo = event['origins'][0].longitude
		evmg = event['magnitudes'][0].mag
		ax.scatter(evlo,evla,c='r',transform=ccrs.Geodetic())
		ax.text(evlo,evla,f'{evid}\nMw:{evmg}',transform=ccrs.Geodetic())
		event.write(f'Events/{evid}.xml', format="QUAKEML") 
plt.savefig('map.png',dpi=300)