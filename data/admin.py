from django.contrib import admin
from . import models


@admin.register(models.Data)
class DataAdmin(admin.ModelAdmin):
    list_display = ['file_name', 'file_size', 'created', 'created_by', 'modified', 'modified_by']
    list_filter = ['file_name']


@admin.register(models.Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(models.Score)
class ScoreAdmin(admin.ModelAdmin):
    list_display = ['data', 'tot_score', 'dur_gap_l_scaled', 'dur_gap_a_scaled', 'hedge_rate', 'dv', 'cost_retrun',
                    'cost_return_stress', 'cash_flow_test_base', 'cash_flow_test_stress', 'liquidity']
    list_filter = ['data']


class BaseAdmin(admin.ModelAdmin):
    list_filter = ['data', 'account']
    ordering = ['data']


@admin.register(models.Assets)
class AssetsAdmin(BaseAdmin):
    list_display = ['data', 'account', 'tot', 'cash', 'fixed_income', 'equity', 'loan']


@admin.register(models.Reserve)
class ReserveAdmin(BaseAdmin):
    list_display = ['data', 'account', 'reserve']


@admin.register(models.ModifiedDuration)
class ModifiedDurationAdmin(BaseAdmin):
    list_display = ['data', 'account', 'gap_l_scaled', 'l_in', 'l_out', 'a', 'gap_a_scaled']


@admin.register(models.HedgeRate)
class HedgeRateAdmin(BaseAdmin):
    list_display = ['data', 'account', 'l_sensitivity', 'hedge_rate']


@admin.register(models.DV)
class DVAdmin(BaseAdmin):
    list_display = ['data', 'account', 'dv']


@admin.register(models.CostReturn)
class CostReturnAdmin(BaseAdmin):
    list_display = ['data', 'account', 'comp_gap', 'fin_gap', 'ra_comp_gap', 'avg_3y_gap']


@admin.register(models.CostReturnStressBase)
class CostReturnStressBaseAdmin(BaseAdmin):
    list_display = ['data', 'account', 'gap_y1', 'gap_y2', 'gap_y3']


@admin.register(models.CostReturnStress1)
class CostReturnStress1StressBaseAdmin(BaseAdmin):
    list_display = ['data', 'account', 'loss_rate', 'gap']


@admin.register(models.CostReturnStress2)
class CostReturnStress2Admin(BaseAdmin):
    list_display = ['data', 'account', 'gap_y1', 'gap_y2', 'gap_y3']


@admin.register(models.CostReturnStress3)
class CostReturnStress3Admin(BaseAdmin):
    list_display = ['data', 'account', 'gap_y1', 'gap_y2', 'gap_y3']


@admin.register(models.CashFlowTest)
class CashFlowTestAdmin(BaseAdmin):
    list_display = ['data', 'account', 'cf_accumulated_q1_base', 'cf_accumulated_q2_base', 'cf_accumulated_q3_base',
                    'cf_accumulated_q4_base', 'cf_accumulated_y2_base', 'cf_accumulated_y3_base',
                    'cf_accumulated_q1_stress', 'cf_accumulated_q2_stress', 'cf_accumulated_q3_stress',
                    'cf_accumulated_q4_stress', 'cf_accumulated_y2_stress', 'cf_accumulated_y3_stress']
