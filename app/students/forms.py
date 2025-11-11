from flask_wtf import FlaskForm  
from wtforms import StringField, SubmitField, BooleanField, DateField  
from wtforms.validators import DataRequired, Email, Length, Optional, ValidationError  
from app.models.student import Student # تم التعديل هنا ليتوافق مع هيكلك  

class StudentForm(FlaskForm):  
    student_id_number = StringField('رقم تعريف الطالب', validators=[DataRequired(), Length(min=2, max=20)])  
    first_name = StringField('الاسم الأول', validators=[DataRequired(), Length(max=64)])  
    last_name = StringField('الاسم الأخير', validators=[DataRequired(), Length(max=64)])  
    email = StringField('البريد الإلكتروني', validators=[Optional(), Email(), Length(max=120)])  
    phone_number = StringField('رقم الهاتف', validators=[Optional(), Length(max=20)])  
    grade = StringField('الصف الدراسي', validators=[Optional(), Length(max=10)])  
    major = StringField('التخصص', validators=[Optional(), Length(max=64)])  
    date_of_birth = DateField('تاريخ الميلاد (YYYY-MM-DD)', format='%Y-%m-%d', validators=[Optional()])  
    is_active = BooleanField('نشط', default=True)  
    submit = SubmitField('حفظ الطالب')  

    def __init__(self, original_id_number=None, original_email=None, *args, **kwargs):  
        super(StudentForm, self).__init__(*args, **kwargs)  
        self.original_id_number = original_id_number  
        self.original_email = original_email  

    def validate_student_id_number(self, student_id_number_field):  
        if student_id_number_field.data != self.original_id_number:  
            student = Student.query.filter_by(student_id_number=student_id_number_field.data).first()  
            if student:  
                raise ValidationError('رقم تعريف الطالب هذا موجود بالفعل. يرجى اختيار رقم آخر.')  

    def validate_email(self, email_field):  
        if email_field.data and email_field.data != self.original_email:  
            student = Student.query.filter_by(email=email_field.data).first()  
            if student:  
                raise ValidationError('هذا البريد الإلكتروني مسجل لطالب آخر. يرجى اختيار بريد آخر.')