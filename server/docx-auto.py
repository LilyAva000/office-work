from docxtpl import DocxTemplate, InlineImage
from docx.shared import Mm

info = {
    '姓名': '张三',
    '曾用名': '无',
    '身份证号': '1234567890',
    '出生年月': '1990-01-01',
    '入党日期': '2016-02-15',
    '政治面貌': '团员',
    '籍贯': '北京',
    '文化程度': '本科',
    '性别': '男',
    '民族': '汉',
    '爱好': '吉他',
    '婚姻状况': '已婚',
    '通讯地址': '北京市朝阳区',
    '手机': '13800138000',
    '个人简历': '2008-2012 就读于XX大学\n2012-2020 就职于XX公司',
    '家庭情况': [
        {'关系': '父亲', '姓名': '张爸', '身份证号': '1111111111', '工作单位': '某公司'},
        {'关系': '母亲', '姓名': '李妈', '身份证号': '2222222222', '工作单位': '某单位'},
        {'关系': '配偶', '姓名': '王美', '身份证号': '3333333333', '工作单位': '某单位'},
    ],
    '照片': r'C:\Users\jfw\Pictures\img\loading.png',
    '有无出国境证件': '无',
    '出国境情况': '无',
}

doc = DocxTemplate("templates/word/word-table.docx")
output_path = "output/word登记表-张三.docx"
info['照片'] = InlineImage(doc, info['照片'], height=Mm(35))

doc.render(info)
doc.save(output_path)

print(f"写入成功，格式已保留，文件已保存到 {output_path}")