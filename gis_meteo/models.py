from django.db import models


class GisMeteoRecord(models.Model):

    time_observation_times = [
        '00:00',
        '03:00',
        '06:00',
        '09:00',
        '12:00',
        '15:00',
        '18:00',
        '21:00',
    ]

    time_observation_choices = [(i, i) for i in time_observation_times]

    dt_parsed = models.DateTimeField(
        verbose_name='Время парсинга',
        auto_now_add=True
    )
    date_observation = models.DateField(
        verbose_name='Дата'
    )
    time_observation = models.CharField(
        verbose_name='Время',
        choices=time_observation_choices,
        max_length=5)
    value = models.PositiveSmallIntegerField(
        verbose_name='Значение'
    )
