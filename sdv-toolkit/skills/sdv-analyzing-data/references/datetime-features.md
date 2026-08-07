# Datetime Feature Engineering

## Component Extraction

```python
df['year'] = df['timestamp'].dt.year
df['month'] = df['timestamp'].dt.month
df['day'] = df['timestamp'].dt.day
df['hour'] = df['timestamp'].dt.hour
df['dayofweek'] = df['timestamp'].dt.dayofweek
df['quarter'] = df['timestamp'].dt.quarter
```

## Cyclical Encoding

```python
import numpy as np

# Month as cyclical
month = df['timestamp'].dt.month
df['month_sin'] = np.sin(2 * np.pi * month / 12)
df['month_cos'] = np.cos(2 * np.pi * month / 12)

# Hour as cyclical
hour = df['timestamp'].dt.hour
df['hour_sin'] = np.sin(2 * np.pi * hour / 24)
df['hour_cos'] = np.cos(2 * np.pi * hour / 24)
```

## Duration Features

```python
# Time since reference
df['days_since_start'] = (df['timestamp'] - df['timestamp'].min()).dt.days

# Time to next event (requires sorting)
df['time_to_next'] = df['timestamp'].diff().shift(-1)
```
