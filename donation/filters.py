from .models import(
    Donation,
)

from CODE.filters import CODEDateFilter

class DonationFilter(CODEDateFilter):
    class Meta:
        model = Donation
        fields = {
            'name': ['exact', 'icontains'],
            'description': ['exact', 'icontains'],
            'amount': ['exact', 'icontains'],
            'department': ['exact', 'icontains'],
            'user': ['exact', 'icontains'],
        }


