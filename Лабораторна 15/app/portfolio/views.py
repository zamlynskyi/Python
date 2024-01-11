from flask import render_template, request
from . import portfolio
from .. import navigation
from datetime import datetime
import os


@portfolio.context_processor
def inject_navigation():
    return dict(navigation=navigation())


my_skills = [
    "Python",
    "HTML",
    "CSS",
    "JavaScript",
    "SQL",
    "Git",
    "C++",
    "PHP",
]


@portfolio.route('/')
def home():
    os_info = os.name
    user_agent = request.user_agent.string
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return render_template('portfolio.html', os_info=os_info, user_agent=user_agent, current_time=current_time)


@portfolio.route('/portfolio')
def portfolios():
    os_info = os.name
    user_agent = request.user_agent.string
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return render_template('portfolio.html', os_info=os_info, user_agent=user_agent, current_time=current_time)


@portfolio.route('/skills')
@portfolio.route('/skills/<int:id>')
def skills(id=None):
    if id is None:
        total_skills = len(my_skills)
        return render_template('skills.html', skills=my_skills, total_skills=total_skills)
    elif id < len(my_skills):
        return render_template('skill.html', skills=my_skills[id], id=id + 1)
    else:
        return "Немає навички з таким id"


@portfolio.route('/resume')
def resume():
    return render_template('resume.html')


@portfolio.route('/contacts')
def contacts():
    os_info = os.name
    user_agent = request.user_agent.string
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return render_template('contacts.html', os_info=os_info, user_agent=user_agent, current_time=current_time)
