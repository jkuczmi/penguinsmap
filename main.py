import pandas as pd
import geopandas as gpd
import pandas as pd
import geopandas as gpd
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import streamlit as st
import numpy as np
import matplotlib.patches as mpatches
import matplotlib.lines as mlines
colors_list = ['darkorange', 'darkgreen', 'blue', 'crimson', 'darkviolet', 'yellow']

def draw_single(map, df_subset, color_temp):
    if len(df_subset)==0:
        return map
    x_i, y_i = map(df_subset[LONG], df_subset[LAT])
    
    map.scatter(x_i,y_i, marker='o',s=22,color=color_temp)
    return map


def draw_zoomed(df_subset, show=False, color_temp = 'yellow'):
    
    draw_single(map, df_subset, color_temp)
    if show:
        plt.show()
    return map


def prepare_map():
    map = Basemap(projection='stere',resolution='c',
                lat_0=-90, lon_0=(-100+-30)/2.,  lat_ts=(-90.+-55.)/2.,
                llcrnrlon=-100,urcrnrlon=-50,llcrnrlat=-70,urcrnrlat=-60)

    map.drawmapboundary(fill_color='skyblue')
    map.fillcontinents(color='azure', lake_color='aqua')
    map.drawcoastlines()
    map.drawmeridians(np.arange(0,360,10), labels=[False, False, False, True])
    map.drawparallels(np.arange(-90,90,5), labels=[False, True, False, False])
    return map

def prepare_big_map():
    map = Basemap(projection='spstere', boundinglat=-60,lon_0=-250)
    map.drawmapboundary(fill_color='skyblue')
    map.fillcontinents(color='azure',lake_color='aqua')
    map.drawcoastlines()
    map.drawmeridians(np.arange(0,360,20), labels=[False, True, False, False])
    map.drawparallels(np.arange(-90,90,5), labels=[False, False, False, True])
    return map

def draw_map(map, df_subset,show=False, color_temp = 'yellow'):
    if len(df_subset)==0:
        return map
    x_i, y_i = map(df_subset[LONG], df_subset[LAT])
    map.scatter(x_i,y_i, marker='o', s=22, color=color_temp)
    if show:
        plt.show()
    return map

def draw_south_pole(map):
    x_sp,y_sp = map(0,-90)
    map.scatter(x_sp,y_sp,marker='.', color='black')
    ax.annotate('Geographic South Pole', (x_sp,y_sp))
    return map

# loading
LONG = 'longitude_epsg_4326'
LAT = 'latitude_epsg_4326'
YEAR = 'year'
COUNT = 'penguin_count'
NAME='common_name'

geodf = gpd.read_file('AllCounts_V_4_1.csv')
geodf.crs = 'epsg:4326'

# processing
geodf.replace('', None, inplace=True)
geodf = geodf.dropna(subset=[YEAR, LONG, LAT, COUNT])
geodf['year'] = geodf['year'].astype('int')
geodf[COUNT] = geodf[COUNT].astype('int')
geodf[LONG]=geodf[LONG].astype('float')
geodf[LAT]=geodf[LAT].astype('float')

st.title("Map of Penguin Colonies in Antarctica")
st.write("Select species of penguins to display their location on the map in 1989, 1999, 2009, or 2019.")

years_list = [1989,1999,2009,2019]

selected_species=[]
selected_species = st.multiselect("Select species", set(list(geodf[NAME])))
selected_year = st.selectbox("Choose year", years_list)


fig = plt.figure(figsize=(12,10))
st.subheader(f"Penguin colonies spotted in {selected_year}")

ax = fig.add_subplot(121)
df_selected = geodf[geodf[YEAR]==selected_year]

map = prepare_big_map()
map=draw_south_pole(map)
for n, specie in enumerate(selected_species):
    map = draw_map(map, df_selected[df_selected[NAME]==specie],color_temp=colors_list[n])



ax = fig.add_subplot(122)

ax.set_title(f"Zoom on Antarctic Peninsula")
df_selected = geodf[geodf[YEAR]==selected_year]
map = prepare_map()
patches = []
for n, specie in enumerate(selected_species):
    map = draw_single(map, df_selected[df_selected[NAME]==specie],color_temp= colors_list[n])
    patch = mlines.Line2D([], [], color=colors_list[n], marker='o', linestyle='None', markersize=10, label=specie)
    patches.append(patch)
# if len(selected_species) >0:
#     red_patch = mpatches.Patch(color='red', label='The red data')
if len(selected_species) >0:
    ax.legend(handles=patches,loc='upper center', bbox_to_anchor=(0.5, -0.05),  ncol=2)

# fig.legend(loc='outside lower center', title='outside lower center')
st.pyplot(fig)
st.caption("References: Dataset MAPPPD v4.1 from: https://www.penguinmap.com/mapppd/ ")
