from flask import Flask, Blueprint, render_template, request, redirect
from models.booking import Booking
from repositories import booking_repository

bookings_blueprint = Blueprint("bookings", __name__)