# Datetime Feature Engineering

Complete guide to extracting features from datetime columns.

## Component Extraction

Extract individual date/time components as numeric features:

```python
# Calendar components
df['year'] = df['timestamp'].dt.year
df['month'] = df['timestamp'].dt.month
df['day'] = df['timestamp'].dt.day
df['dayofweek'] = df['timestamp'].dt.dayofweek  # 0=Monday
df['dayofyear'] = df['timestamp'].dt.dayofyear
df['quarter'] = df['timestamp'].dt.quarter

# Time components
df['hour'] = df['timestamp'].dt.hour
df['minute'] = df['timestamp'].dt.minute

# Boolean flags
df['is_weekend'] = df['timestamp'].dt.dayofweek.isin([5, 6])
df['is_month_start'] = df['timestamp'].dt.is_month_start
df['is_month_end'] = df['timestamp'].dt.is_month_end
```

## Cyclical Encoding

Encode time features as cyclical (sin/cos) to preserve circular relationships:

```python
import numpy as np

def cyclical_encode(series, period):
    """Encode a cyclical feature using sine and cosine.
    
    Args:
        series: pandas Series with values 0 to period-1
        period: the period length (e.g., 12 for months, 24 for hours)
    """
    sin_val = np.sin(2 * np.pi * series / period)
    cos_val = np.cos(2 * np.pi * series / period)
    return sin_val, cos_val

# Month cyclical encoding (period=12)
df['month_sin'], df['month_cos'] = cyclical_encode(df['timestamp'].dt.month, 12)

# Hour cyclical encoding (period=24)
df['hour_sin'], df['hour_cos'] = cyclical_encode(df['timestamp'].dt.hour, 24)

# Day of week cyclical encoding (period=7)
df['dow_sin'], df['dow_cos'] = cyclical_encode(df['timestamp'].dt.dayofweek, 7)

# Day of year cyclical encoding (period=365)
df['doy_sin'], df['doy_cos'] = cyclical_encode(df['timestamp'].dt.dayofyear, 365)
```

**Why cyclical?** December (12) is close to January (1) - raw encoding loses this.

## Duration Features

```python
# Time since reference date
reference_date = df['timestamp'].min()
df['days_since_start'] = (df['timestamp'] - reference_date).dt.days

# Time since specific event
df['days_since_event'] = (df['timestamp'] - df['event_date']).dt.days

# Time until next event (requires sorting)
df = df.sort_values('timestamp')
df['time_to_next'] = df['timestamp'].diff().shift(-1).dt.total_seconds() / 3600  # hours

# Age of record
df['record_age_days'] = (pd.Timestamp.now() - df['timestamp']).dt.days
```

## Seasonality Features

```python
# Season of year
def get_season(month):
    if month in [12, 1, 2]:
        return 'winter'
    elif month in [3, 4, 5]:
        return 'spring'
    elif month in [6, 7, 8]:
        return 'summer'
    else:
        return 'fall'

df['season'] = df['timestamp'].dt.month.apply(get_season)

# Part of day
def get_part_of_day(hour):
    if 5 <= hour < 12:
        return 'morning'
    elif 12 <= hour < 17:
        return 'afternoon'
    elif 17 <= hour < 21:
        return 'evening'
    else:
        return 'night'

df['part_of_day'] = df['timestamp'].dt.hour.apply(get_part_of_day)
```

## Time Differences Between Records

```python
# Time since previous record
df = df.sort_values('timestamp')
df['time_since_prev'] = df['timestamp'].diff().dt.total_seconds()

# Time between events per group
df['time_since_prev_by_user'] = df.groupby('user_id')['timestamp'].diff().dt.total_seconds()

# Rolling time windows
df['rolling_7d_count'] = df.set_index('timestamp').rolling('7D').size().values
```

## Business Calendar Features

```python
# US Federal holidays (requires holidays package)
import holidays

us_holidays = holidays.US()
df['is_holiday'] = df['timestamp'].dt.date.isin(us_holidays)

# Business day features
df['is_business_day'] = ~df['timestamp'].dt.dayofweek.isin([5, 6]) & ~df['is_holiday']

# Days to/from month end
df['days_to_month_end'] = df['timestamp'].dt.days_in_month - df['timestamp'].dt.day
```

## Lag Features

```python
# Sort by timestamp first
df = df.sort_values('timestamp')

# Lagged values (previous time periods)
df['value_lag_1d'] = df['value'].shift(1)
df['value_lag_7d'] = df['value'].shift(7)

# Lagged values within groups
df['value_lag_1d_by_user'] = df.groupby('user_id')['value'].shift(1)
```

## Complete Example

```python
import pandas as pd
import numpy as np

def engineer_datetime_features(df, timestamp_col='timestamp'):
    """Engineer comprehensive datetime features."""
    df = df.copy()
    ts = df[timestamp_col]
    
    # Calendar components
    df['year'] = ts.dt.year
    df['month'] = ts.dt.month
    df['day'] = ts.dt.day
    df['dayofweek'] = ts.dt.dayofweek
    df['hour'] = ts.dt.hour
    df['quarter'] = ts.dt.quarter
    
    # Cyclical encoding
    df['month_sin'] = np.sin(2 * np.pi * ts.dt.month / 12)
    df['month_cos'] = np.cos(2 * np.pi * ts.dt.month / 12)
    df['hour_sin'] = np.sin(2 * np.pi * ts.dt.hour / 24)
    df['hour_cos'] = np.cos(2 * np.pi * ts.dt.hour / 24)
    
    # Boolean flags
    df['is_weekend'] = ts.dt.dayofweek.isin([5, 6])
    df['is_month_start'] = ts.dt.is_month_start
    
    # Duration
    df['days_since_start'] = (ts - ts.min()).dt.days
    
    return df
```
