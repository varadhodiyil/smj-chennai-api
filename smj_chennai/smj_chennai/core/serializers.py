from rest_framework import serializers
from smj_chennai.core import models


class DocumentsSerializer(serializers.ModelSerializer):
    party = serializers.CharField(max_length=250)

    def to_representation(self, instance):

        data = super().to_representation(instance)
        data["party"] = instance.party.name
        return data

    def save(self, **kwargs):
        self.validated_data["party"], _ = models.Party.objects.get_or_create(
            name=self.validated_data["party"]
        )
        return super().save(**kwargs)

    class Meta:
        model = models.Documents
        fields = "__all__"


class ChargesSerializer(serializers.ModelSerializer):

    party = serializers.CharField(max_length=250)
    document = serializers.CharField(max_length=20)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["party"] = instance.party.name
        data["document"] = instance.document.docket_number
        return super().to_representation(data)

    def save(self, **kwargs):

        self.validated_data["party"], _ = models.Party.objects.get_or_create(
            name=self.validated_data["party"]
        )
        self.validated_data["document"] = models.Documents.objects.get(
            docket_number=self.validated_data["document"]
        )
        return super().save(**kwargs)

    class Meta:
        model = models.Charges
        fields = "__all__"


class PartySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Party
        fields = "__all__"


class BillsSerializer(serializers.ModelSerializer):
    party = serializers.CharField(max_length=250)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["party"] = instance.party.name
        return super().to_representation(data)

    def save(self, **kwargs):

        self.validated_data["party"], _ = models.Party.objects.get_or_create(
            name=self.validated_data["party"]
        )
        return super().save(**kwargs)

    class Meta:
        model = models.Bills
        fields = "__all__"
