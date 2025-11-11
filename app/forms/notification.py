# app/forms/notification.py

from flask_wtf import FlaskForm
from wtforms import SelectField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length
from app.models.student import Student # تأكد من استيراد نموذج Student
from app.models.user import User # قد تحتاجها في المستقبل لإسناد الطلاب للمستخدمين

class SendNotificationForm(FlaskForm):
    student_id = SelectField('الطالب المستلم', coerce=int, validators=[DataRequired(message='الرجاء اختيار طالب.')])
    message = TextAreaField('الرسالة', validators=[DataRequired(message='لا يمكن أن تكون الرسالة فارغة.'), Length(min=5, max=500, message='طول الرسالة يجب أن يكون بين 5 و 500 حرف.')])
    submit = SubmitField('إرسال الإشعار')

    def __init__(self, *args, **kwargs):
        super(SendNotificationForm, self).__init__(*args, **kwargs)
        # 🟢 الحل: استخدام عمود حقيقي لعملية الفرز
        # على افتراض أن لديك Student.first_name أو Student.last_name
        # إذا كان لديك عمود واحد للاسم الكامل، استخدمه.
        students = Student.query.order_by(Student.first_name, Student.last_name).all() # أو فقط Student.first_name
        
        # إضافة خيار افتراضي "اختر طالباً" بقيمة 0
        self.student_id.choices = [(0, '--- اختر طالباً ---')] + \
                                  [(s.id, s.full_name) for s in students]