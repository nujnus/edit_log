from rest_framework import serializers
from .models import FileInfo

from django.conf import settings
TARGET_FILE_DIRECTORY = settings.TARGET_FILE_DIRECTORY
#TARGET_FILE_DIRECTORY

#||class FileInfoSerializer(serializers.ModelSerializer):
#||   #path = serializers.FilePathField(TARGET_FILE_DIRECTORY)
#||   path = serializers.FilePathField("/tmp")
#||   class Meta:
#||       model = FileInfo
#||       fields = '__all__'
#||       #exclude = [ 'path' ]
#||
#||
#||#fis= FileInfoSerializer(data={"path" : "NetpasHelper.log"})
#||
#||fis= FileInfoSerializer(data={"path" : "/tmp/NetpasHelper.log", "tag" : "iadasasda", "activate": True, "exist": True})
#||
#||list(filter(lambda x:'error' in x, dir(fis)))
#||
#||#----------------------------------
#||from demo.serializers import *
#||#fis.is_valid(raise_exception=True)
#||fis.is_valid()
#||#dir(fis).find("error")
#||fis._errors
#||#fis.error()
#||#fis.save()
#||#            except ValidationError as exc:
#||#{'path': [ErrorDetail(string='"NetpasHelper.log" is not a valid path choice.', code='invalid_choice')],
#||# 'tag': [ErrorDetail(string='This field is required.', code='required')],
#||# 'activate': [ErrorDetail(string='This field is required.', code='required')],
#||# 'exist': [ErrorDetail(string='This field is required.', code='required')]}
#||
#||
#||
#||#----------------------------------
#||#输入url, parser分析.
#||#----------------------------------
#||#to_repr

from demo.models import FileInfo, FileInfo_has_Date, FileInfoDate, FileInfoHasGroup, FileGroup, GroupSearchResult
from django.conf import settings
TARGET_FILE_DIRECTORY = settings.TARGET_FILE_DIRECTORY
print(TARGET_FILE_DIRECTORY)
class FileInfoSerializer(serializers.ModelSerializer):
   path = serializers.FilePathField(TARGET_FILE_DIRECTORY)
   class Meta:
       model = FileInfo
       fields = '__all__'
       #exclude = [ 'path' ]


class FileInfoDateSerializer(serializers.ModelSerializer):
   class Meta:
       model = FileInfoDate
       fields = '__all__'

class FileInfoHasGroupSerializer(serializers.ModelSerializer):
   class Meta:
       model = FileInfoHasGroup
       fields = '__all__'

class FileGroupSerializer(serializers.ModelSerializer):
   class Meta:
       model = FileGroup
       fields = '__all__'

class GroupSearchResultSerializer(serializers.ModelSerializer):
   group_search_result_log = serializers.FilePathField(TARGET_FILE_DIRECTORY)
   class Meta:
       model = GroupSearchResult
       fields = '__all__'
       #exclude = [ 'group_search_result_log' ]
