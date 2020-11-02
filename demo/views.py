from pip._vendor.distlib.compat import filter
from rest_framework.decorators import api_view
# from django.shortcuts import render
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import authentication_classes
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated

from rest_framework import status, viewsets
from rest_framework.decorators import action

from django.forms.models import model_to_dict
from rest_framework.parsers import MultiPartParser, FileUploadParser, FormParser
from rest_framework.decorators import parser_classes


# @api_view(['GET'])
# @authentication_classes([JWTAuthentication])
# @permission_classes([IsAuthenticated])
# def test_auth_perm_api_view(request, format=None):
#     return Response({"code": code, "message": message, "data": data})


import demo.codes as codes

@api_view(['GET'])
def special_case_2003(request, format=None):
    data = 123
    return Response({"code": codes.CODE_SUCCESS, "message": codes.MSG_SUCCESS, "data": data})


@api_view(['GET', 'post'])
def year_archive(request, year, format=None):
    print(year)
    print(request)
    print(request.data)
    print(request.query_params)
    return Response({"code": codes.CODE_SUCCESS, "message": codes.MSG_SUCCESS, "data": "data"})

@api_view(['GET', 'post'])
def month_archive(request, year, month, format=None):
    print(year)
    print(month)
    print(request)
    print(request.data)
    print(request.query_params)
    return Response({"code": codes.CODE_SUCCESS, "message": codes.MSG_SUCCESS, "data": "data"})


from demo.models import FileInfo, FileInfo_has_Date, FileInfoDate, FileInfoHasGroup, FileGroup, GroupSearchResult
from demo.serializers import FileInfoSerializer#, FileInfoDateSerializer, FileInfoHasGroupSerializer, FileGroup2Serializer, GroupSearchResultSerializer
#
#
class FileInfoSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing user instances.
    """
    serializer_class = FileInfoSerializer
    queryset = FileInfo.objects.all()
#
#    @action()
#    def xxx(): pass
#
#    @action()
#    def xxxx(): pass
#
#    @action()
#    def xxxxx(): pass
#
#
#class FileInfoDateSet(viewsets.ModelViewSet):
#    """
#    A viewset for viewing and editing user instances.
#    """
#    serializer_class = FileInfoDateSerializer
#    queryset = FileInfoDate.objects.all()
#
#
#class FileInfoHasGroupSet(viewsets.ModelViewSet):
#    """
#    A viewset for viewing and editing user instances.
#    """
#    serializer_class = FileInfoHasGroupSerializer
#    queryset = FileInfoHasGroup.objects.all()
#
#
#class FileGroup2Set(viewsets.ModelViewSet):
#    """
#    A viewset for viewing and editing user instances.
#    """
#    serializer_class = FileGroup2Serializer
#    queryset = FileGroup2.objects.all()
#
#
#class GroupSearchResultSet(viewsets.ModelViewSet):
#    """
#    A viewset for viewing and editing user instances.
#    """
#    serializer_class = GroupSearchResultSerializer
#    queryset = GroupSearchResult.objects.all()
