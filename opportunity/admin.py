from django.contrib import admin
from opportunity.models import Opportunity, OpportunitySkill, OpportunityApplication

# Register your models here.
admin.site.register(Opportunity)
admin.site.register(OpportunitySkill)
admin.site.register(OpportunityApplication)