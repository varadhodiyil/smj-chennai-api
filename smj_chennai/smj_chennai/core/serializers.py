from rest_framework import serializers
from smj_chennai.core import models


class DocumentsSerializer(serializers.ModelSerializer):
    party = serializers.CharField(max_length=250)

    def save(self, **kwargs):
        self.validated_data["party"], _ = models.Party.objects.get_or_create(
            name=self.validated_data["party"]
        )
        return super().save(**kwargs)

    class Meta:
        model = models.Documents
        fields = "__all__"


class ChargesSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Charges
        fields = "__all__"
