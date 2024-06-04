from django.contrib import admin
from . models import PlacedBet, UserStats, Results, FinisedBet

admin.site.register(PlacedBet)
admin.site.register(UserStats)
admin.site.register(Results)
admin.site.register(FinisedBet)