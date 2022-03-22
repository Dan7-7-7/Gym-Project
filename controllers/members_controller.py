from flask import Flask, Blueprint, render_template, request, redirect
from models.member import Member
from repositories import member_repository

members_blueprint = Blueprint("members", __name__)

@members_blueprint.route('/members')
def all_members():
    members = member_repository.select_all()
    def activated(member):
        return member.activated == False
    members.sort(key=activated)
    return render_template('/members/index.html', title="Members", members=members)

@members_blueprint.route('/members/new')
def new_member():
    return render_template('/members/new_member.html', title="New Member")

@members_blueprint.route('/members', methods=['POST'])
def add_new_member():
    membership = True if "premium" in request.form else False
    member = Member(request.form['name'], request.form['age'], membership)
    member_repository.save(member)
    return redirect('/members')

@members_blueprint.route('/members/<id>')
def single_member(id):
    member = member_repository.select(id)
    return render_template('/members/single_member.html', title="Member Details", member=member)

@members_blueprint.route('/members/<id>/edit')
def edit_member(id):
    member = member_repository.select(id)
    checked = ""
    if member.premium == True:
        checked = "checked"
    return render_template('/members/edit_member.html', title="Edit Member Details", member=member, checked=checked)

@members_blueprint.route('/members/<id>', methods=['POST'])
def update_member(id):
    membership = True if "premium" in request.form else False
    member = Member(request.form['name'], request.form['age'], membership, True, id)
    member_repository.update(member)
    return redirect(f'/members/{id}')

@members_blueprint.route('/members/<id>/deactivate')
def deactivate(id):
    member = member_repository.select(id)
    member_repository.deactivate(member)
    return render_template('/members/deactivate_member.html', title="Deactivate Member", member=member)

@members_blueprint.route('/members/<id>/reactivate')
def reactivate(id):
    member = member_repository.select(id)
    member_repository.reactivate(member)
    return render_template('/members/reactivate_member.html', title="Member Reactivated", member=member)