# app/utils/export_helpers.py  

import csv  
from io import StringIO  
# قد تحتاج إلى مكتبات إضافية لتصدير PDF، مثل reportlab أو xhtml2pdf  
# from xhtml2pdf import pisa  
# from flask import make_response  

def export_to_csv(data, headers, filename="export.csv"):  
    """  
    يقوم بتصدير قائمة من القواميس (أو كائنات لها سمات) إلى ملف CSV.  
    data: قائمة من الكائنات أو القواميس المراد تصديرها.  
    headers: قائمة بأسماء الأعمدة (strings) التي تتطابق مع مفاتيح القواميس أو سمات الكائنات.  
    filename: اسم الملف الناتج.  
    """  
    si = StringIO()  
    cw = csv.writer(si)  

    # كتابة رؤوس الأعمدة  
    cw.writerow(headers)  

    # كتابة البيانات  
    for row in data:  
        # تأكد من أننا نصل إلى البيانات بشكل صحيح سواء كانت قاموسًا أو كائنًا  
        if isinstance(row, dict):  
            cw.writerow([row.get(header, '') for header in headers])  
        else:  
            cw.writerow([getattr(row, header, '') for header in headers])  

    output = si.getvalue()  
    si.close()  

    # يمكنك إرجاع الاستجابة مباشرة لـ Flask إذا كنت تستخدم make_response  
    # response = make_response(output)  
    # response.headers["Content-Disposition"] = f"attachment; filename={filename}"  
    # response.headers["Content-type"] = "text/csv"  
    # return response  

    return output # لإرجاع المحتوى كـ string  

def export_to_pdf(html_content, filename="export.pdf"):  
    """  
    يقوم بتحويل محتوى HTML إلى ملف PDF.  
    يتطلب مكتبة xhtml2pdf: pip install xhtml2pdf  
    """  
    # هذه الدالة تتطلب تكوينًا إضافيًا ومكتبات خارجية  
    # مثال بسيط (غير مكتمل بدون تهيئة Flask والاستجابات):  
    # if pisa: # تحقق من استيراد pisa  
    #     result_file = StringIO()  
    #     pisa_status = pisa.CreatePDF(  
    #         html_content,  
    #         dest=result_file  
    #     )  
    #     if not pisa_status.err:  
    #         response = make_response(result_file.getvalue())  
    #         response.headers["Content-Disposition"] = f"attachment; filename={filename}"  
    #         response.headers["Content-type"] = "application/pdf"  
    #         return response  
    # return "Failed to generate PDF", 500  
    
    # حاليًا، دعها كدالة وهمية أو قم بإعادتها كـ NotImplementedError  
    raise NotImplementedError("PDF export requires xhtml2pdf library and proper Flask response handling.")