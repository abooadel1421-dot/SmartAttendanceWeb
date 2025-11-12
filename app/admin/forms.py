# app/admin/forms.py  
from flask_wtf import FlaskForm  
from wtforms import StringField, PasswordField, SubmitField, SelectField, DateField, BooleanField  
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError, Optional  
from datetime import date  

# تأكد من استيراد النماذج (Models) من المسارات الصحيحة  
from app.models.user import User, UserRole # تأكد من وجود UserRole  
from app.models.student import Student  
from app.models.card import Card, CardStatus # تأكد من وجود CardStatus  
from app.models.device import Device, DeviceStatus # تأكد من وجود DeviceStatus  

# Form for User Management  
class UserForm(FlaskForm):  
    username = StringField('اسم المستخدم', validators=[DataRequired(), Length(min=2, max=64)])  
    email = StringField('البريد الإلكتروني', validators=[DataRequired(), Email()])  
    password = PasswordField('كلمة المرور', validators=[Optional(), Length(min=6)])  
    password2 = PasswordField(  
        'تأكيد كلمة المرور', validators=[Optional(), EqualTo('password', message='كلمتا المرور غير متطابقتين')])  
    # استخدام UserRole enum للخيارات  
    role = SelectField('الدور', choices=[(role.value, role.value) for role in UserRole], validators=[DataRequired()])  

    # ****** حقل جديد لربط المستخدم بالطالب ******  
    # هذا الحقل سيتم تعبئته ديناميكيًا في routes.py  
    student_to_link = SelectField('ربط بطالب موجود', choices=[], coerce=str, validators=[Optional()])  
    # *******************************************  

    submit = SubmitField('حفظ')  

    def __init__(self, original_username=None, original_email=None, *args, **kwargs):  
        super(UserForm, self).__init__(*args, **kwargs)  
        self.original_username = original_username  
        self.original_email = original_email  

    def validate_username(self, username):  
        if username.data != self.original_username:  
            user = User.query.filter_by(username=self.username.data).first()  
            if user:  
                raise ValidationError('اسم المستخدم هذا موجود بالفعل. الرجاء اختيار اسم مستخدم آخر.')  

    def validate_email(self, email):  
        if email.data != self.original_email:  
            user = User.query.filter_by(email=self.email.data).first()  
            if user:  
                raise ValidationError('البريد الإلكتروني هذا موجود بالفعل. الرجاء استخدام بريد إلكتروني آخر.')  

# Form for Student Management  
class StudentForm(FlaskForm):  
    student_id_number = StringField('الرقم الأكاديمي', validators=[DataRequired(), Length(max=20)])  
    first_name = StringField('الاسم الأول', validators=[DataRequired(), Length(min=2, max=64)])  
    last_name = StringField('اسم العائلة', validators=[DataRequired(), Length(min=2, max=64)])  
    parent_email = StringField('بريد ولي الأمر الإلكتروني', validators=[Optional(), Email(), Length(max=120)])  
    parent_phone_number = StringField('رقم هاتف ولي الأمر', validators=[Optional(), Length(max=20)])  
    grade = StringField('المستوى', validators=[Optional(), Length(max=10)])  
    major = StringField('التخصص', validators=[Optional(), Length(max=64)])  
    date_of_birth = DateField('تاريخ الميلاد', format='%Y-%m-%d', validators=[Optional()])  
    is_active = BooleanField('نشط', default=True)  

    # ****** حقل جديد لربط الطالب بالمستخدم ******  
    # هذا الحقل سيتم تعبئته ديناميكيًا في routes.py  
    user_to_link = SelectField('ربط بحساب مستخدم (طالب) موجود', choices=[], coerce=str, validators=[Optional()])  
    # *******************************************  

    submit = SubmitField('حفظ')  

    def __init__(self, original_student_id_number=None, *args, **kwargs):  
        super(StudentForm, self).__init__(*args, **kwargs)  
        self.original_student_id_number = original_student_id_number  

    def validate_student_id_number(self, student_id_number):  
        if student_id_number.data != self.original_student_id_number:  
            student = Student.query.filter_by(student_id_number=self.student_id_number.data).first()  
            if student:  
                raise ValidationError('الرقم الأكاديمي هذا مسجل بالفعل.')  

# Form for Card Management  
# في ملف app/admin/forms.py - class CardForm

class CardForm(FlaskForm):  
    card_uid = StringField('معرف البطاقة (UID)', validators=[DataRequired(), Length(max=50)])
    issued_at = DateField('تاريخ الإصدار', format='%Y-%m-%d', default=date.today, validators=[DataRequired()])
    status = SelectField('حالة البطاقة', choices=[(status.value, status.value) for status in CardStatus], validators=[DataRequired()])
    student = SelectField('الطالب المرتبط', coerce=int, validators=[Optional()])
    submit = SubmitField('حفظ')

    def __init__(self, *args, **kwargs):  
        super(CardForm, self).__init__(*args, **kwargs)  
        students = Student.query.order_by(Student.first_name).all()  
        self.student.choices = [(s.id, s.full_name) for s in students]  
        self.student.choices.insert(0, (0, '--- اختر طالب ---'))

# في ملف app/admin/forms.py - استبدل دالة validate_card_uid في class CardForm

    # def validate_card_uid(self, card_uid):
    #     card = Card.query.filter_by(card_uid=self.card_uid.data).first()
    
    #     if card is None:
    #         return  # ما فيه بطاقة بنفس الـ UID = تمام
    
    # # إذا البطاقة الموجودة هي نفس البطاقة اللي بتعدّل عليها
    # # self.obj هو كائن البطاقة الأصلي
    #     if self.obj and self.obj.id == card.id:
    #         return  # نفس البطاقة = تمام
    
    # # بطاقة مختلفة موجودة = خطأ
    #     raise ValidationError('معرف البطاقة هذا موجود بالفعل لبطاقة أخرى.')
# Form for Device Management  
class DeviceForm(FlaskForm):  
    name = StringField('اسم الجهاز', validators=[DataRequired(), Length(min=2, max=100)])  
    serial_number = StringField('الرقم التسلسلي', validators=[DataRequired(), Length(max=100)])  
    location = StringField('الموقع', validators=[DataRequired(), Length(max=100)])  
    # استخدام DeviceStatus enum للخيارات  
    status = SelectField('الحالة', choices=[(status.value, status.value) for status in DeviceStatus], validators=[DataRequired()])  
    submit = SubmitField('حفظ')  

    def __init__(self, original_serial_number=None, *args, **kwargs):  
        super(DeviceForm, self).__init__(*args, **kwargs)  
        self.original_serial_number = original_serial_number  

    def validate_serial_number(self, serial_number):  
        if serial_number.data != self.original_serial_number:  
            device = Device.query.filter_by(serial_number=self.serial_number.data).first()  
            if device:  
                raise ValidationError('الرقم التسلسلي هذا مسجل بالفعل لجهاز آخر.')