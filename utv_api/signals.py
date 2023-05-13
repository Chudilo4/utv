import logging

from django.dispatch import receiver
from django.db.models.signals import post_save
from utv_api.models import Worker


logger = logging.getLogger(__name__)


@receiver(post_save, sender=Worker)
def post_save_comments(**kwargs):
    logger.info('Добавлено рабочее время')
