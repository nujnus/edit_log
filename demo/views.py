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

from django_celery_results.models import TaskResult

# @api_view(['GET'])
# @authentication_classes([JWTAuthentication])
# @permission_classes([IsAuthenticated])
# def test_auth_perm_api_view(request, format=None):
#     return Response({"code": code, "message": message, "data": data})


import demo.codes as codes
from rest_framework.exceptions import APIException


class EditLogExceptin(Exception):
    def __str__(self):
        return self.detail

class DBBroken(EditLogExceptin):
    def __init__(self, message=None, code=30001):
        self.detail = "数据库数据结构异常:{}".format(str(message))
        self.code = code

class IdUsed(EditLogExceptin):
    def __init__(self, id=None, code=30002):
        self.detail = "该id已被占用:{}".format(str(id))
        self.code = code

class ExecutionFailed(EditLogExceptin):
    def __init__(self, message=None, code=30003):
        self.detail = "任务执行失败:{}".format(str(message))
        self.code = code

from rest_framework.response import Response
class APIResponse(Response):
    def __init__(self, data=None, code=0, detail='success', **kwargs):
        dic = {'code': code, 'detail': detail}
        if data:
            dic = {'code': code, 'detail': detail, 'data': data}
        super().__init__(data=dic, **kwargs)


from django.db import connection, transaction
from django.db import transaction

from rest_framework.exceptions import *


# @transaction.atomic()
@api_view(['GET'])
def special_case_2003(request, format=None):
    data = 123
    print(123)
    # try:
    # with transaction.atomic():
    cursor = connection.cursor()
    s1 = transaction.savepoint()  # 可以设置多个保存点
    cursor.execute('update FileInfo set tag = "KncQeaRabUEacHLImhACaQWSJJJ666999" WHERE id = 3')
    # transaction.savepoint_commit(s1)  #在with中没用, 在@transaction.atomic()中有用.
    # transaction.commit()

    # raise ParseError()
    #raise TypeError()
    #raise DBBroken(message="测试")
    #raise IdUsed(id=123)
    raise ExecutionFailed(message="job name: 123")

    # transaction.commit()
    # except Exception as e:
    #  transaction.savepoint_rollback(s1)  #在raise e之前, 就又触发了异常.
    #  #transaction.rollback()
    #  raise e

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
    GroupSearchResultSerializer, FileInfoDateSerializer, FileInfoWithDateSerializer, DateSerializer, \
    FileInfoWithMaxMinDateSerializer

#
#
from rest_framework import generics, mixins, views
from demo import permissions

import time


def timeit(f):
    def timed(*args, **kw):
        ts = time.time()
        result = f(*args, **kw)
        te = time.time()
        print('func:%r args:[%r, %r] took: %2.4f sec' % (f.__name__, args, kw, te - ts))
        return result

    return timed


