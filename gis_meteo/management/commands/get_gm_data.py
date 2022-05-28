import time

from django.core.management.base import BaseCommand
from django.utils import timezone

from gis_meteo.services import GMGetter
from gis_meteo.models import GisMeteoRecord


def get_gm_data():
    last_parsed = GisMeteoRecord.objects.all().order_by('-id').first()
    if last_parsed:
        now = timezone.now()
        last_parsed_dt = last_parsed.dt_parsed
        delta = now - last_parsed_dt
        min_delta_seconds = 60 * 60

        if delta.seconds < min_delta_seconds:
            remaining = min_delta_seconds - delta.seconds
            remain_minutes = (remaining // 60) + 1
            print(f'try again in {remain_minutes} minutes')
            return False

    items = []
    for i in GMGetter().get_data():
        date_o, time_o, value = i
        items.append(GisMeteoRecord(
            date_observation=date_o,
            time_observation=time_o,
            value=value
        ))
    if items:
        GisMeteoRecord.objects.bulk_create(items)
    print('Parsed OK at {}'.format(now))
    return True


class Command(BaseCommand):

    def handle(self, *args, **options):

        while True:
            if get_gm_data():
                time.sleep(10)
            else:
                print("OK, I'll try in 10 min", timezone.now())
                time.sleep(60 * 10)



