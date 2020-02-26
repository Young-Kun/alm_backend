import xlrd
import os
from rest_framework import serializers

from alm_backend.settings import BASE_DIR


# 装饰器，获取一群单元格的数据，存在一个二维字典里
# axis一般指账户所在的轴
# sheet_name:表名; rows:行字典; cols:列字典 是必须参数；acc_in_row为账号是否在横轴，默认为True
# -999为空值
def get_cells(obj):
    def wrap(self, *args, **kwargs):
        assert hasattr(obj, 'sheet_name'), '未指定sheet_name'
        assert hasattr(obj, 'rows'), 'rows字段未设置'
        assert hasattr(obj, 'cols'), 'cols字段未设置'
        sheet_name = getattr(obj, 'sheet_name')
        rows = getattr(obj, 'rows')
        cols = getattr(obj, 'cols')
        acc_in_row = getattr(obj, 'acc_in_row') if hasattr(obj, 'acc_in_row') else True  # 默认账户在行
        cells_data_type = getattr(obj, 'cells_data_type') if hasattr(obj, 'cells_data_type') else float  # 默认数据类型为float
        results = {}
        if acc_in_row:
            accs = rows
            fields = cols
        else:
            accs = cols
            fields = rows
        for acc in accs:
            tmp = {}
            for field in fields:
                row = rows[acc if acc_in_row else field]
                col = cols[field if acc_in_row else acc]
                if row is None or col is None:
                    tmp[field] = -999
                else:
                    tmp[field] = self.get_cell(sheet_name, row, col, cells_data_type)
            results[acc] = tmp
        return results

    return wrap


