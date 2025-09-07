import webbrowser

import requests
import time
from threading import Thread

from src.databases.sqlite_db.engine_sqlite_db import sqlite_engine


class QMSTestEngine:
	def __init__(self):
		self.headers: dict = {
			'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36 Edg/139.0.0.0',
			'accept': 'application/json, text/plain, */*',
			'origin': 'https://www.qms.ru',
			'connection': 'keep-alive',
			'sec-ch-ua-platform': 'Windows',
			'sec-fetch-mode': 'cors',
			'sec-fetch-site': 'same-site'
		}

	def run_webbrowser(self):
		webbrowser.open('https://rt.qms.ru/')

	def download_test(self, url: str, duration=15, streams=8):
	    total_bytes = 0
	    start_time = time.time()
	    end_time = start_time + duration
	    session = requests.session()
	    
	    def download_chunk():
	        nonlocal total_bytes
	        while time.time() < end_time:
	            try:
	                with session.get(url, headers=self.headers, stream=True) as r:
	                    for chunk in r.iter_content(chunk_size=1024 * 1024):
	                        if time.time() >= end_time:
	                            break
	                        total_bytes += len(chunk)
	            except:
	                continue
	    
	    threads = []
	    for _ in range(streams):
	        t = Thread(target=download_chunk)
	        t.start()
	        threads.append(t)
	    
	    for t in threads:
	        t.join()
	    
	    elapsed = time.time() - start_time
	    download_mbps = (total_bytes * 8) / (elapsed * 1_000_000) 
	    return round(download_mbps, 2)

	def upload_test(self, url: str, duration=15, streams=4, chunk_size=1024*1024*25):
		session = requests.session()
		total_bytes = 0
		start_time = time.time()
		end_time = start_time + duration
		data = b'\0' * chunk_size  # 1 MB нулевых данных

		def upload_chunk():
			nonlocal total_bytes
			while time.time() < end_time:
				try:
				    response = session.post(url, headers=self.headers, data=data)
				    if response.ok:
				        total_bytes += chunk_size
				except:
				    continue

		threads = []
		for _ in range(streams):
			t = Thread(target=upload_chunk)
			t.start()
			threads.append(t)

		for t in threads:
			t.join()

		elapsed = time.time() - start_time
		upload_mbps = (total_bytes * 8) / (elapsed * 1_000_000) 
		return round(upload_mbps, 2)

	def start_test(self):
		download_speed = self.download_test(url='https://spb.qms.ru:20000/download.php?ckSize=25', duration=sqlite_engine.get_duration())
		upload_speed = self.upload_test(url='https://spb.qms.ru:20000/upload.php', duration=sqlite_engine.get_duration())

		data_of_test: dict = {
			'downstream': download_speed,
			'upstream': upload_speed
		}

		return data_of_test


qms_test_engine = QMSTestEngine()