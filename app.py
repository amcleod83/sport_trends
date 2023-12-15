from flask import Flask, render_template 
from pytrends.request import TrendReq
import time
import datetime
from pandas import Timestamp
from functools import wraps
import logging
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)

# Decorator to add retry 
def retry(num_retries=3, delay=180):
    def wrapper(func):
        @wraps(func)
        def inner(*args, **kwargs):
            for i in range(num_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    logging.info("Exception occurred")
                    logging.info(e)
                    attempt = i + 1
                    if attempt == num_retries:
                        logging.info("Max retries exceeded")
                        return render_template('error.html', error=e)
                    logging.info(f"Attempt {attempt} of {num_retries}")
                    logging.info(f"Retrying in {delay}s")
                    time.sleep(delay)
            return None
        return inner
    return wrapper


@app.route('/')
@retry(num_retries=3, delay=10)
def home():
    pytrends = TrendReq(hl='en-UK', tz=360) 
    keywords = ['football', 'rugby', 'tennis']
    pytrends.build_payload(keywords, timeframe='today 3-m')

    try:
        logging.info("Trying to get data")
        data = pytrends.interest_over_time()
    except Exception as e:
        print(e)
        print("Max retries exceeded")
        return render_template('error.html', error=e.message)
    
    logging.info("Got data")
    
    dates = data.index.tolist() if data is not None else []
    formatted_dates = []

    for date in dates:
        if isinstance(date, Timestamp):
            formatted_date = date.strftime("%d %b %Y")
            formatted_dates.append(str(formatted_date))
        else:
            formatted_dates.append(str(datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S").strftime("%d %b %Y")))

    
    football_data = data['football'].tolist() if data is not None else [] 
    rugby_data = data['rugby'].tolist() if data is not None else []
    tennis_data = data['tennis'].tolist() if data is not None else []
    
    # sample data obtained from pytrends request above 

    # formatted_dates =['2023-09-15', '2023-09-16', '2023-09-17', '2023-09-18', '2023-09-19', '2023-09-20', '2023-09-21', '2023-09-22', '2023-09-23', '2023-09-24', '2023-09-25', '2023-09-26', '2023-09-27', '2023-09-28', '2023-09-29', '2023-09-30', '2023-10-01', '2023-10-02', '2023-10-03', '2023-10-04', '2023-10-05', '2023-10-06', '2023-10-07', '2023-10-08', '2023-10-09', '2023-10-10', '2023-10-11', '2023-10-12', '2023-10-13', '2023-10-14', '2023-10-15', '2023-10-16', '2023-10-17', '2023-10-18', '2023-10-19', '2023-10-20', '2023-10-21', '2023-10-22', '2023-10-23', '2023-10-24', '2023-10-25', '2023-10-26', '2023-10-27', '2023-10-28', '2023-10-29', '2023-10-30', '2023-10-31', '2023-11-01', '2023-11-02', '2023-11-03', '2023-11-04', '2023-11-05', '2023-11-06', '2023-11-07', '2023-11-08', '2023-11-09', '2023-11-10', '2023-11-11', '2023-11-12', '2023-11-13', '2023-11-14', '2023-11-15', '2023-11-16', '2023-11-17', '2023-11-18', '2023-11-19', '2023-11-20', '2023-11-21', '2023-11-22', '2023-11-23', '2023-11-24', '2023-11-25', '2023-11-26', '2023-11-27', '2023-11-28', '2023-11-29', '2023-11-30', '2023-12-01', '2023-12-02', '2023-12-03', '2023-12-04', '2023-12-05', '2023-12-06', '2023-12-07', '2023-12-08', '2023-12-09', '2023-12-10', '2023-12-11']
    # football_data = [32, 100, 100, 31, 27, 22, 26, 32, 98, 82, 29, 23, 22, 22, 29, 93, 62, 26, 23, 21, 21, 29, 90, 66, 27, 19, 20, 23, 32, 91, 47, 26, 25, 22, 21, 26, 80, 57, 23, 24, 21, 22, 26, 75, 56, 23, 21, 22, 20, 24, 81, 59, 25, 22, 20, 20, 26, 83, 64, 24, 21, 18, 27, 29, 82, 55, 25, 30, 22, 24, 37, 82, 62, 23, 22, 22, 19, 23, 65, 76, 27, 24, 20, 17, 20, 33, 29, 19] 
    # rugby_data = [19, 28, 30, 10, 7, 10, 18, 17, 34, 25, 10, 7, 10, 10, 16, 22, 20, 8, 6, 6, 10, 21, 36, 26, 11, 6, 6, 7, 10, 41, 54, 15, 6, 5, 6, 20, 38, 16, 6, 5, 5, 5, 15, 47, 14, 5, 3, 2, 2, 3, 5, 4, 2, 2, 2, 2, 2, 3, 3, 2, 2, 2, 2, 2, 3, 3, 2, 2, 2, 2, 2, 3, 2, 1, 1, 1, 1, 2, 3, 3, 2, 1, 1, 2, 2, 4, 3, 2] 
    # tennis_data = [4, 5, 5, 4, 4, 4, 4, 4, 5, 4, 4, 4, 4, 4, 4, 5, 5, 4, 5, 5, 4, 4, 4, 5, 5, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 5, 4, 5, 5, 5, 5, 6, 5, 4, 3, 4, 4, 3, 4, 5, 5, 6, 5, 6, 5, 9, 8, 4, 3, 3, 4, 4, 6, 6, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3]

    return render_template('graph.html', labels=formatted_dates, football=football_data, rugby=rugby_data, tennis=tennis_data)