from flask import render_template, request, redirect, url_for, flash, abort, session, jsonify, Blueprint
import json
import os.path
from werkzeug.utils import secure_filename

from .predict_disease import predict_disease

bp = Blueprint('project',__name__)

@bp.route('/')
def home():
    return render_template('home.html', codes=session.keys())

@bp.route('/your-url', methods=['GET','POST'])
def your_url():
    if request.method == 'POST':
        codes = {}

        if os.path.exists('codes.json'):
            with open('codes.json') as codes_file:
                codes = json.load(codes_file)

        if request.form['code'] in codes.keys():
            flash('That short code has already been taken. Please select another name.')
            return redirect(url_for('project.home'))

        f = request.files['file']
        full_name = request.form['code'] + '_' + secure_filename(f.filename)
        f.save(os.getcwd() + '/project/static/user_files/' + full_name)
        codes[request.form['code']] = {'file':full_name}


        with open('codes.json','w') as codes_file:
            json.dump(codes, codes_file)
            session[request.form['code']] = True
        return render_template('your_url.html', code = request.form['code'])
    else:
        return redirect(url_for('project.home'))

@bp.route('/<string:code>')
def redirect_to_url(code):
    if os.path.exists('codes.json'):
        with open('codes.json') as codes_file:
            codes = json.load(codes_file)
            if code in codes.keys():
                image_path = os.getcwd() + '/project/static/user_files/' + codes[code]['file']
                disease, info = predict_disease(image_path)
                print(disease + "\n" + info)

                return render_template('result_page.html', disease = disease, info = info,
                    image_path = url_for('static', filename='user_files/' + codes[code]['file']))
    return abort(404)

@bp.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404

@bp.route('/api')
def session_api():
    return jsonify(list(session.keys()))
