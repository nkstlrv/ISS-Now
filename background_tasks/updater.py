from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from background_tasks.jobs import loc


def check_loc():
    scheduler = BackgroundScheduler()
    scheduler.add_job(loc, 'interval', seconds=5)
    scheduler.start()


if __name__ == "__main__":
    check_loc()