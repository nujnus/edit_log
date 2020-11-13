from rest_framework.views import exception_handler as drf_exception_handler
from rest_framework.views import set_rollback
from rest_framework.response import Response
from rest_framework import status
import traceback
import sys
import logging
import demo.codes as codes

from demo.views import EditLogExceptin

import uuid

logger = logging.getLogger('django')


def exception_handler(exc, context):
    print('---exception_handler---')

    response = drf_exception_handler(exc, context)
    # detail = '%s - %s - %s' % (context.get('view'), context.get('request').method, exc)
    detail = '%s - %s' % (context.get('request').method, exc)  # 请求类型 和 错误信息 都打印一遍.

    # set_rollback()  #只用作返回值, 和日志, 不用作
    logid = uuid.uuid4().hex
    if not response:  # 服务端错误
        if isinstance(exc, EditLogExceptin):
            response = Response({'detail': "[{}] - {}".format(logid, detail), 'code': exc.code,
                                 'data': {}}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            response = Response({'detail': "[{}] - {}".format(logid, detail), 'code': 10500}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        response.data = {'detail': "[{}] - {}".format(logid, detail), 'code': 20500, 'data': {}}
        #response.data["code"] = 20500#{'detail': "[{}] - {}".format(logid, detail), 'code': 20500, 'data': {}}

    logger.critical("uuid: [{}], traceback:{}".format(logid, str(traceback.format_exc())))  # 感觉应该记录异常id
    print(response)

    return response
