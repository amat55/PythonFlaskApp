from wtforms import (StringField, PasswordField, SubmitField,
                     validators, ValidationError, TextAreaField)

from flask_wtf import FlaskForm
from src.models import UserModel
from wtforms.validators import DataRequired, Email
from flask_wtf.file import FileField, FileRequired, FileAllowed


class RegisterForm(FlaskForm):
    name = StringField('Name: ', [validators.DataRequired()], render_kw={'style':'margin-bottom:10px'})
    surname = StringField('Surname: ', [validators.DataRequired()], render_kw={'style':'margin-bottom:10px'})
    email = StringField('Email: ', [validators.Email(), validators.DataRequired()],
                        render_kw={'style':'margin-bottom:10px'})
    password = PasswordField('Password: ',
                             [validators.DataRequired(),
                              validators.EqualTo('confirm', message=' Both password must match! ')],
                             render_kw={'style':'margin-bottom:10px'})
    confirm = PasswordField('Repeat Password: ', [validators.DataRequired()],
                            render_kw={'style':'margin-bottom:10px'})

    submit = SubmitField('Sign up')

    def validate_email(self, email):
        if UserModel.query.filter_by(email=email.data).first():
            raise ValidationError("This email address is already in use!")


class UpdateForm(FlaskForm):
    name = StringField('Name: ', [validators.DataRequired()], render_kw={'style':'margin-bottom:10px'})
    surname = StringField('Surname: ', [validators.DataRequired()], render_kw={'style':'margin-bottom:10px'})
    email = StringField('Email: ', [validators.Email(), validators.DataRequired()],
                        render_kw={'style':'margin-bottom:10px'})
    password = PasswordField('New Password: ',
                             [validators.DataRequired(),
                              validators.EqualTo('confirm', message=' Both password must match! ')],
                             render_kw={'style':'margin-bottom:10px'})

    submit = SubmitField('Update')

    def validate_email(self, email):
        if UserModel.query.filter_by(email=email.data).first():
            raise ValidationError("This email address is already in use!")



class LoginFrom(FlaskForm):
    email = StringField(label='Email', validators=[DataRequired(), Email()],render_kw={'style':'margin-bottom:10px'})
    password = PasswordField(label='Password', validators=[DataRequired()],render_kw={'style':'margin-bottom:10px'})
    submit = SubmitField(label='Sign in')


class BlogForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    subtitle = StringField("Subtitle", validators=[DataRequired()])
    img_url = FileField('Image', validators=[DataRequired(), FileRequired(), FileAllowed(['jpg', 'png', 'gif', 'jpeg'])])
    audio_url = FileField('Audio', validators=[FileAllowed(['mp3', 'wav'])])
    video_url = FileField('Video', validators=[FileAllowed(['mp4', 'webm'])])
    body = TextAreaField("Description", validators=[DataRequired()])
    submit = SubmitField("Submit")




