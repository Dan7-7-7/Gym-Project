from flask import Flask, Blueprint, render_template, request, redirect
from models.member import Member
from repositories import member_repository

members_blueprint = Blueprint("members", __name__)

@members_blueprint.route('/members')
def all_members():
    members = member_repository.select_all()
    return render_template('/members/index.html', title="Members", members=members)

@members_blueprint.route('/members/new')
def new_member():
    return render_template('/members/new_member.html', title="New Member")

@members_blueprint.route('/members', methods=['POST'])
def add_new_member():
    member = Member(request.form['name'], request.form['age'])
    member_repository.save(member)
    return redirect('/members')

@members_blueprint.route('/members/<id>')
def single_member(id):
    member = member_repository.select(id)
    return render_template('/members/single_member.html', title="Member", member=member)

@members_blueprint.route('/members/<id>/edit')
def edit_member(id):
    member = member_repository.select(id)
    return render_template('/members/edit_member.html', title="Edit Member Details", member=member)

@members_blueprint.route('/members/<id>', methods=['POST'])
def update_member(id):
    member = Member(request.form['name'], request.form['age'], id)
    member_repository.update(member)
    return redirect(f'/members/{id}')