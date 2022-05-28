from django.shortcuts import render

from .models import GisMeteoRecord


def fix_times():
    GisMeteoRecord.objects.filter(time_observation='0:00').update(time_observation='00:00')
    GisMeteoRecord.objects.filter(time_observation='3:00').update(time_observation='03:00')
    GisMeteoRecord.objects.filter(time_observation='6:00').update(time_observation='06:00')
    GisMeteoRecord.objects.filter(time_observation='9:00').update(time_observation='09:00')


def index(request):
    fix_times()

    dates = sorted(set(GisMeteoRecord.objects.all().values_list('date_observation', flat=True)))

    current_date = dates[-1]

    context = {
        'dates': dates,
        'current_date': current_date
    }

    return render(request, 'gis_meteo/index.html', context)
