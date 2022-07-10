from rest_framework import status
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from smj_chennai.core.models import Charges, Documents
from smj_chennai.core.serializers import ChargesSerializer, DocumentsSerializer


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


class ChargesAPI(ListAPIView):
    serializer_class = ChargesSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryset = Charges.objects.order_by("-created_at").all()
        document_id = self.request.query_params.get("document")
        if document_id is not None:
            queryset = queryset.filter(document_id=document_id).prefetch_related()
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
            return Response(result)

        result["status"] = False
        result["errors"] = s.errors
        return Response(result, status=status.HTTP_400_BAD_REQUEST)
