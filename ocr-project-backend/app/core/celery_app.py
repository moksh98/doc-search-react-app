from celery import Celery
from app.core.settings import settings

celapp = Celery('proj',
                broker="redis://"+settings.RD_HOST+":"+str(settings.RD_PORT)+"/0",
                backend="redis://"+settings.RD_HOST+":"+str(settings.RD_PORT)+"/0",
                include=["app.tasks.upload"],
                task_serializer='pickle',
                result_serializer='pickle',
                accept_content = ['application/json', 'application/x-python-serialize'],
)

# Optional configuration, see the application user guide.
# celapp.conf.update(
#     result_expires=3600,
# )
