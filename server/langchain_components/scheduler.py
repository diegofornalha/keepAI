from typing import Dict, Any
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.date import DateTrigger
from apscheduler.triggers.interval import IntervalTrigger


class TaskScheduler:
    def __init__(self):
        self.scheduler = BackgroundScheduler()
        self.scheduler.start()

    def schedule_task(
        self, task_id: str, func: callable, trigger_type: str, **trigger_args
    ) -> Dict[str, Any]:
        try:
            if trigger_type == "date":
                trigger = DateTrigger(
                    run_date=trigger_args.get("run_date", datetime.now())
                )
            elif trigger_type == "interval":
                trigger = IntervalTrigger(
                    seconds=trigger_args.get("seconds", 0),
                    minutes=trigger_args.get("minutes", 0),
                    hours=trigger_args.get("hours", 0),
                )
            else:
                return {"success": False, "error": "Tipo de trigger não suportado"}

            self.scheduler.add_job(func=func, trigger=trigger, id=task_id)
            return {"success": True}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def remove_task(self, task_id: str) -> Dict[str, Any]:
        try:
            self.scheduler.remove_job(task_id)
            return {"success": True}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def get_tasks(self) -> Dict[str, Any]:
        try:
            jobs = self.scheduler.get_jobs()
            return {"success": True, "jobs": jobs}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def shutdown(self) -> Dict[str, Any]:
        try:
            self.scheduler.shutdown()
            return {"success": True}
        except Exception as e:
            return {"success": False, "error": str(e)}
