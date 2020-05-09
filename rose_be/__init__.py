#  Copyright 2020 Francesco Lombardo <franclombardo@gmail.com>
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

import os
from flask import Flask, jsonify
from flask_cors import CORS
from flask_python_arango import FlaskArango
from .error_handler import init_errorhandler

ArangoDB = FlaskArango()


def create_app(test_config=None):
    # from . import auth
    from . import device
    from . import graph
    from . import dashboard

    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'rose_be.sqlite'),
    )
    CORS(app, resources={r"/.*": {"origins": "*"}})
    app.config['CORS_HEADERS'] = 'Content-Type'
    app.config['ARANGODB_HOST'] = 'http://arangodb:8529'
    app.config['ARANGODB_DB'] = 'srv6_pm'
    app.config['ARANGODB_USERNAME'] = 'root'
    app.config['ARANGODB_PSW'] = '12345678'

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)
    init_errorhandler(app)
    ArangoDB.init_app(app)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    app.register_blueprint(dashboard.bp)
    # app.register_blueprint(auth.bp)
    app.register_blueprint(device.bp)
    app.register_blueprint(graph.bp)
    # app.register_blueprint(operator.bp)

    return app
