# Bokeh Server Applications

## Real-time Streaming

```python
from bokeh.plotting import figure, curdoc
from bokeh.models import ColumnDataSource
import random

source = ColumnDataSource({'x': [], 'y': []})

p = figure(title="Real-time Stream")
p.line('x', 'y', source=source)

def update():
    new = {'x': [source.data['x'][-1] + 1 if source.data['x'] else 0], 
           'y': [random.random()]}
    source.stream(new)

curdoc().add_periodic_callback(update, 100)  # ms
curdoc().add_root(p)
```

Run: `bokeh serve app.py`

## Custom JS Callbacks

```python
from bokeh.models import CustomJS, Slider

slider = Slider(start=0, end=10, value=1, step=0.1)
slider.js_link('value', glyph, 'radius')
```
