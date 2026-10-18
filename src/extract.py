from requests import Session
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
from datetime import datetime, timedelta
from config import STATUS_FORCE_LIST, BASE_URL, END_POINT_AIR_QUALITY



def create_session():
    retry = Retry(total=4, backoff_factor=1, status_forcelist=STATUS_FORCE_LIST)
    session = Session()
    session.mount("https://", HTTPAdapter(max_retries=retry))

    return session


def fetch_data(
        lat,
        lon,
        timezone,
        mode,
        vars,
        **kwargs
):
    """
    lat:
    lon:
    timezone:
    mode:
    vars:

    forcast_day:
    start_date:
    end_date:
    """

    # setup params based on mode
    params = {
    'latitude': lat,
    'longitude': lon,
    'timezone': timezone,
    }

    if mode == 'hourly':
        if 'forcast_day' not in kwargs:
            forcast_day = 2
        
        params['hourly'] = vars
        params['forcast_day'] = forcast_day
    
    if mode == 'daily':
        if 'start_date' not in kwargs:
            start_date = datetime.now().date() - timedelta(days=3)
        if 'end_date' not in kwargs:
            end_date = datetime.now().date() - timedelta(days=1)

        params['daily'] = vars
        params['start_date'] = start_date
        params['end_date'] = end_date
    

    # fetch data
    session = create_session()

    try:
        response = session.get(f"{BASE_URL}{END_POINT_AIR_QUALITY}", params = vars, timeout=30)
        payload = response.json()
        print('Data fetched successfully')
    except Exception as e:
        payload = {}
        print(e)
    
    return {
        'data': payload,
        'mode': mode
    }


