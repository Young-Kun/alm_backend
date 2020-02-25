from django.db import models

from alm_backend.settings import REPORTS_PATH, ACCOUNTS
from custom.precision import HUNDRED, PERCENT, BILLION


class Data(models.Model):
    file_name = models.CharField(max_length=6, primary_key=True, verbose_name='文件名')
    file = models.FileField(upload_to=REPORTS_PATH, max_length=255, unique=True, verbose_name='量化评估表')
    file_size = models.IntegerField(default=0, editable=False, verbose_name='文件大小')
    created = models.DateTimeField(auto_now_add=True, verbose_name='首次上传')
    created_by = models.CharField(max_length=150, editable=False, verbose_name='上传人')
    modified = models.DateTimeField(auto_now=True, verbose_name='最后修改')
    modified_by = models.CharField(max_length=150, editable=False, verbose_name='修改人')

    class Meta:
        ordering = ['-file_name']
        verbose_name_plural = verbose_name = '源数据'


class Account(models.Model):
    name = models.CharField(max_length=1, primary_key=True, choices=ACCOUNTS, verbose_name='账户名称')

    class Meta:
        verbose_name_plural = verbose_name = '账户'


# 得分
class Score(models.Model):
    data = models.OneToOneField('Data', on_delete=models.CASCADE, verbose_name='数据源')
    dur_gap_l_scaled = models.IntegerField(verbose_name='规模调整后的修正久期缺口得分')
    dur_gap_a_scaled = models.IntegerField(verbose_name='资产调整后的期限缺口得分')
    hedge_rate = models.IntegerField(verbose_name='利率风险对冲率得分')
    dv = models.IntegerField(verbose_name='基点价值变动率得分')
    cost_retrun = models.IntegerField(verbose_name='成本收益匹配状况得分')
    cost_return_stress = models.IntegerField(verbose_name='成本收益匹配压力测试得分')
    cash_flow_test_base = models.IntegerField(verbose_name='现金流测试得分')
    cash_flow_test_stress = models.IntegerField(verbose_name='现金流压力测试得分')
    liquidity = models.IntegerField(verbose_name='流动性指标得分')
    tot_score = models.IntegerField(verbose_name='总分')

    class Meta:
        verbose_name_plural = verbose_name = '得分情况'


# 分账户的指标模型基类
class FieldBaseModel(models.Model):
    data = models.ForeignKey('Data', on_delete=models.CASCADE, verbose_name='数据源')
    account = models.ForeignKey('Account', on_delete=models.CASCADE, verbose_name='账户')

    class Meta:
        abstract = True

    def get_data(self):
        return self.data.file_name

    def get_account(self):
        return self.account.name


# 资产大类
class Assets(FieldBaseModel):
    tot = models.DecimalField(**BILLION, verbose_name='期末资金运用净额')
    cash = models.DecimalField(**BILLION, verbose_name='现金及流动性管理工具')
    fixed_income = models.DecimalField(**BILLION, verbose_name='固定收益类投资资产')
    equity = models.DecimalField(**BILLION, verbose_name='权益类投资资产')
    loan = models.DecimalField(**BILLION, verbose_name='保单贷款')

    class Meta:
        verbose_name_plural = verbose_name = '资产净额'


# 会计准备金
class Reserve(FieldBaseModel):
    reserve = models.DecimalField(**BILLION, verbose_name='会计准备金')

    class Meta:
        verbose_name_plural = verbose_name = '会计准备金'


# 修正久期
class ModifiedDuration(FieldBaseModel):
    l_in = models.DecimalField(**HUNDRED, verbose_name='负债现金流入修正久期')
    l_out = models.DecimalField(**HUNDRED, verbose_name='负债现金流出修正久期')
    a = models.DecimalField(**HUNDRED, verbose_name='资产修正久期')
    gap_l_scaled = models.DecimalField(**HUNDRED, verbose_name='规模调整后的修正久期缺口')
    gap_a_scaled = models.DecimalField(**HUNDRED, verbose_name='资产调整后的期限缺口')

    class Meta:
        verbose_name_plural = verbose_name = '修正久期'


