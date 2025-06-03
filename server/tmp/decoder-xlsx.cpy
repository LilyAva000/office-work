import re
from openpyxl import load_workbook

class ExcelTemplateDecoder:
    def __init__(self, template_path, filled_path):
        self.template_path = template_path
        self.filled_path = filled_path
        self.template_wb = load_workbook(self.template_path)
        self.template_ws = self.template_wb.active
        self.filled_wb = load_workbook(self.filled_path)
        self.filled_ws = self.filled_wb.active
        self.sample_row_idx, self.var_keys = self._find_var_keys()

    def _find_var_keys(self):
        """找到模板样板行和每一列的变量key，支持嵌套（如考核['2023']）"""
        sample_row_idx = None
        var_keys = []
        for i, row in enumerate(self.template_ws.iter_rows(min_row=1, max_row=self.template_ws.max_row), 1):
            for cell in row:
                if cell.value and isinstance(cell.value, str) and "{{" in cell.value:
                    sample_row_idx = i
                    break
            if sample_row_idx:
                break
        if sample_row_idx is None:
            raise RuntimeError("未找到包含占位符的样板行")
        for cell in self.template_ws[sample_row_idx]:
            # 提取 {{变量}} 或 {{变量['2023']}} 里的内容
            if cell.value and "{{" in str(cell.value):
                match = re.search(r"{{\s*(.*?)\s*}}", str(cell.value))
                var_keys.append(match.group(1) if match else None)
            else:
                var_keys.append(None)
        return sample_row_idx, var_keys

    def _set_nested_value(self, d, keyexpr, value):
        """支持嵌套key的赋值，如 考核['2023']"""
        main = keyexpr.strip()
        # 先分割主key和后续key
        m = re.match(r"^([^\[]+)((?:\[[^\]]+\])*)$", main)
        if not m:
            d[main] = value
            return
        base = m.group(1)
        rest = m.group(2)
        if not rest:
            d[base] = value
            return
        if base not in d or not isinstance(d[base], dict):
            d[base] = {}
        sub = d[base]
        keys = re.findall(r"\[([^\]]+)\]", rest)
        for k in keys[:-1]:
            k = k.strip(" '\"")
            if k not in sub or not isinstance(sub[k], dict):
                sub[k] = {}
            sub = sub[k]
        last_key = keys[-1].strip(" '\"")
        sub[last_key] = value

    def extract(self):
        """提取数据，返回list（多行）或dict（单行）"""
        # 数据区从样板行对应的行号在已填写表中开始
        data_start = self.sample_row_idx
        # 判断是否为单行：下方是否只剩一行
        rows = list(self.filled_ws.iter_rows(min_row=data_start, max_row=self.filled_ws.max_row))
        results = []
        for row in rows:
            row_dict = {}
            empty_row = True
            for cell, key in zip(row, self.var_keys):
                if key:
                    val = cell.value
                    if val is not None and str(val).strip() != "":
                        empty_row = False
                    self._set_nested_value(row_dict, key, val)
            if not empty_row:
                results.append(row_dict)
        if len(results) == 1:
            return results[0]
        else:
            return results

def decode_excel():
    gt_true = [
        {
            "序号": '1',
            "证件号": "1234567890",
            "姓名": "张三",
            "出生年月": "1990-01-01",
            "性别": "男",
            "民族": "汉",
            "考核": {"2023": "合格", "2024": "优秀"}
        },
        {
            "序号": '2',
            "证件号": "2234567890",
            "姓名": "李四",
            "出生年月": "1992-03-04",
            "性别": "女",
            "民族": "汉",
            "考核": {"2023": "优秀", "2024": "合格"}
        }
    ]
    print(gt_true)
    template_path = "templates/excel/excel-table-template.xlsx"
    filled_path = "output/result.xlsx"
    extractor = ExcelTemplateDecoder(template_path, filled_path)
    info = extractor.extract()
    print(f"{filled_path}提取出的info：")
    print(info)
    print("提取结果与预期一致" if info == gt_true else "提取结果与预期不一致")

if __name__ == "__main__":
    decode_excel()