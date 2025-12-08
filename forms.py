from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, PasswordField, TextAreaField, IntegerField, SelectField
from wtforms.validators import DataRequired, Length, NumberRange


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=64)])
    password = PasswordField('Password', validators=[DataRequired()])


class CourseForm(FlaskForm):
    name = StringField('Course Name', validators=[DataRequired(), Length(max=100)])
    description = TextAreaField('Description')


class SubjectForm(FlaskForm):
    name = StringField('Subject Name', validators=[DataRequired(), Length(max=100)])
    course_id = SelectField('Course', coerce=int, validators=[DataRequired()])
    semester = IntegerField('Semester', validators=[DataRequired(), NumberRange(min=1, max=10)])


class NoteForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(max=200)])
    description = TextAreaField('Description')
    subject_id = SelectField('Subject', coerce=int, validators=[DataRequired()])
    file = FileField('File', validators=[
        FileRequired(),
        FileAllowed(['pdf', 'doc', 'docx', 'ppt', 'pptx', 'txt'], 'Only PDF, Word, PowerPoint and Text files allowed!')
    ])


class NoteEditForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(max=200)])
    description = TextAreaField('Description')
    subject_id = SelectField('Subject', coerce=int, validators=[DataRequired()])
    file = FileField('Replace File (optional)', validators=[
        FileAllowed(['pdf', 'doc', 'docx', 'ppt', 'pptx', 'txt'], 'Only PDF, Word, PowerPoint and Text files allowed!')
    ])


class QuestionPaperForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(max=200)])
    year = IntegerField('Year', validators=[DataRequired(), NumberRange(min=2000, max=2100)])
    semester = IntegerField('Semester', validators=[DataRequired(), NumberRange(min=1, max=10)])
    exam_type = SelectField('Exam Type', choices=[
        ('midterm', 'Midterm'),
        ('endterm', 'End Term'),
        ('supplementary', 'Supplementary'),
        ('quiz', 'Quiz'),
        ('other', 'Other')
    ])
    subject_id = SelectField('Subject', coerce=int, validators=[DataRequired()])
    file = FileField('File', validators=[
        FileRequired(),
        FileAllowed(['pdf', 'doc', 'docx'], 'Only PDF and Word files allowed!')
    ])


class QuestionPaperEditForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(max=200)])
    year = IntegerField('Year', validators=[DataRequired(), NumberRange(min=2000, max=2100)])
    semester = IntegerField('Semester', validators=[DataRequired(), NumberRange(min=1, max=10)])
    exam_type = SelectField('Exam Type', choices=[
        ('midterm', 'Midterm'),
        ('endterm', 'End Term'),
        ('supplementary', 'Supplementary'),
        ('quiz', 'Quiz'),
        ('other', 'Other')
    ])
    subject_id = SelectField('Subject', coerce=int, validators=[DataRequired()])
    file = FileField('Replace File (optional)', validators=[
        FileAllowed(['pdf', 'doc', 'docx'], 'Only PDF and Word files allowed!')
    ])
