#from app_demo_2EC6E023F4.models import Record
#from app_demo_2EC6E023F4.serializers import RecordsRequestSerializer
#
#
#class RecordsPermission(object):
#    def has_permission(self, request, view):
#        rqs = RecordsRequestSerializer(data=request.query_params)
#        if rqs.is_valid():
#            start_date = rqs.validated_data['start']
#            record = Record.objects.get(date=start_date)
#            user = request.user
#            if user.has_perm('app_demo_2EC6E023F4.view_record') or user.has_perm('app_demo_2EC6E023F4.view_record',
#                                                                                 record):
#                # if request.user.has_perm('app_demo_2EC6E023F4.add_record'):
#                return True

from rest_framework import permissions
class BlocklistPermission(permissions.BasePermission):
    """
    Global permission check for blocked IPs.
    """
    def has_permission(self, request, view):
        print("has_permission:{},{}".format(str(request), str(view)))
        #ip_addr = request.META['REMOTE_ADDR']
        #blocked = Blocklist.objects.filter(ip_addr=ip_addr).exists()
        #return not blocked
        return True

    def has_object_permission(self, request, view, obj):
        print("has_object_permission:{},{},{}".format(str(request), str(view), str(obj)))
        return True
