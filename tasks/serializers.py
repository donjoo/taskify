from rest_framework import serializers
from .models import Task

class TaskSerializer(serializers.ModelSerializer):
    assigned_to_username = serializers.CharField(source='assigned_to.username', read_only=True)
    class Meta:
        model = Task
        fields = ['id','title','description','assigned_to','assigned_to_username','due_date','status','completion_report','worked_hours','created_at','updated_at']
        read_only_fields = ['id','created_at','updated_at','assigned_to_username']

class TaskStatusUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['status','completion_report','worked_hours']

    def validate(self, attrs):
        status = attrs.get('status', None)
        if status == 'completed':
            if not attrs.get('completion_report'):
                raise serializers.ValidationError({'completion_report': 'Required when marking completed.'})
            if attrs.get('worked_hours') is None:
                raise serializers.ValidationError({'worked_hours': 'Required when marking completed.'})
        return attrs
