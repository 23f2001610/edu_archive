import os
import uuid
from flask import render_template, redirect, url_for, flash, request, send_from_directory, abort
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.utils import secure_filename

from app import app, db, login_manager
from models import Admin, Course, Subject, Note, QuestionPaper
from forms import (LoginForm, CourseForm, SubjectForm, NoteForm, NoteEditForm, 
                   QuestionPaperForm, QuestionPaperEditForm)


@login_manager.user_loader
def load_user(user_id):
    return Admin.query.get(int(user_id))


def allowed_file(filename):
    allowed_extensions = {'pdf', 'doc', 'docx', 'ppt', 'pptx', 'txt'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions


def save_file(file):
    if file and allowed_file(file.filename):
        original_filename = secure_filename(file.filename)
        extension = original_filename.rsplit('.', 1)[1].lower()
        unique_filename = f"{uuid.uuid4().hex}.{extension}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        file.save(filepath)
        file_size = os.path.getsize(filepath)
        return unique_filename, original_filename, file_size
    return None, None, None


def delete_file(filename):
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if os.path.exists(filepath):
        os.remove(filepath)


def format_file_size(size):
    if size < 1024:
        return f"{size} B"
    elif size < 1024 * 1024:
        return f"{size / 1024:.1f} KB"
    else:
        return f"{size / (1024 * 1024):.1f} MB"


app.jinja_env.filters['format_size'] = format_file_size


@app.route('/')
def index():
    courses = Course.query.all()
    recent_notes = Note.query.order_by(Note.uploaded_at.desc()).limit(5).all()
    recent_papers = QuestionPaper.query.order_by(QuestionPaper.uploaded_at.desc()).limit(5).all()
    return render_template('index.html', courses=courses, recent_notes=recent_notes, recent_papers=recent_papers)


@app.route('/notes')
def notes():
    courses = Course.query.all()
    return render_template('notes.html', courses=courses)


@app.route('/notes/course/<int:course_id>')
def course_subjects(course_id):
    course = Course.query.get_or_404(course_id)
    subjects = Subject.query.filter_by(course_id=course_id).order_by(Subject.semester).all()
    return render_template('course_subjects.html', course=course, subjects=subjects)


@app.route('/notes/subject/<int:subject_id>')
def subject_notes(subject_id):
    subject = Subject.query.get_or_404(subject_id)
    notes = Note.query.filter_by(subject_id=subject_id).order_by(Note.uploaded_at.desc()).all()
    return render_template('subject_notes.html', subject=subject, notes=notes)


@app.route('/question-papers')
def question_papers():
    semester_filter = request.args.get('semester', type=int)
    year_filter = request.args.get('year', type=int)
    
    query = QuestionPaper.query
    
    if semester_filter:
        query = query.filter_by(semester=semester_filter)
    if year_filter:
        query = query.filter_by(year=year_filter)
    
    papers = query.order_by(QuestionPaper.year.desc(), QuestionPaper.semester).all()
    
    years = db.session.query(QuestionPaper.year).distinct().order_by(QuestionPaper.year.desc()).all()
    years = [y[0] for y in years]
    
    semesters = db.session.query(QuestionPaper.semester).distinct().order_by(QuestionPaper.semester).all()
    semesters = [s[0] for s in semesters]
    
    return render_template('question_papers.html', papers=papers, years=years, semesters=semesters,
                           current_semester=semester_filter, current_year=year_filter)


@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('admin_dashboard'))
    
    form = LoginForm()
    if form.validate_on_submit():
        admin = Admin.query.filter_by(username=form.username.data).first()
        if admin and admin.check_password(form.password.data):
            login_user(admin)
            flash('Login successful!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page or url_for('admin_dashboard'))
        flash('Invalid username or password', 'danger')
    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))


@app.route('/admin')
@login_required
def admin_dashboard():
    total_notes = Note.query.count()
    total_papers = QuestionPaper.query.count()
    total_courses = Course.query.count()
    total_subjects = Subject.query.count()
    recent_notes = Note.query.order_by(Note.uploaded_at.desc()).limit(5).all()
    recent_papers = QuestionPaper.query.order_by(QuestionPaper.uploaded_at.desc()).limit(5).all()
    return render_template('admin/dashboard.html', 
                           total_notes=total_notes, 
                           total_papers=total_papers,
                           total_courses=total_courses,
                           total_subjects=total_subjects,
                           recent_notes=recent_notes,
                           recent_papers=recent_papers)


