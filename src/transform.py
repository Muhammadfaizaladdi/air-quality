import pandas as pd
from zoneinfo import ZoneInfo
from uuid import uuid4
from datetime import datetime, timezone

def normalize_data(district, lat, lon, tz, payload):
    frame = None
    data = None


    if payload['mode'] == 'hourly':
        data = payload['hourly']
    else:
        data = payload['daily']

    
    frame = pd.DataFrame({
        'local_time' : data['time'],
        'pm10' : data['pm10'],
        'pm25' : data['pm2_5'],
        'carbon_monoxide' : data['carbon_monoxide'],
        'carbon_dioxide_ppm' : data['carbon_dioxide'],
        'nitroden_dioxide' : data['nitroden_dioxide'],
        'ozone' : data['ozone'],
        'sulphur_dioxide' : data['sulphur_dioxide'],
    })


    local = pd.to_datetime(frame['local_time']).dt.tz_localize(ZoneInfo(tz))
    frame['local_time'] = pd.to_datetime(frame['local_time']).dt.strftime('%Y-%m-%d %H:%M:%S')
    frame['observed_at'] = local.dt.tz_convert("UTC")
    frame['kecamatan'] = district
    frame['latitude'] = lat
    frame['longitude'] = lon
    frame['source'] = "open_meteo"
    frame['ingestion_id'] = str(uuid4())
    
    return frame
        