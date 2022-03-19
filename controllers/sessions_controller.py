from flask import Flask, Blueprint, render_template, request, redirect, session
from models.session import Session
from repositories import session_repository

sessions_blueprint = Blueprint("sessions", __name__)

@sessions_blueprint.route('/classes')
def show_classes():
    sessions = session_repository.select_all()
    return render_template('/sessions/index.html', title="Classes", sessions=sessions)

# @sessions_blueprint.route('/classes/new')


# @sessions_blueprint.route('/classes', methods=['POST'])


# @sessions_blueprint.route('/classes/<id>')


# @sessions_blueprint.route('/classes/<id>/edit')


# @sessions_blueprint.route('/classes/<id>', methods=['POST'])


# @sessions_blueprint.route('/classes/<id>/members')