# 利率风险对冲率
class HedgeRate(FieldBaseModel):
    l_sensitivity = models.DecimalField(**PERCENT, verbose_name='利率风险负债敏感度')
    hedge_rate = models.DecimalField(**PERCENT, verbose_name='利率风险对冲率')

    class Meta:
        verbose_name_plural = verbose_name = '利率风险对冲率'


# 基点价值变动率
class DV(FieldBaseModel):
    dv = models.DecimalField(**PERCENT, verbose_name='基点价值变动率')

    class Meta:
        verbose_name_plural = verbose_name = '基点价值变动率'


# 成本收益匹配
class CostReturn(FieldBaseModel):
    eff_cost = models.DecimalField(**PERCENT, verbose_name='有效成本率')
    capital_cost = models.DecimalField(**PERCENT, verbose_name='资金成本率')
    gre_cost = models.DecimalField(**PERCENT, verbose_name='保证成本率')
    avg_3y_cost = models.DecimalField(**PERCENT, verbose_name='三年平均资金成本率')
    comp_return = models.DecimalField(**PERCENT, verbose_name='年化综合投资收益率')
    fin_return = models.DecimalField(**PERCENT, verbose_name='年化会计投资收益率')
    ra_comp_return = models.DecimalField(**PERCENT, verbose_name='风险调整后综合投资收益率')
    avg_3y_return = models.DecimalField(**PERCENT, verbose_name='三年平均年化综合投资收益率')

    class Meta:
        verbose_name_plural = verbose_name = '成本收益匹配'


# 成本收益压力测试 基本情景
class CostReturnStressBase(FieldBaseModel):
    fin_return_y1 = models.DecimalField(**PERCENT, verbose_name='第一年会计收益率')
    fin_return_y2 = models.DecimalField(**PERCENT, verbose_name='第二年会计收益率')
    fin_return_y3 = models.DecimalField(**PERCENT, verbose_name='第三年会计收益率')
    capital_cost_y1 = models.DecimalField(**PERCENT, verbose_name='第一年资金成本率')
    capital_cost_y2 = models.DecimalField(**PERCENT, verbose_name='第二年资金成本率')
    capital_cost_y3 = models.DecimalField(**PERCENT, verbose_name='第三年资金成本率')
    gap_y1 = models.DecimalField(**PERCENT, verbose_name='第一年差额')
    gap_y2 = models.DecimalField(**PERCENT, verbose_name='第二年差额')
    gap_y3 = models.DecimalField(**PERCENT, verbose_name='第三年差额')

    class Meta:
        verbose_name_plural = verbose_name = '成本收益压力测试 基本情景'


# 成本收益压力测试 压力一
class CostReturnStress1(FieldBaseModel):
    loss_rate = models.DecimalField(**PERCENT, verbose_name='投资资产损失率')
    gap = models.DecimalField(**PERCENT, verbose_name='压力后差额一')

    class Meta:
        verbose_name_plural = verbose_name = '成本收益压力测试 压力一'


# 成本收益压力测试 压力二
class CostReturnStress2(FieldBaseModel):
    fin_return_y1 = models.DecimalField(**PERCENT, verbose_name='第一年会计收益率')
    fin_return_y2 = models.DecimalField(**PERCENT, verbose_name='第二年会计收益率')
    fin_return_y3 = models.DecimalField(**PERCENT, verbose_name='第三年会计收益率')
    gre_cost_y1 = models.DecimalField(**PERCENT, verbose_name='第一年保证成本率')
    gre_cost_y2 = models.DecimalField(**PERCENT, verbose_name='第二年保证成本率')
    gre_cost_y3 = models.DecimalField(**PERCENT, verbose_name='第三年保证成本率')
    gap_y1 = models.DecimalField(**PERCENT, verbose_name='第一年差额')
    gap_y2 = models.DecimalField(**PERCENT, verbose_name='第二年差额')
    gap_y3 = models.DecimalField(**PERCENT, verbose_name='第三年差额')

    class Meta:
        verbose_name_plural = verbose_name = '成本收益压力测试 压力二'


