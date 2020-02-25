from django.contrib import admin
from . import models


@admin.register(models.Data)
class DataAdmin(admin.ModelAdmin):
    list_display = ['file_name', 'file_size', 'created', 'created_by', 'modified', 'modified_by']


@admin.register(models.Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(models.Score)
class ScoreAdmin(admin.ModelAdmin):
    list_display = ['tot_score']


@admin.register(models.Assets)
class AssetsAdmin(admin.ModelAdmin):
    list_display = ['get_data', 'get_account', 'tot']


@admin.register(models.Reserve)
class ReserveAdmin(admin.ModelAdmin):
    pass


@admin.register(models.ModifiedDuration)
class ModifiedDurationAdmin(admin.ModelAdmin):
    pass


@admin.register(models.HedgeRate)
class HedgeRateAdmin(admin.ModelAdmin):
    pass


@admin.register(models.DV)
class DVAdmin(admin.ModelAdmin):
    pass


@admin.register(models.CostReturn)
class CostReturnAdmin(admin.ModelAdmin):
    pass


@admin.register(models.CostReturnStressBase)
class CostReturnStressBaseAdmin(admin.ModelAdmin):
    pass


@admin.register(models.CostReturnStress1)
class CostReturnStress1StressBaseAdmin(admin.ModelAdmin):
    pass


@admin.register(models.CostReturnStress2)
class CostReturnStress2Admin(admin.ModelAdmin):
    pass


@admin.register(models.CostReturnStress3)
class CostReturnStress3Admin(admin.ModelAdmin):
    pass


@admin.register(models.CashFlowTest)
class CashFlowTestAdmin(admin.ModelAdmin):
    pass
