from .models import Connection
from CODE.filters import CODEDateFilter


class ConnectionFilter(CODEDateFilter):
    class Meta:
        model = Connection
        fields = {
            'createdAt': ['exact'],
            'updatedAt': ['exact'],
            'status': ['exact'],
            'userA': ['exact'],
            'userB': ['exact'],
        }
