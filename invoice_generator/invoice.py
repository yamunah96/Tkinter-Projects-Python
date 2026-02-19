#invoice template
from docxtpl import DocxTemplate
mydoc= DocxTemplate('invoice_template.docx')
invoice_list=[
    [1,"Book",20,20],
    [2,"icecream",2,4],
    [4,"Pizza", 10,40]
]

mydoc.render({
    "name":"poorvi",
    "phone":"123456789",
    "invoice_list":invoice_list,
    "subtotal":64,
    "salestax":"5%",
    "total":60.8
})
mydoc.save("new_invoice.docx")