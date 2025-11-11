# app/utils/helpers.py  

import datetime  

def format_timestamp(timestamp_obj, fmt="%Y-%m-%d %I:%M:%S %p"):  
    """  
    يقوم بتنسيق كائن datetime إلى سلسلة نصية.  
    """  
    if timestamp_obj:  
        return timestamp_obj.strftime(fmt)  
    return ""  

def generate_unique_id(prefix="id_"):  
    """  
    يقوم بإنشاء معرّف فريد بسيط (يمكن تحسينه لاحقًا باستخدام UUID).  
    """  
    return f"{prefix}{datetime.datetime.now().strftime('%Y%m%d%H%M%S%f')}"  

def is_valid_email(email):  
    """  
    يتحقق مما إذا كان البريد الإلكتروني صحيحًا (تحقق بسيط).  
    """  
    # يمكن استخدام مكتبة مثل 'email_validator' للتحقق الأكثر دقة  
    return "@" in email and "." in email.split("@")[-1]  

# يمكنك إضافة المزيد من الدوال المساعدة هنا حسب الحاجة  
# مثال: دالة لتحويل التوقيت الزمني  
# from pytz import timezone  
# def convert_to_local_time(utc_dt, tz_name='Asia/Riyadh'):  
#     local_tz = timezone(tz_name)  
#     return utc_dt.replace(tzinfo=pytz.utc).astimezone(local_tz)