class ExcelData:
    """
    file可以是路径或文件实例
    @字段命名规则：账户_指标
    """

    def __init__(self, file):
        if isinstance(file, str):
            self.file = xlrd.open_workbook(file)
        else:
            self.file = xlrd.open_workbook(file_contents=file.read())

    # 获取某单元格数据
    def get_cell(self, sheet, row: int, col: int, cell_data_type=float):
        try:
            value = self.file.sheet_by_name(sheet).cell_value(row - 1, col - 1)
        except Exception as e:
            raise serializers.ValidationError(r'表[%s]单元格(%d, %d)读取数据有误\n' % (sheet, row, col) + str(e))
        if not isinstance(value, cell_data_type):
            raise serializers.ValidationError(
                r'表[%s]单元格(%d, %d)数据类型有误，应当为%s，实际为%s' % (sheet, row, col, cell_data_type, type(value)))
        return value

    # 得分
    @property
    @get_cells
    class Score:
        sheet_name = '量化评估标准及评分'
        acc_in_row = False
        rows = {'dur_gap_l_scaled': 4, 'dur_gap_a_scaled': 5, 'hedge_rate': 6, 'dv': 7,
                'avg_3y_gap': 8, 'comp_gap': 9, 'ra_comp_gap': 10, 'fin_gap': 11, 'short_gap': 13,
                'gap_stress1': 15, 'gap_stress2': 16, 'gap_stress3': 17,
                'cash_flow_test_base': 19, 'cash_flow_test_stress': 21, 'liquidity': 23}
        cols = {'score': 9}

    # 会计准备金
    @property
    @get_cells
    class Reserve:
        sheet_name = '表1-3 负债产品信息'
        rows = {'T': 10, 'C': 6, 'P': 8, 'U': 9}
        cols = {'reserve': 9}

    # 资产大类
    @property
    @get_cells
    class Assets:
        sheet_name = '表1-1 资产配置状况'
        acc_in_row = False
        cols = {'T': 3, 'C': 8, 'P': 17, 'U': 20}
        rows = {'tot': 81, 'cash': 17, 'fixed_income': 20, 'equity': 41, 'loan': 77}

    # 修正久期
    @property
    @get_cells
    class ModifiedDuration:
        sheet_name = '表2-1 期限结构匹配测试表_修正久期'
        rows = {'T': 11, 'C': 6, 'P': 9, 'U': 10}
        cols = {'l_in': 3, 'l_out': 5, 'a': 2, 'gap_l_scaled': 6, 'gap_a_scaled': 14}

    # 利率风险对冲率
    @property
    @get_cells
    class HedgeRate:
        sheet_name = '表2-1 期限结构匹配测试表_修正久期'
        rows = {'T': 19, 'C': 14, 'P': 17, 'U': 18}
        cols = {'l_sensitivity': 10, 'hedge_rate': 11}

    # 基点价值变动率
    @property
    @get_cells
    class DV:
        sheet_name = '表2-2 期限结构匹配测试表_关键久期'
        rows = {'T': 35, 'C': None, 'P': None, 'U': None}
        cols = {'dv': 25}

    # 成本收益匹配
    @property
    @get_cells
    class CostReturn:
        sheet_name = '表3-1 成本收益匹配状况表'
        acc_in_row = False
        cols = {'T': 3, 'C': 4, 'P': 7, 'U': 8}
        rows = {'eff_cost': 37, 'capital_cost': 38, 'gre_cost': 39, 'avg_3y_cost': 42,
                'comp_return': 15, 'fin_return': 10, 'ra_comp_return': 32, 'avg_3y_return': 12,
                'comp_gap': 45, 'fin_gap': 47, 'ra_comp_gap': 46, 'avg_3y_gap': 44}

    # 成本收益压力测试 基本情景
    @property
    @get_cells
    class CostReturnStressBase:
        sheet_name = '表3-2 成本收益匹配压力测试表'
        rows = {'T': 63, 'C': 48, 'P': 57, 'U': 60}
        cols = {'fin_return_y1': 3, 'fin_return_y2': 8, 'fin_return_y3': 13,
                'capital_cost_y1': 4, 'capital_cost_y2': 9, 'capital_cost_y3': 14,
                'gap_y1': 6, 'gap_y2': 11, 'gap_y3': 16}

    # 成本收益压力测试 压力一
    @property
    @get_cells
    class CostReturnStress1:
        sheet_name = '表3-2 成本收益匹配压力测试表'
        rows = {'T': 83, 'C': None, 'P': None, 'U': None}
        cols = {'loss_rate': 4, 'gap': 6}

    # 成本收益压力测试 压力二
    @property
    @get_cells
    class CostReturnStress2:
        sheet_name = '表3-2 成本收益匹配压力测试表'
        rows = {'T': 104, 'C': 89, 'P': 98, 'U': 101}
        cols = {'fin_return_y1': 3, 'fin_return_y2': 7, 'fin_return_y3': 11,
                'gre_cost_y1': 4, 'gre_cost_y2': 8, 'gre_cost_y3': 12,
                'gap_y1': 5, 'gap_y2': 9, 'gap_y3': 13}

    # 成本收益压力测试 压力三
    @property
    @get_cells
    class CostReturnStress3:
        sheet_name = '表3-2 成本收益匹配压力测试表'
        rows = {'T': 127, 'C': 112, 'P': 121, 'U': 124}
        cols = {'fin_return_y1': 3, 'fin_return_y2': 7, 'fin_return_y3': 11,
                'capital_cost_y1': 4, 'capital_cost_y2': 8, 'capital_cost_y3': 12,
                'gap_y1': 5, 'gap_y2': 9, 'gap_y3': 13}

    # 现金流压力测试
    @property
    def CashFlowTest(self):
        tmp = {
            'T': self.CashFlowTestAccT,
            'C': self.CashFlowTestAccC,
            'P': self.CashFlowTestAccP,
            'U': self.CashFlowTestAccU,
        }
        results = {}
        for acc in tmp:
            value = tmp[acc]
            content = {}
            for cf_item in value:
                for period in value[cf_item]:
                    content[cf_item + '_' + period] = value[cf_item][period]
            results[acc] = content

        return results

    # 现金流压力测试 基类
    class CashFlowTestBase:
        rows = {'cf_business': 8, 'cf_assets': 32, 'cf_financing': 38, 'cf_net': 47, 'cf_accumulated': 48}
        cols = {'q1_base': 3, 'q2_base': 4, 'q3_base': 5, 'q4_base': 6, 'y2_base': 7, 'y3_base': 8,
                'q1_stress': 9, 'q2_stress': 10, 'q3_stress': 11, 'q4_stress': 12, 'y2_stress': 13, 'y3_stress': 14}

    # 现金流压力测试 普通账户
    @property
    @get_cells
    class CashFlowTestAccT(CashFlowTestBase):
        sheet_name = '表4-1 现金流测试表_普通账户'

    # 现金流压力测试 传统账户
    @property
    @get_cells
    class CashFlowTestAccC(CashFlowTestBase):
        sheet_name = '表4-2 现金流测试表_传统保险账户'

    # 现金流压力测试 分红账户
    @property
    @get_cells
    class CashFlowTestAccP(CashFlowTestBase):
        sheet_name = '表4-3 现金流测试表_分红保险账户'

    # 现金流压力测试 万能账户
    @property
    @get_cells
    class CashFlowTestAccU(CashFlowTestBase):
        sheet_name = '表4-4 现金流测试表_万能保险账户'


# 测试用
if __name__ == "__main__":
    data_path = os.path.join(BASE_DIR, '201912.xlsx')
    data = ExcelData(data_path)

    print(data.Score)
