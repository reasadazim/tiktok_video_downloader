from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from .jobs import delete_downloads


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(delete_downloads, 'interval', seconds=86400) #runs daily ones
    scheduler.start()
