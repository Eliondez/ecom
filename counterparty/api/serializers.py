from rest_framework import serializers
from ..models import Counterparty


class CounterpartySerializer(serializers.ModelSerializer):
    class Meta:
        model = Counterparty
        fields = [
            'id', 'name'
        ]
