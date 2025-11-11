# app/auth/forms.py  
from flask_wtf import FlaskForm  
from wtforms import StringField, PasswordField, BooleanField, SubmitField  
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, Length  
from app.models.user import User # استيراد نموذج المستخدم للتحقق من الوجود  

class LoginForm(FlaskForm):  
    username = StringField('اسم المستخدم', validators=[DataRequired()])  
    password = PasswordField('كلمة المرور', validators=[DataRequired()])  
    remember_me = BooleanField('تذكرني')  
    submit = SubmitField('تسجيل الدخول')  

class RegistrationForm(FlaskForm):  
    username = StringField('اسم المستخدم', validators=[DataRequired(), Length(min=4, max=64)])  
    email = StringField('البريد الإلكتروني', validators=[DataRequired(), Email(), Length(max=120)])  
    password = PasswordField('كلمة المرور', validators=[DataRequired(), Length(min=6)])  
    password2 = PasswordField(  
        'تأكيد كلمة المرور', validators=[DataRequired(), EqualTo('password', message='كلمتا المرور غير متطابقتين')])  
    submit = SubmitField('تسجيل')  

    def validate_username(self, username):  
        user = User.query.filter_by(username=username.data).first()  
        if user is not None:  
            raise ValidationError('اسم المستخدم هذا مستخدم بالفعل. الرجاء اختيار اسم آخر.')  

    def validate_email(self, email):  
        user = User.query.filter_by(email=email.data).first()  
        if user is not None:  
            raise ValidationError('البريد الإلكتروني هذا مسجل بالفعل. الرجاء استخدام بريد إلكتروني آخر.')