@app.route('/admin/courses')
@login_required
def admin_courses():
    courses = Course.query.all()
    return render_template('admin/courses.html', courses=courses)


@app.route('/admin/courses/add', methods=['GET', 'POST'])
@login_required
def admin_add_course():
    form = CourseForm()
    if form.validate_on_submit():
        course = Course(name=form.name.data, description=form.description.data)
        db.session.add(course)
        db.session.commit()
        flash('Course added successfully!', 'success')
        return redirect(url_for('admin_courses'))
    return render_template('admin/course_form.html', form=form, title='Add Course')


@app.route('/admin/courses/edit/<int:course_id>', methods=['GET', 'POST'])
@login_required
def admin_edit_course(course_id):
    course = Course.query.get_or_404(course_id)
    form = CourseForm(obj=course)
    if form.validate_on_submit():
        course.name = form.name.data
        course.description = form.description.data
        db.session.commit()
        flash('Course updated successfully!', 'success')
        return redirect(url_for('admin_courses'))
    return render_template('admin/course_form.html', form=form, title='Edit Course')


@app.route('/admin/courses/delete/<int:course_id>', methods=['POST'])
@login_required
def admin_delete_course(course_id):
    course = Course.query.get_or_404(course_id)
    for subject in course.subjects:
        for note in subject.notes:
            delete_file(note.filename)
        for paper in subject.question_papers:
            delete_file(paper.filename)
    db.session.delete(course)
    db.session.commit()
    flash('Course deleted successfully!', 'success')
    return redirect(url_for('admin_courses'))


@app.route('/admin/subjects')
@login_required
def admin_subjects():
    subjects = Subject.query.join(Course).order_by(Course.name, Subject.semester).all()
    return render_template('admin/subjects.html', subjects=subjects)


@app.route('/admin/subjects/add', methods=['GET', 'POST'])
@login_required
def admin_add_subject():
    form = SubjectForm()
    form.course_id.choices = [(c.id, c.name) for c in Course.query.order_by(Course.name).all()]
    if form.validate_on_submit():
        subject = Subject(
            name=form.name.data, 
            course_id=form.course_id.data,
            semester=form.semester.data
        )
        db.session.add(subject)
        db.session.commit()
        flash('Subject added successfully!', 'success')
        return redirect(url_for('admin_subjects'))
    return render_template('admin/subject_form.html', form=form, title='Add Subject')


@app.route('/admin/subjects/edit/<int:subject_id>', methods=['GET', 'POST'])
@login_required
def admin_edit_subject(subject_id):
    subject = Subject.query.get_or_404(subject_id)
    form = SubjectForm(obj=subject)
    form.course_id.choices = [(c.id, c.name) for c in Course.query.order_by(Course.name).all()]
    if form.validate_on_submit():
        subject.name = form.name.data
        subject.course_id = form.course_id.data
        subject.semester = form.semester.data
        db.session.commit()
        flash('Subject updated successfully!', 'success')
        return redirect(url_for('admin_subjects'))
    return render_template('admin/subject_form.html', form=form, title='Edit Subject')


@app.route('/admin/subjects/delete/<int:subject_id>', methods=['POST'])
@login_required
def admin_delete_subject(subject_id):
    subject = Subject.query.get_or_404(subject_id)
    for note in subject.notes:
        delete_file(note.filename)
    for paper in subject.question_papers:
        delete_file(paper.filename)
    db.session.delete(subject)
    db.session.commit()
    flash('Subject deleted successfully!', 'success')
    return redirect(url_for('admin_subjects'))


@app.route('/admin/notes')
@login_required
def admin_notes():
    notes = Note.query.join(Subject).order_by(Note.uploaded_at.desc()).all()
    return render_template('admin/notes.html', notes=notes)


@app.route('/admin/notes/add', methods=['GET', 'POST'])
@login_required
def admin_add_note():
    form = NoteForm()
    subjects = Subject.query.join(Course).order_by(Course.name, Subject.name).all()
    form.subject_id.choices = [(s.id, f"{s.course.name} - {s.name}") for s in subjects]
    
    if form.validate_on_submit():
        filename, original_filename, file_size = save_file(form.file.data)
        if filename:
            note = Note(
                title=form.title.data,
                description=form.description.data,
                subject_id=form.subject_id.data,
                filename=filename,
                original_filename=original_filename,
                file_size=file_size
            )
            db.session.add(note)
            db.session.commit()
            flash('Note added successfully!', 'success')
            return redirect(url_for('admin_notes'))
        flash('Error uploading file', 'danger')
    return render_template('admin/note_form.html', form=form, title='Add Note')