# class FileInfoSet(viewsets.ModelViewSet):
class FileInfoSet(mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  # mixins.DestroyModelMixin,
                  # mixins.ListModelMixin,
                  viewsets.GenericViewSet):
    """
    A viewset for viewing and editing user instances.
    """
    serializer_class = FileInfoSerializer
    queryset = FileInfo.objects.all()
    authentication_classes = [JWTAuthentication, ]
    permission_classes = [permissions.BlocklistPermission, ]

    @timeit
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
            if date_serializer.is_valid(raise_exception=True):
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
                return APIResponse(serializer.data)
        if "path_contains" in request.query_params:
            params = request.query_params
            params = DateSerializer(data=params)
            if params.is_valid():
                validated_params = params.validated_data
                queryset = FileInfo.objects.filter(path__contains=validated_params["path_contains"])
                serializer = FileInfoSerializer(queryset, many=True)
                return APIResponse(serializer.data)
                # return Response({"code": codes.CODE_SUCCESS, "message": codes.MSG_SUCCESS, "data": "data"})
            #return Response({"code": codes.CODE_SUCCESS, "message": codes.MSG_SUCCESS, "data": "data"})
            return APIResponse("serializer.data")
        if "tag_contains" in request.query_params:
            params = request.query_params
            params = DateSerializer(data=params)
            if params.is_valid():
                validated_params = params.validated_data
                queryset = FileInfo.objects.filter(tag__contains=validated_params["tag_contains"])
                serializer = FileInfoSerializer(queryset, many=True)
                return Response(serializer.data)
                # return Response({"code": codes.CODE_SUCCESS, "message": codes.MSG_SUCCESS, "data": "data"})
            #return Response({"code": codes.CODE_SUCCESS, "message": codes.MSG_SUCCESS, "data": "data"})
            return APIResponse("serializer.data")
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
                #return Response(serializer.data)
                return APIResponse(serializer.data)
        else:
            queryset = self.filter_queryset(self.get_queryset())

            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)

            serializer = self.get_serializer(queryset, many=True)
            #return Response(serializer.data)
            return APIResponse(serializer.data)

    def partial_update(self, request, *args, **kwargs):
        print(request.data)
        #return Response({"code": codes.CODE_SUCCESS, "message": codes.MSG_SUCCESS, "data": "data"})
        return APIResponse("serializer.data")

    @action(methods=['patch'], detail=True, url_path="increase", url_name="increase")
    def increase(self, request, pk=None):
        f_h_ds = FileInfo_has_Date.objects.filter(FileInfo_id=pk)
        assert len(f_h_ds) > 0, "没有对应的pk, 或没有对应的时间"

        # if f_h_ds == 0: 创建对应记录.
        list_of_file_info_date = [
            FileInfoDate.objects.get(id=f_h_d.FileInfoDate_id)
            for f_h_d in f_h_ds
        ]

        # 必要时创建记录.
        import datetime
        date_ids = [f_h_d.FileInfoDate_id for f_h_d in FileInfo_has_Date.objects.filter(FileInfo_id=pk)]
        queryset = FileInfoDate.objects.filter(id__in=date_ids).filter(date=datetime.date(2020, 2, 23))
        q = queryset[0]
        q.savetime += 1
        q.save()

        # print(type(list_of_file_info_date[0].date))
        # datetime.date(2020,2,23)
        # list_of_file_info_date = [fd for fd in list_of_file_info_date if fd.date == datetime.date(2020, 2, 23)]
        # for file_info_date in list_of_file_info_date:
        #    file_info_date.savetime += 1
        #    file_info_date.save()
        serializer = FileInfoDateSerializer(q)
        #return Response({"code": codes.CODE_SUCCESS, "message": codes.MSG_SUCCESS, "data": serializer.data})
        return APIResponse(serializer.data)
        # return Response({"code": codes.CODE_SUCCESS, "message": codes.MSG_SUCCESS, "data": "data"})

    # @action(methods=['patch'], detail=True, url_path="partial", url_name="partial_update")
    # def update_partial(self, request, pk=None):
    #    return Response({"code": codes.CODE_SUCCESS, "message": codes.MSG_SUCCESS, "data": "data"})

    # ----groupby------------------------
    @action(methods=['get'], detail=True, url_path="savetimes/sum", url_name="sum_savetimes")
    def sum_savetimes(self, request, pk=None):
        """
        statistics_a_file_all_edit_time_orderby, {"sum_edit": True}),
        """
        sql = "select \
        file.id, file.path, file.tag, file.description,file.activate, file.exist, file.savetime_total,\
        FileInfoDate.date, FileInfoDate.savetime\
        from FileInfo as file\
        left join FileInfo_has_Date as file_date on file.id = file_date.FileInfo_id\
        left join FileInfoDate on FileInfoDate.id = file_date.FileInfoDate_id\
        where FileInfoDate.date > '{}' and FileInfoDate.date < '{}' limit 100"

        #return Response({"code": codes.CODE_SUCCESS, "message": codes.MSG_SUCCESS, "data": "data"})
        return APIResponse("data")

    @action(methods=['get'], detail=True, url_path="dates", url_name="dates")
    def dates(self, request, pk=None):
        """
        statistics_a_file_all_date, {"statistics_date": True}),
        """
        self.check_object_permissions(request, pk)
        sql = "select \
        file.id, \
        max(FileInfoDate.date) as max_date, min(FileInfoDate.date) as min_date\
        from FileInfo as file \
        left join FileInfo_has_Date as file_date on file.id = file_date.FileInfo_id \
        left join FileInfoDate on FileInfoDate.id = file_date.FileInfoDate_id \
        where file.id = {} \
        group by file.id "

        queryset = FileInfo.objects.raw(sql.format(pk))
        serializer = FileInfoWithMaxMinDateSerializer(queryset, many=True)
        #return Response(serializer.data)
        # return Response({"code": codes.CODE_SUCCESS, "message": codes.MSG_SUCCESS, "data": "data"})
        return APIResponse(serializer.data)


from demo import tasks


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
        res = tasks.add.delay(1, 3)
        #return Response({"code": codes.CODE_SUCCESS, "message": codes.MSG_SUCCESS, "data": res.task_id})
        return APIResponse(data)


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
        data = list(TaskResult.objects.filter(task_id=request.data["task_id"]).values())
        return APIResponse(data)
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
