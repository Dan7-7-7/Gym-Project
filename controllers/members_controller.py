from flask import Flask, Blueprint, render_template, request, redirect
from models.member import Member
from repositories import member_repository

members_blueprint = Blueprint("members", __name__)