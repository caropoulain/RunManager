from fitparse import FitFile
from io import BytesIO

def process_fit_file(file_bytes: bytes) -> dict:
    f = FitFile(BytesIO(file_bytes))
    lat = []; lon = []; alt = []; heart = []; cadence = []
    timestamp_first = None; timestamp_last = None
    total_distance = None

    for record in f.get_messages('record'):
        values = {v.name: v.value for v in record}
        ts = values.get('timestamp')
        if ts:
            if timestamp_first is None:
                timestamp_first = ts
            timestamp_last = ts

        if values.get('altitude') is not None:
            alt.append(values.get('altitude'))
        if values.get('heart_rate') is not None:
            heart.append(values.get('heart_rate'))
        if values.get('cadence') is not None:
            cadence.append(values.get('cadence'))
        if values.get('distance') is not None:
            total_distance = values.get('distance')

    duration_sec = None
    if timestamp_first and timestamp_last:
        duration_sec = (timestamp_last - timestamp_first).total_seconds()
    avg_hr = sum(heart)/len(heart) if heart else None
    avg_cadence = sum(cadence)/len(cadence) if cadence else None

    pace_s_per_km = None
    if total_distance and duration_sec:
        pace_s_per_km = duration_sec / (total_distance/1000)

    gain = 0
    for i in range(1, len(alt)):
        diff = alt[i] - alt[i-1]
        if diff > 0: gain += diff

    return {
        'duration_sec': duration_sec,
        'distance_m': total_distance,
        'avg_hr': avg_hr,
        'avg_cadence': avg_cadence,
        'pace_s_per_km': pace_s_per_km,
        'elevation_gain_m': gain,
    }