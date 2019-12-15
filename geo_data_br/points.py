from typing import List
from shapely.geometry import Point
import geopandas as gpd
import pandas as pd

def data_on_points(points: List[Point], level='best'):
    '''points is a list of longitute, latitude tuples shapely.geometry.Point objects'''
    if level not in ('best', 'all'):
        raise TypeError('choose a suported_level')
    if not points:
        return pd.DataFrame()
    points = [Point(p) for p in points]
    points =  gpd.GeoDataFrame(geometry=points)
    points.crs = {'init' :'epsg:4326'} # default to this projection
    geo_dfs = get_geo_dataframes()
    udh_level = gpd.sjoin(points, geo_dfs['udh'])
    missing_points = points.index.difference(udh_level.index)
    if level == 'best':
        if missing_points.empty:
            municipality_level = gpd.GeoDataFrame()
        else:
            municipality_level = gpd.sjoin(points.loc[missing_points], geo_dfs['municipality'])
        out = pd.concat([udh_level, municipality_level], sort=False)
        assert out.index.shape == points.index.shape
        return out.loc[points.index]
    elif level == 'all':
        raise NotImplementedError

from importlib.resources import path
import functools, joblib
@functools.lru_cache()
def get_geo_dataframes():
    out = {}
    with path('geo_data_br.data', 'municipality.pickle') as municipality, \
            path('geo_data_br.data', 'udh.pickle') as udh:
        out['municipality'] = joblib.load(municipality)
        out['udh'] = joblib.load(udh)
    for level_name, df in out.items():
        df['level'] = level_name
        df.columns = [c.lower() for c in df.columns]
        df.to_crs({'init': 'epsg:4326'}, inplace=True)
        df.sindex
    return out
