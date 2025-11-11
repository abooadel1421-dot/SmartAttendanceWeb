# app/forms/report.py (ملف جديد)

from flask_wtf import FlaskForm
from wtforms import DateField, TimeField, SelectField, SubmitField
from wtforms.validators import DataRequired, ValidationError
from datetime import time, date
from flask_wtf import FlaskForm
# 🟢 تأكد من وجود TextAreaField هنا
from wtforms import DateField, TimeField, SelectField, SubmitField, TextAreaField # 🟢 أضف TextAreaField هنا
# 🟢 تأكد من وجود Length هنا
from wtforms.validators import DataRequired, ValidationError, Length # 🟢 أضف Length هنا
from datetime import time, date

class GenerateAttendanceReportForm(FlaskForm):
    report_date = DateField('التاريخ', format='%Y-%m-%d', validators=[DataRequired('الرجاء اختيار تاريخ.')])
    start_time = TimeField('وقت بدء الفترة (مثال: 07:30)', format='%H:%M', validators=[DataRequired('الرجاء تحديد وقت بدء الفترة.')])
    end_time = TimeField('وقت انتهاء الفترة (مثال: 08:30)', format='%H:%M', validators=[DataRequired('الرجاء تحديد وقت انتهاء الفترة.')])
    submit = SubmitField('إنشاء الكشف')

    def validate_end_time(self, field):
        if field.data <= self.start_time.data:
            raise ValidationError('وقت الانتهاء يجب أن يكون بعد وقت البدء.')

class UpdateAttendanceStatusForm(FlaskForm):
    # هذا الفورم سيتم إنشاؤه ديناميكياً لكل طالب في الواجهة
    # لا يحتاج إلى حقول هنا، ولكن يمكن أن يكون له حقل Submit
    submit = SubmitField('حفظ التعديلات')

class ExcuseForm(FlaskForm):
    date_of_absence = DateField('تاريخ الغياب/التأخير', format='%Y-%m-%d', validators=[DataRequired('الرجاء اختيار تاريخ الغياب.')])
    reason = TextAreaField('سبب الغياب/التأخير', validators=[DataRequired('الرجاء كتابة السبب.'), Length(min=10, max=500)])
    submit = SubmitField('إرسال العذر')
