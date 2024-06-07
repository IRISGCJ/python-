import streamlit as st
import folium
from folium.plugins import MousePosition
import geopandas as gpd
from streamlit_folium import st_folium
from folium.features import GeoJson

# 标题
st.title("天目山野外实习区域POI点")

# 创建Map控件，不加载底图（tiles=None）
m = folium.Map(location=[30.0, 120.0], zoom_start=12, tiles=None)

# 在线加载天目山野外实习区域的POI数据
data_path="tms_POIs.geojson"
gdf=gpd.read_file(data_path)

# 创建POI点矢量要素图层
feature_group = folium.FeatureGroup(name="POI")

for idx, row in gdf.iterrows():
    popup_html = f"""
    <h4>{row['NAME']}</h4>
    <h6>{row['text']}</h6>
    <img src="{row['photo_url']}" width="100"/>
    """
    folium.Marker(
        location=[row.geometry.y, row.geometry.x],
        popup=popup_html
    ).add_to(feature_group)

feature_group.add_to(m)

# 创建三个Tile（地图切片）图层
tile_layers = {
    "Esri全球影像": "Esri.WorldImagery",
    "Carto地图": "CartoDB.Positron",
    "高德地图": "Gaode.Normal"
}

for name, tile in tile_layers.items():
    if "高德地图" in name:
        folium.TileLayer(
            tiles=tile, 
            name=name,
            attr='高德地图'
        ).add_to(m)
    else:
        folium.TileLayer(tile, name=name).add_to(m)

# 设置初始底图为高德地图
folium.TileLayer(
    tiles="Gaode.Normal",
    name="高德地图",
    attr='高德地图'
).add_to(m)

# 创建图层控制控件并添加到地图控件中
folium.LayerControl().add_to(m)

# 创建显示坐标控件并添加到地图控件中
MousePosition().add_to(m)

# 利用POI数据的范围设置地图的初始范围
minx, miny, maxx, maxy = gdf.total_bounds
m.fit_bounds([[miny, minx], [maxy, maxx]])

# 显示地图
st_folium(m, width=700, height=500)