# 成本收益压力测试 压力三
class CostReturnStress3(FieldBaseModel):
    fin_return_y1 = models.DecimalField(**PERCENT, verbose_name='第一年会计收益率')
    fin_return_y2 = models.DecimalField(**PERCENT, verbose_name='第二年会计收益率')
    fin_return_y3 = models.DecimalField(**PERCENT, verbose_name='第三年会计收益率')
    capital_cost_y1 = models.DecimalField(**PERCENT, verbose_name='第一年资金成本率')
    capital_cost_y2 = models.DecimalField(**PERCENT, verbose_name='第二年资金成本率')
    capital_cost_y3 = models.DecimalField(**PERCENT, verbose_name='第三年资金成本率')
    gap_y1 = models.DecimalField(**PERCENT, verbose_name='第一年差额')
    gap_y2 = models.DecimalField(**PERCENT, verbose_name='第二年差额')
    gap_y3 = models.DecimalField(**PERCENT, verbose_name='第三年差额')

    class Meta:
        verbose_name_plural = verbose_name = '成本收益压力测试 压力三'


# 现金流压力测试
class CashFlowTest(FieldBaseModel):
    cf_business_q1_base = models.DecimalField(**BILLION, verbose_name='基本情景未来第一季度业务现金流')
    cf_business_q2_base = models.DecimalField(**BILLION, verbose_name='基本情景未来第二季度业务现金流')
    cf_business_q3_base = models.DecimalField(**BILLION, verbose_name='基本情景未来第三季度业务现金流')
    cf_business_q4_base = models.DecimalField(**BILLION, verbose_name='基本情景未来第四季度业务现金流')
    cf_business_y2_base = models.DecimalField(**BILLION, verbose_name='基本情景未来第二年业务现金流')
    cf_business_y3_base = models.DecimalField(**BILLION, verbose_name='基本情景未来第三年业务现金流')

    cf_business_q1_stress = models.DecimalField(**BILLION, verbose_name='压力情景未来第一季度业务现金流')
    cf_business_q2_stress = models.DecimalField(**BILLION, verbose_name='压力情景未来第二季度业务现金流')
    cf_business_q3_stress = models.DecimalField(**BILLION, verbose_name='压力情景未来第三季度业务现金流')
    cf_business_q4_stress = models.DecimalField(**BILLION, verbose_name='压力情景未来第四季度业务现金流')
    cf_business_y2_stress = models.DecimalField(**BILLION, verbose_name='压力情景未来第二年业务现金流')
    cf_business_y3_stress = models.DecimalField(**BILLION, verbose_name='压力情景未来第三年业务现金流')

    cf_assets_q1_base = models.DecimalField(**BILLION, verbose_name='基本情景未来第一季度资产现金流')
    cf_assets_q2_base = models.DecimalField(**BILLION, verbose_name='基本情景未来第二季度资产现金流')
    cf_assets_q3_base = models.DecimalField(**BILLION, verbose_name='基本情景未来第三季度资产现金流')
    cf_assets_q4_base = models.DecimalField(**BILLION, verbose_name='基本情景未来第四季度资产现金流')
    cf_assets_y2_base = models.DecimalField(**BILLION, verbose_name='基本情景未来第二年资产现金流')
    cf_assets_y3_base = models.DecimalField(**BILLION, verbose_name='基本情景未来第三年资产现金流')

    cf_assets_q1_stress = models.DecimalField(**BILLION, verbose_name='压力情景未来第一季度资产现金流')
    cf_assets_q2_stress = models.DecimalField(**BILLION, verbose_name='压力情景未来第二季度资产现金流')
    cf_assets_q3_stress = models.DecimalField(**BILLION, verbose_name='压力情景未来第三季度资产现金流')
    cf_assets_q4_stress = models.DecimalField(**BILLION, verbose_name='压力情景未来第四季度资产现金流')
    cf_assets_y2_stress = models.DecimalField(**BILLION, verbose_name='压力情景未来第二年资产现金流')
    cf_assets_y3_stress = models.DecimalField(**BILLION, verbose_name='压力情景未来第三年资产现金流')

    cf_financing_q1_base = models.DecimalField(**BILLION, verbose_name='基本情景未来第一季度筹资现金流')
    cf_financing_q2_base = models.DecimalField(**BILLION, verbose_name='基本情景未来第二季度筹资现金流')
    cf_financing_q3_base = models.DecimalField(**BILLION, verbose_name='基本情景未来第三季度筹资现金流')
    cf_financing_q4_base = models.DecimalField(**BILLION, verbose_name='基本情景未来第四季度筹资现金流')
    cf_financing_y2_base = models.DecimalField(**BILLION, verbose_name='基本情景未来第二年筹资现金流')
    cf_financing_y3_base = models.DecimalField(**BILLION, verbose_name='基本情景未来第三年筹资现金流')

    cf_financing_q1_stress = models.DecimalField(**BILLION, verbose_name='压力情景未来第一季度筹资现金流')
    cf_financing_q2_stress = models.DecimalField(**BILLION, verbose_name='压力情景未来第二季度筹资现金流')
    cf_financing_q3_stress = models.DecimalField(**BILLION, verbose_name='压力情景未来第三季度筹资现金流')
    cf_financing_q4_stress = models.DecimalField(**BILLION, verbose_name='压力情景未来第四季度筹资现金流')
    cf_financing_y2_stress = models.DecimalField(**BILLION, verbose_name='压力情景未来第二年筹资现金流')
    cf_financing_y3_stress = models.DecimalField(**BILLION, verbose_name='压力情景未来第三年筹资现金流')

    cf_net_q1_base = models.DecimalField(**BILLION, verbose_name='基本情景未来第一季度净现金流')
    cf_net_q2_base = models.DecimalField(**BILLION, verbose_name='基本情景未来第二季度净现金流')
    cf_net_q3_base = models.DecimalField(**BILLION, verbose_name='基本情景未来第三季度净现金流')
    cf_net_q4_base = models.DecimalField(**BILLION, verbose_name='基本情景未来第四季度净现金流')
    cf_net_y2_base = models.DecimalField(**BILLION, verbose_name='基本情景未来第二年净现金流')
    cf_net_y3_base = models.DecimalField(**BILLION, verbose_name='基本情景未来第三年净现金流')

    cf_net_q1_stress = models.DecimalField(**BILLION, verbose_name='压力情景未来第一季度净现金流')
    cf_net_q2_stress = models.DecimalField(**BILLION, verbose_name='压力情景未来第二季度净现金流')
    cf_net_q3_stress = models.DecimalField(**BILLION, verbose_name='压力情景未来第三季度净现金流')
    cf_net_q4_stress = models.DecimalField(**BILLION, verbose_name='压力情景未来第四季度净现金流')
    cf_net_y2_stress = models.DecimalField(**BILLION, verbose_name='压力情景未来第二年净现金流')
    cf_net_y3_stress = models.DecimalField(**BILLION, verbose_name='压力情景未来第三年净现金流')

    cf_accumulated_q1_base = models.DecimalField(**BILLION, verbose_name='基本情景未来第一季度累计现金及流动性管理工具')
    cf_accumulated_q2_base = models.DecimalField(**BILLION, verbose_name='基本情景未来第二季度累计现金及流动性管理工具')
    cf_accumulated_q3_base = models.DecimalField(**BILLION, verbose_name='基本情景未来第三季度累计现金及流动性管理工具')
    cf_accumulated_q4_base = models.DecimalField(**BILLION, verbose_name='基本情景未来第四季度累计现金及流动性管理工具')
    cf_accumulated_y2_base = models.DecimalField(**BILLION, verbose_name='基本情景未来第二年累计现金及流动性管理工具')
    cf_accumulated_y3_base = models.DecimalField(**BILLION, verbose_name='基本情景未来第三年累计现金及流动性管理工具')

    cf_accumulated_q1_stress = models.DecimalField(**BILLION, verbose_name='压力情景未来第一季度累计现金及流动性管理工具')
    cf_accumulated_q2_stress = models.DecimalField(**BILLION, verbose_name='压力情景未来第二季度累计现金及流动性管理工具')
    cf_accumulated_q3_stress = models.DecimalField(**BILLION, verbose_name='压力情景未来第三季度累计现金及流动性管理工具')
    cf_accumulated_q4_stress = models.DecimalField(**BILLION, verbose_name='压力情景未来第四季度累计现金及流动性管理工具')
    cf_accumulated_y2_stress = models.DecimalField(**BILLION, verbose_name='压力情景未来第二年累计现金及流动性管理工具')
    cf_accumulated_y3_stress = models.DecimalField(**BILLION, verbose_name='压力情景未来第三年累计现金及流动性管理工具')

    class Meta:
        verbose_name_plural = verbose_name = '现金流压力测试'
