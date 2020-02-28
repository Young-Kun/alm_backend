from rest_framework import serializers
from data import models


class ScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Score
        fields = ['data', 'tot_score', 'dur_score', 'cost_return_score', 'cash_flow_score', 'dur_gap_l_scaled',
                  'dur_gap_a_scaled', 'hedge_rate', 'dv', 'avg_3y_gap', 'comp_gap', 'ra_comp_gap', 'fin_gap',
                  'short_gap', 'gap_stress1', 'gap_stress2', 'gap_stress3', 'cash_flow_test_base',
                  'cash_flow_test_stress', 'liquidity']


class AssetsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Assets
        fields = ['data', 'account', 'tot', 'cash', 'fixed_income', 'equity', 'loan']


class ReserveSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Reserve
        fields = ['data', 'account', 'reserve']
