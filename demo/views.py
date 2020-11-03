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
from demo.serializers import FileInfoSerializer, FileGroupSerializer, FileInfoHasGroupSerializer, \
    GroupSearchResultSerializer, FileInfoDateSerializer, FileInfoWithDateSerializer, DateSerializer

#
#
from rest_framework import generics, mixins, views


# class FileInfoSet(viewsets.ModelViewSet):
class FileInfoSet(mixins.CreateModelMixin,
                  # mixins.RetrieveModelMixin,
                  # mixins.UpdateModelMixin,
                  # mixins.DestroyModelMixin,
                  # mixins.ListModelMixin,
                  viewsets.GenericViewSet):
    """
    A viewset for viewing and editing user instances.
    """
    serializer_class = FileInfoSerializer
    queryset = FileInfo.objects.all()

    def list(self, request, *args, **kwargs):
        """
        自定义搜索
        """
        # 路径
        # queryset = FileInfo.objects.filter(path__contains="ab")
        # serializer = self.get_serializer(queryset, many=True)
        # return Response(serializer.data)

        # 标记
        # queryset = FileInfo.objects.filter(tag__contains="ab")
        # serializer = self.get_serializer(queryset, many=True)
        # return Response(serializer.data)

        # 日期时间:
        # raw也能直接返回:
        # validated_date = {"date": "2020-9-12"}
        if "date" in request.query_params:
            date = request.query_params
            date_serializer = DateSerializer(data=date)
            if date_serializer.is_valid():
                validated_date = date_serializer.validated_data
                sql = "select \
                file.id, file.path, file.tag, file.description,file.activate, file.exist, file.savetime_total,\
                FileInfoDate.date, FileInfoDate.savetime\
                from FileInfo as file\
                left join FileInfo_has_Date as file_date on file.id = file_date.FileInfo_id\
                left join FileInfoDate on FileInfoDate.id = file_date.FileInfoDate_id\
                where FileInfoDate.date = '{}' limit 100"
                queryset = FileInfo.objects.raw(sql.format(validated_date["date"]))
                serializer = FileInfoWithDateSerializer(queryset, many=True)
                return Response(serializer.data)
        if "path_contains" in request.query_params:
            params = request.query_params
            params = DateSerializer(data=params)
            if params.is_valid():
                validated_params = params.validated_data
                queryset = FileInfo.objects.filter(path__contains=validated_params["path_contains"])
                serializer = FileInfoSerializer(queryset, many=True)
                return Response(serializer.data)
                # return Response({"code": codes.CODE_SUCCESS, "message": codes.MSG_SUCCESS, "data": "data"})
            return Response({"code": codes.CODE_SUCCESS, "message": codes.MSG_SUCCESS, "data": "data"})
        if "tag_contains" in request.query_params:
            params = request.query_params
            params = DateSerializer(data=params)
            if params.is_valid():
                validated_params = params.validated_data
                queryset = FileInfo.objects.filter(tag__contains=validated_params["tag_contains"])
                serializer = FileInfoSerializer(queryset, many=True)
                return Response(serializer.data)
                # return Response({"code": codes.CODE_SUCCESS, "message": codes.MSG_SUCCESS, "data": "data"})
            return Response({"code": codes.CODE_SUCCESS, "message": codes.MSG_SUCCESS, "data": "data"})
        if "begin_date" in request.query_params and "end_date" in request.query_params:
            params = request.query_params
            params = DateSerializer(data=params)
            if params.is_valid():
                validated_params = params.validated_data
                sql = "select \
                file.id, file.path, file.tag, file.description,file.activate, file.exist, file.savetime_total,\
                FileInfoDate.date, FileInfoDate.savetime\
                from FileInfo as file\
                left join FileInfo_has_Date as file_date on file.id = file_date.FileInfo_id\
                left join FileInfoDate on FileInfoDate.id = file_date.FileInfoDate_id\
                where FileInfoDate.date > '{}' and FileInfoDate.date < '{}' limit 100"
                queryset = FileInfo.objects.raw(
                    sql.format(validated_params["begin_date"], validated_params['end_date']))
                serializer = FileInfoWithDateSerializer(queryset, many=True)
                return Response(serializer.data)
        else:
            queryset = self.filter_queryset(self.get_queryset())

            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)

            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)

    def partial_update(self, request, *args, **kwargs):
        return Response({"code": codes.CODE_SUCCESS, "message": codes.MSG_SUCCESS, "data": "data"})

    @action(methods=['patch'], detail=True, url_path="increase", url_name="increase")
    def increase(self, request, pk=None):
        return Response({"code": codes.CODE_SUCCESS, "message": codes.MSG_SUCCESS, "data": "data"})

    # @action(methods=['patch'], detail=True, url_path="partial", url_name="partial_update")
    # def update_partial(self, request, pk=None):
    #    return Response({"code": codes.CODE_SUCCESS, "message": codes.MSG_SUCCESS, "data": "data"})

    @action(methods=['get'], detail=True, url_path="savetimes/sum", url_name="sum_savetimes")
    def sum_savetimes(self, request, pk=None):
        return Response({"code": codes.CODE_SUCCESS, "message": codes.MSG_SUCCESS, "data": "data"})

    @action(methods=['get'], detail=True, url_path="dates", url_name="dates")
    def dates(self, request, pk=None):
        return Response({"code": codes.CODE_SUCCESS, "message": codes.MSG_SUCCESS, "data": "data"})


# class FileGroupSet(viewsets.ModelViewSet):
class FileGroupSet(mixins.CreateModelMixin,
                   # mixins.RetrieveModelMixin,
                   # mixins.UpdateModelMixin,
                   # mixins.DestroyModelMixin,
                   mixins.ListModelMixin,
                   viewsets.GenericViewSet):
    """
    A viewset for viewing and editing user instances.
    """
    serializer_class = FileGroupSerializer
    queryset = FileGroup.objects.all()

    @action(methods=['post'], detail=True, url_path="search", url_name="search")
    def search(self, request, pk=None):
        """
        search_file_group
        """
        return Response({"code": codes.CODE_SUCCESS, "message": codes.MSG_SUCCESS, "data": "data"})


# class GroupSearchResultSet(viewsets.ModelViewSet):
class GroupSearchResultSet(mixins.CreateModelMixin,
                           mixins.RetrieveModelMixin,
                           # mixins.UpdateModelMixin,
                           # mixins.DestroyModelMixin,
                           mixins.ListModelMixin,
                           viewsets.GenericViewSet):
    """
    A viewset for viewing and editing user instances.
    """
    serializer_class = GroupSearchResultSerializer
    queryset = GroupSearchResult.objects.all()

    @action(methods=['post'], detail=False, url_path="search", url_name="search")
    def search(self, request):
        """
        search_in_all_search_results
        """
        return Response({"code": codes.CODE_SUCCESS, "message": codes.MSG_SUCCESS, "data": "data"})
# class FileInfoDateSet(viewsets.ModelViewSet):
#    """
#    A viewset for viewing and editing user instances.
#    """
#    serializer_class = FileInfoDateSerializer
#    queryset = FileInfoDate.objects.all()
#
#
# class FileInfoHasGroupSet(viewsets.ModelViewSet):
#    """
#    A viewset for viewing and editing user instances.
#    """
#    serializer_class = FileInfoHasGroupSerializer
#    queryset = FileInfoHasGroup.objects.all()
#
#
