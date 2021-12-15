import os

from celery import Celery
from kombu import Queue, Exchange

# Установка переменных окружения из django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# Инициализация приложения
app = Celery('config')

# Использование настроек django
app.config_from_object('django.conf:settings', namespace='CELERY')

# Установка очереди для рабочих Celery поумолчанию
app.conf.task_default_queue = 'default'

# Создание очередей для рабочих Celery
CELERY_QUEUES = (
    Queue('default', Exchange('default'), routing_key='default'),
    Queue('email', Exchange('email'), routing_key='email'),
    Queue('solo_task', Exchange('solo_task'), routing_key='solo_task'),
    Queue('multi_task', Exchange('multi_task'), routing_key='multi_task'),
    Queue('beat_task', Exchange('beat_task'), routing_key='beat_task'),
)

# Автоматический поиск задач
app.autodiscover_tasks(['users.services'])

# Создание расписания периодических задач для рабочих Celery
app.conf.beat_schedule = {
    # 'example': {
    #     'task': 'api.tasks.update_all_klines',
    #     'schedule': 1800,
    #     'args': ('5m', '30m', 1800)
    # },
}
