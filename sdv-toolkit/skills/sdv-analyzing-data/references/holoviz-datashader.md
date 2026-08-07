# HoloViz and Datashader for Large Data

## Automatic Datashader Rasterization

```python
import hvplot.pandas
import datashader as ds

# Automatic rasterization for >1M points
df.hvplot.scatter(x='x', y='y', datashade=True, width=800, height=600)
```

## Linked Brushing

```python
import holoviews as hv
from holoviews import opts

scatter = hv.Scatter(df, 'x', 'y')
hist = hv.Histogram(df, 'y')

# Link selections
scatter.opts(tools=['box_select']) + hist
```

## Geospatial with GeoViews

```python
import geoviews as gv
import cartopy.crs as ccrs

gv.Points(df, ['lon', 'lat'], crs=ccrs.PlateCarree()).opts(
    projection=ccrs.Mercator(),
    global_extent=True
)
```
