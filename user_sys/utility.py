from rest_framework.views import exception_handler as drf_exception_handler
from rest_framework.response import Response
from rest_framework import status
import traceback
import sys
import logging
import app_demo_2EC6E023F4.codes as codes
logger = logging.getLogger('django')

def exception_handler(exc, context):
    print('---exception_handler---')
    response = drf_exception_handler(exc, context)
    #detail = '%s - %s - %s' % (context.get('view'), context.get('request').method, exc)
    detail = '%s - %s' % (context.get('request').method, exc)
    if not response:  # 服务端错误
        response =  Response({'detail': detail}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        response.data = {'detail': detail, 'code' : codes.CODE_AUTH_ERROR, 'data': {}}

    logger.critical("traceback:{}".format(str(traceback.format_exc())))
    print(response)
    return response