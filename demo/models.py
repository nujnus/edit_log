from django.db import models

#class ModelDemo(models.Model):
#    b = models.IntegerField()
#    b2 = models.BigIntegerField()
#    b3 = models.PositiveIntegerField()
#    b4 = models.IntegerField()
#    b5 = models.BooleanField()
#    b6 = models.NullBooleanField()
#    b7 = models.FloatField()
#    b8 = models.DecimalField(max_digits=5, decimal_places=2)
#    b9 = models.CharField(max_length=100)
#    b10 = models.TextField()
#    b11 = models.URLField()
#    b12 = models.UUIDField()
#    b13 = models.DateField()
#    b14 = models.DateTimeField()
#    b15 = models.DurationField()
#    b16 = models.TimeField()
#    b17 = models.EmailField()
#    b18 = models.FileField()
#    b19 = models.FilePathField()
#    b20 = models.ImageField()
#    b21 = models.GenericIPAddressField()
#    b22 = models.BinaryField()
#    b23 = models.SlugField()

class FileInfo(models.Model):
   path = models.FilePathField(unique=True, max_length=200)
   tag = models.TextField()
   description = models.TextField(default="")
   activate = models.BooleanField()
   exist = models.BooleanField()
   savetime_total = models.PositiveIntegerField(default=0)
   class Meta:
       db_table = 'FileInfo'

class FileInfo_has_Date(models.Model):
    FileInfo_id = models.IntegerField()
    FileInfoDate_id = models.IntegerField()

    class Meta:
        db_table = 'FileInfo_has_Date'

class FileInfoDate(models.Model):
   date = models.DateField()
   savetime = models.PositiveIntegerField(default=0)

   class Meta:
       db_table = 'FileInfoDate'

class FileInfoHasGroup(models.Model):
    FileInfo_id = models.IntegerField()
    FileGroup_id = models.IntegerField()
    class Meta:
        unique_together = (("FileInfo_id", "FileGroup_id"),)
        db_table = 'FileInfoHasGroup'

class FileGroup(models.Model):
   name = models.CharField(max_length=200, unique=True)
   create_datetime = models.DateTimeField()
   description = models.TextField()

   class Meta:
       db_table = 'FileGroup'

class GroupSearchResult(models.Model):
   search_keyword =  models.CharField(max_length=200, default="")
   group_search_result_log = models.FilePathField(unique=True, max_length=200)
   group_id = models.IntegerField()
   exsit = models.BooleanField()
   timestamp = models.DateTimeField()

   class Meta:
       db_table = 'GroupSearchResult'

#FileInfo.objects.all()
