from apscheduler.schedulers.asyncio import AsyncIOScheduler

scheduler = AsyncIOScheduler(timezone="UTC")


def start_scheduler():
    if not scheduler.running:
        scheduler.start()
        print("Scheduler запущен!")
