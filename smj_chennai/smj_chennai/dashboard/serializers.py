from datetime import datetime, timedelta
from rest_framework import serializers


class AnalyticsSerializer(serializers.Serializer):

    key = serializers.CharField(max_length=100)
    value = serializers.IntegerField()

    class Meta:
        fields = "__all__"


def from_date(days=30):
    return datetime.now() - timedelta(days=days)


class DateRangeSerializer(serializers.Serializer):
    from_date = serializers.DateTimeField(default=from_date())

    to_date = serializers.DateTimeField(default=datetime.now())

    class Meta:
        fields = "__all__"