@app.route('/admin/notes/edit/<int:note_id>', methods=['GET', 'POST'])
@login_required
def admin_edit_note(note_id):
    note = Note.query.get_or_404(note_id)
    form = NoteEditForm(obj=note)
    subjects = Subject.query.join(Course).order_by(Course.name, Subject.name).all()
    form.subject_id.choices = [(s.id, f"{s.course.name} - {s.name}") for s in subjects]
    
    if form.validate_on_submit():
        note.title = form.title.data
        note.description = form.description.data
        note.subject_id = form.subject_id.data
        
        if form.file.data:
            delete_file(note.filename)
            filename, original_filename, file_size = save_file(form.file.data)
            if filename:
                note.filename = filename
                note.original_filename = original_filename
                note.file_size = file_size
        
        db.session.commit()
        flash('Note updated successfully!', 'success')
        return redirect(url_for('admin_notes'))
    return render_template('admin/note_form.html', form=form, title='Edit Note', note=note)


@app.route('/admin/notes/delete/<int:note_id>', methods=['POST'])
@login_required
def admin_delete_note(note_id):
    note = Note.query.get_or_404(note_id)
    delete_file(note.filename)
    db.session.delete(note)
    db.session.commit()
    flash('Note deleted successfully!', 'success')
    return redirect(url_for('admin_notes'))


@app.route('/admin/question-papers')
@login_required
def admin_question_papers():
    papers = QuestionPaper.query.join(Subject).order_by(QuestionPaper.uploaded_at.desc()).all()
    return render_template('admin/question_papers.html', papers=papers)


@app.route('/admin/question-papers/add', methods=['GET', 'POST'])
@login_required
def admin_add_question_paper():
    form = QuestionPaperForm()
    subjects = Subject.query.join(Course).order_by(Course.name, Subject.name).all()
    form.subject_id.choices = [(s.id, f"{s.course.name} - {s.name}") for s in subjects]
    
    if form.validate_on_submit():
        filename, original_filename, file_size = save_file(form.file.data)
        if filename:
            paper = QuestionPaper(
                title=form.title.data,
                year=form.year.data,
                semester=form.semester.data,
                exam_type=form.exam_type.data,
                subject_id=form.subject_id.data,
                filename=filename,
                original_filename=original_filename,
                file_size=file_size
            )
            db.session.add(paper)
            db.session.commit()
            flash('Question paper added successfully!', 'success')
            return redirect(url_for('admin_question_papers'))
        flash('Error uploading file', 'danger')
    return render_template('admin/question_paper_form.html', form=form, title='Add Question Paper')


@app.route('/admin/question-papers/edit/<int:paper_id>', methods=['GET', 'POST'])
@login_required
def admin_edit_question_paper(paper_id):
    paper = QuestionPaper.query.get_or_404(paper_id)
    form = QuestionPaperEditForm(obj=paper)
    subjects = Subject.query.join(Course).order_by(Course.name, Subject.name).all()
    form.subject_id.choices = [(s.id, f"{s.course.name} - {s.name}") for s in subjects]
    
    if form.validate_on_submit():
        paper.title = form.title.data
        paper.year = form.year.data
        paper.semester = form.semester.data
        paper.exam_type = form.exam_type.data
        paper.subject_id = form.subject_id.data
        
        if form.file.data:
            delete_file(paper.filename)
            filename, original_filename, file_size = save_file(form.file.data)
            if filename:
                paper.filename = filename
                paper.original_filename = original_filename
                paper.file_size = file_size
        
        db.session.commit()
        flash('Question paper updated successfully!', 'success')
        return redirect(url_for('admin_question_papers'))
    return render_template('admin/question_paper_form.html', form=form, title='Edit Question Paper', paper=paper)


@app.route('/admin/question-papers/delete/<int:paper_id>', methods=['POST'])
@login_required
def admin_delete_question_paper(paper_id):
    paper = QuestionPaper.query.get_or_404(paper_id)
    delete_file(paper.filename)
    db.session.delete(paper)
    db.session.commit()
    flash('Question paper deleted successfully!', 'success')
    return redirect(url_for('admin_question_papers'))
