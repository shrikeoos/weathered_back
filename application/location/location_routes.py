from flask import Blueprint, request, make_response
from .location_model import db, LocationModel
from flask_jwt_extended import jwt_required

location_bp = Blueprint('location_bp', __name__)


@location_bp.route('/location', methods=['POST'])
@jwt_required
def create_location():
    id = request.json['id']
    country = request.json['country']
    city = request.json['city']
    latitude = request.json['latitude']
    longitude = request.json['longitude']

    if id and country and city and latitude and longitude:
        location_exists = LocationModel.query.filter(
            LocationModel.id == id).first()
        if location_exists:
            return make_response("This location already exists", 204)
        new_location = LocationModel(
            id=id, country=country, city=city, latitude=latitude, longitude=longitude)
        db.session.add(new_location)
        db.session.commit()
        return make_response(f"{country}, {city} added", 201)
    else:
        return make_response(f"Error in the request", 400)
