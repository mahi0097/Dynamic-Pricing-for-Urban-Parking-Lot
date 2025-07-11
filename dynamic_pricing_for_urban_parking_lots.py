# -*- coding: utf-8 -*-
"""Dynamic_Pricing_for_Urban_Parking_Lots.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1q5LqkdV2WEMznIFyqewy11HPJQlqARMA
"""

pip install pathway

!pip install nbconvert --quiet

!jupyter nbconvert \
  --ClearMetadataPreprocessor.enabled=True \
  --clear-output \
  --inplace \
  Dynamic_Pricing_for_Urban_Parking_Lots.ipynb

import pathway as pw

import pandas as pd

#Load with headers
df = pd.read_csv("dataset.csv")

#Rename headers to match Pathway schema
df = df.rename(columns={
    "SystemCodeNumber": "location_id",
    "LastUpdatedDate": "date",
    "LastUpdatedTime": "time",
    "Latitude": "latitude",
    "Longitude": "longitude",
    "Capacity": "capacity",
    "Occupancy": "occupancy",
    "QueueLength": "queue_length",
    "VehicleType": "vehicle_type",
    "TrafficConditionNearby": "traffic_level",
    "IsSpecialDay": "is_special_day"
})

# Combine timestamp
df["timestamp"] = pd.to_datetime(df["date"] + " " + df["time"], dayfirst=True, errors='coerce')

#Drop any rows where timestamp couldn't be parsed
df = df.dropna(subset=["timestamp"])

#Keep only required columns
df = df[[
    "location_id", "timestamp", "latitude", "longitude", "capacity",
    "occupancy", "queue_length", "vehicle_type", "traffic_level", "is_special_day"
]]

#Save cleaned version
df.to_csv("cleaned_dataset.csv", index=False)
print("✅ Cleaned CSV is ready.")

class ParkingSchema(pw.Schema):
    location_id: str  # <- was int, now string!
    timestamp: str
    latitude: float
    longitude: float
    capacity: int
    occupancy: int
    queue_length: int
    vehicle_type: str
    traffic_level: str
    is_special_day: int

input_table = pw.io.csv.read(
    "cleaned_dataset.csv",
    schema=ParkingSchema,
    mode="streaming",
    autocommit_duration_ms=1000
)

@pw.udf
def compute_price(occupancy, capacity):
    base_price = 10
    alpha = 0.5
    return base_price + alpha * (occupancy / capacity)

output_table = input_table.select(
    location_id=input_table.location_id,
    timestamp=input_table.timestamp,
    occupancy=input_table.occupancy,
    capacity=input_table.capacity,
    price=compute_price(input_table.occupancy, input_table.capacity)
)

def on_change(key, row: dict, time: int, is_addition: bool):
    if is_addition:
        print(f"[{row['timestamp']}] Lot {row['location_id']} - Price: ${row['price']:.2f}")

pw.io.subscribe(output_table, on_change)

@pw.udf
def model_2_price(occupancy, capacity, queue_length, traffic_level, special_day, vehicle_type):
    base_price = 10
    alpha = 1.0
    beta = 0.5
    gamma = 0.4
    delta = 0.3
    epsilon = 0.2
    lambda_factor = 0.5

    vehicle_weights = {
        "car": 1.0,
        "bike": 0.7,
        "truck": 1.5
    }

    traffic_score = {
        "low": 0.3,
        "average": 0.6,
        "high": 1.0
    }

    demand = (
        alpha * (occupancy / capacity) +
        beta * queue_length -
        gamma * traffic_score.get(traffic_level, 0.5) +
        delta * int(special_day) +
        epsilon * vehicle_weights.get(vehicle_type.lower(), 1.0)
    )

    # normalize demand to keep price in range (0.5x to 2x base)
    demand = min(max(demand, 0), 2)

    return base_price * (1 + lambda_factor * demand)

output_table = input_table.select(
    location_id=input_table.location_id,
    timestamp=input_table.timestamp,
    price=model_2_price(
        input_table.occupancy,
        input_table.capacity,
        input_table.queue_length,
        input_table.traffic_level,
        input_table.is_special_day,
        input_table.vehicle_type
    )
)

from math import radians, cos, sin, asin, sqrt

@pw.udf
def haversine(lat1, lon1, lat2, lon2):
    R = 6371
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat/2)**2 + cos(lat1)*cos(lat2)*sin(dlon/2)**2
    c = 2*asin(sqrt(a))
    return R * c

# Assume you've joined this lot with nearby competitors as competitor_table
@pw.udf
def model_3_price(my_price, my_lat, my_lon, comp_price, comp_lat, comp_lon, my_queue):
    distance = haversine(my_lat, my_lon, comp_lat, comp_lon)
    if distance < 0.5 and comp_price < my_price and my_queue > 3:
        return my_price * 0.9  # lower price
    elif distance < 0.5 and comp_price > my_price:
        return my_price * 1.1  # increase price
    return my_price

from bokeh.plotting import figure, output_notebook, show
from bokeh.models import ColumnDataSource
from bokeh.layouts import layout
from bokeh.io import push_notebook
from collections import defaultdict
from datetime import datetime

output_notebook()
lot_sources = defaultdict(lambda: ColumnDataSource(data=dict(x=[], y=[])))
plots = {}
handles = {}

def create_plot_for_lot(lot_id):
    p = figure(title=f"Real-Time Pricing for Lot {lot_id}", x_axis_type='datetime', width=700, height=300)
    p.line('x', 'y', source=lot_sources[lot_id], line_width=2)
    plots[lot_id] = p
    handles[lot_id] = show(p, notebook_handle=True)

def update_plot(lot_id, timestamp, price):
    if lot_id not in lot_sources:
        create_plot_for_lot(lot_id)
    lot_sources[lot_id].stream({'x': [timestamp], 'y': [price]}, rollover=100)
    push_notebook(handle=handles[lot_id])

pw.run()