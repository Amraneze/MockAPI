# __init__.py - indicates that this directory is a Python package
#
# Copyright 2020 Ait Zeouay Amrane <a.zeouayamran@gmail.com>.
#
# This file is part of MockAPI.
#
import os

import json
from flask import Flask
from flask import jsonify
from .config.default import config


def create_app(test_config=None):
    """Create and configure the Mock API."""
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config)

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.update(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    def readJsonFile(jsonFile):
        with open(jsonFile, encoding='utf-8', errors='ignore') as json_data:
            return json.load(json_data, strict=False)

    @app.route('/')
    def home():
        return str('Welcome to the Mocking API.')

    @app.route('/api/mock')
    def mock():
        data = readJsonFile('app/data/mock.json')
        return jsonify(data)

    app.add_url_rule('/', endpoint='home')

    return app
