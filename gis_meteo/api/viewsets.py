import json

from rest_framework import views
from rest_framework.response import Response

from ..models import GisMeteoRecord


class GetLastView(views.APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request):
        results = []
        group = request.query_params.get('group')

        if group:
            group = json.loads(group)
            print('GROUPED', group)
            group_keys = GisMeteoRecord.objects.values_list('date_observation', flat=True).distinct()
            for group_key in group_keys:
                results.append({
                    'key': group_key,
                    'items': [
                        {
                            'id': i.id,
                            'date_observation': i.date_observation,
                            'time_observation': i.time_observation,
                            'value': i.value
                        } for i in GisMeteoRecord.objects.filter(date_observation=group_key)
                    ],
                    'count': 15
                })
        else:
            records = GisMeteoRecord.objects.order_by('-id')[:100]
            for i in records:
                results.append({
                    'id': i.id,
                    'date_observation': i.date_observation,
                    'time_observation': i.time_observation,
                    'value': i.value
                })

        return Response({
            'totalCount': 150,
            'summary': {},
            'data': results
        })


class TestView(views.APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        """
        Return a list of all users.
        """
        dates = sorted(set(GisMeteoRecord.objects.filter(
            date_observation__in=[
                '2022-05-22',
                '2022-05-21',
                '2022-05-20',
                '2022-05-19',
            ]
        ).values_list('date_observation', flat=True)))

        values_by_date = dict()

        for date_str in dates:
            records = GisMeteoRecord.objects.filter(date_observation=date_str).order_by('time_observation')
            if date_str not in values_by_date:
                values_by_date[date_str] = dict()
            for record in records:
                time_str = record.time_observation
                v = record.value
                if time_str not in values_by_date[date_str]:
                    values_by_date[date_str][time_str] = {
                        'time': time_str,
                        'l': v,
                        'h': v,
                        'o': v,
                        'c': v
                    }
                else:
                    if v < values_by_date[date_str][time_str]['l']:
                        values_by_date[date_str][time_str]['l'] = v
                    if v > values_by_date[date_str][time_str]['h']:
                        values_by_date[date_str][time_str]['h'] = v
                    values_by_date[date_str][time_str]['c'] = v

        times = [
            '00:00',
            '03:00',
            '06:00',
            '09:00',
            '12:00',
            '15:00',
            '18:00',
            '21:00',
        ]

        res = []
        for i in dates:
            current_item = dict()
            current_item['date'] = i
            inner = []
            for time_str in times:
                inner.append(values_by_date[i][time_str])
            current_item['inner'] = inner
            res.append(current_item)

        return Response(res)
