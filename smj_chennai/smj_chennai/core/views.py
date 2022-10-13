from datetime import datetime
from typing import Dict
from rest_framework import status
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from smj_chennai.core.models import Bills, Charges, Documents, Party
from smj_chennai.core.serializers import (
    BillsSerializer,
    ChargesSerializer,
    DocumentsSerializer,
    PartySerializer,
)


class DocumentsAPI(ListAPIView):
    queryset = Documents.objects.order_by("-created_at").all()
    serializer_class = DocumentsSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        data = self.get_queryset()
        self.paginate_queryset(data)
        s = self.get_serializer(data, many=True)
        return self.get_paginated_response(s.data)

    def post(self, request, *args, **kwargs):
        data = request.data
        s = self.get_serializer(data=data)
        result = dict()
        if s.is_valid():
            s.save()
            result["status"] = True
            return Response(result)

        result["status"] = False
        result["errors"] = s.errors
        return Response(result, status=status.HTTP_400_BAD_REQUEST)


class DocumentUpdateAPI(GenericAPIView):
    serializer_class = DocumentsSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request, docket_number: int, *args, **kwargs):

        try:
            document = Documents.objects.get(docket_number=docket_number)
            d = self.get_serializer(document)
            return Response({"status": True, "result": d.data})
        except Documents.DoesNotExist:
            return Response({"status": False, "message": "Not found"})

    def put(self, request, docket_number: int, *args, **kwargs):

        try:
            document = Documents.objects.get(docket_number=docket_number)
            s = self.get_serializer(instance=document, data=request.data)
            result = {}
            if s.is_valid():
                result["status"] = True
                result["message"] = "updated!"
            else:
                result["status"] = False
                result["errors"] = s.errors
            return Response(result)
        except Documents.DoesNotExist:
            return Response({"status": False, "message": "Not found"})


class ChargesAPI(ListAPIView):
    serializer_class = ChargesSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryset = Charges.objects.order_by("-created_at").all()
        document_id = self.request.query_params.get("document")
        if document_id is not None:
            queryset = queryset.filter(
                document_id=document_id).prefetch_related()
        return queryset

    def get(self, request, *args, **kwargs):
        data = self.get_queryset()
        self.paginate_queryset(data)
        s = self.get_serializer(data, many=True)
        return self.get_paginated_response(s.data)

    def post(self, request, *args, **kwargs):
        data = request.data
        s = self.get_serializer(data=data)
        result = dict()
        if s.is_valid():
            s.save()
            result["status"] = True
            result["message"] = "Saved!"
            return Response(result)

        result["status"] = False
        result["errors"] = s.errors
        return Response(result, status=status.HTTP_400_BAD_REQUEST)


class ChargesUpdateAPI(GenericAPIView):
    serializer_class = ChargesSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request, id: int, *args, **kwargs):

        try:
            charge = Charges.objects.get(id=id)
            d = self.get_serializer(charge)
            return Response({"status": True, "result": d.data})
        except Charges.DoesNotExist:
            return Response({"status": False, "message": "Not found"})

    def put(self, request, id: int, *args, **kwargs):

        try:
            document = Charges.objects.get(id=id)
            s = self.get_serializer(instance=document, data=request.data)
            result = {}
            if s.is_valid():
                result["status"] = True
                result["message"] = "updated!"
                s.save()
            else:
                result["status"] = False
                result["errors"] = s.errors
            return Response(result)
        except Charges.DoesNotExist:
            return Response({"status": False, "message": "Not found"}, status=status.HTTP_400_BAD_REQUEST)


class PartyAPI(GenericAPIView):

    serializer_class = PartySerializer
    queryset = Party.objects.order_by("-created_at").all()

    def get_queryset(self):
        queryset = Party.objects.order_by("-created_at").all()
        search = self.request.query_params.get("search")
        if search is not None:
            queryset = queryset.filter(name__icontains=search)
        return queryset

    def get(self, request, *args, **kwargs):
        data = self.get_queryset()
        self.paginate_queryset(data)
        s = self.get_serializer(data, many=True)
        return self.get_paginated_response(s.data)


class BillsAPI(GenericAPIView):
    serializer_class = BillsSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        now = datetime.now()

        return Bills.objects.filter(
            payment_received_at__month=now.month, payment_received_at__year=now.year
        ).order_by("-created_at")

    def get(self, request, *args, **kwargs):
        data = self.get_queryset()
        self.paginate_queryset(data)
        s = self.get_serializer(data, many=True)
        return self.get_paginated_response(s.data)

    def post(self, request: Dict):

        data = request.data
        s = self.get_serializer(data=request.data)
        result = {}
        if s.is_valid():
            result["status"] = True
            s.save()
            result["message"] = "Created!"
            _status = status.HTTP_200_OK
        else:
            result["status"] = False
            result["errors"] = s.errors
            _status = status.HTTP_400_BAD_REQUEST
        return Response(result, status=_status)


class BillsUpdateAPI(GenericAPIView):

    serializer_class = BillsSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request: Dict, id: int, *args, **kwargs):

        try:
            bills = Bills.objects.get(id=id)
            d = self.get_serializer(bills)
            return Response({"status": True, "result": d.data})
        except Bills.DoesNotExist:
            return Response({"status": False, "message": "Not found"})

    def put(self, request, id: int, *args, **kwargs):

        try:
            document = Bills.objects.get(id=id)
            s = self.get_serializer(instance=document, data=request.data)
            result = {}
            if s.is_valid():
                result["status"] = True
                result["message"] = "updated!"
                s.save()
                _status = status.HTTP_200_OK
            else:
                result["status"] = False
                result["errors"] = s.errors
                _status = status.HTTP_400_BAD_REQUEST
            return Response(result, status=_status)
        except Bills.DoesNotExist:
            return Response({"status": False, "message": "Not found"}, status=status.HTTP_400_BAD_REQUEST)
