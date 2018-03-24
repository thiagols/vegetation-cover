from flask import render_template, jsonify
from app import app
from .PlanetScopeCalcs import *

file_url = "319567_2331703_2016-12-07_0c0b-20161207T151953Z.tif"

json = {
        "filename": PlanetScopeCalcs.get_name(file_url),
        "cover": PlanetScopeCalcs.calc_vegetated_area_percent(file_url),
        "area": PlanetScopeCalcs.calc_area(file_url),
        "centroid": PlanetScopeCalcs.get_centroid(file_url),
        "local_time": PlanetScopeCalcs.get_local_time_capture()
    }

@app.route("/")
def index():
    return render_template("index.html")


@app.route('/vegetation-cover', methods=['GET'])
def vegetation_cover():
    return jsonify(json)
