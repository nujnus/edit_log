from app_demo_2EC6E023F4.models import Record
from app_demo_2EC6E023F4.serializers import RecordsRequestSerializer

class RecordsPermission(object):
    def has_permission(self, request, view):
        rqs = RecordsRequestSerializer(data=request.query_params)
        if rqs.is_valid():
            start_date = rqs.validated_data['start']
            record = Record.objects.get(date=start_date)
            user = request.user
            if user.has_perm('app_demo_2EC6E023F4.view_record') or user.has_perm('app_demo_2EC6E023F4.view_record',
                                                                                 record):
                # if request.user.has_perm('app_demo_2EC6E023F4.add_record'):
                return True