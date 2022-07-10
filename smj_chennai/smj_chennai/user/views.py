from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from smj_chennai.user.serializers import ProfileSerializer


# Create your views here.


class ProfileApiView(GenericAPIView):
    serializer_class = ProfileSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):

        user = request.user
        d = self.get_serializer(user)
        return Response({"status": True, "result": d.data})
