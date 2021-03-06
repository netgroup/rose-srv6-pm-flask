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

from flask import (
    Blueprint, flash, g, redirect, request, session, url_for, jsonify, abort, make_response
)
from rose_be.error_handler import Unauthorized, BadRequest, ServerError, ResourceNotFound
from rose_be import ArangoDB
from arango.exceptions import AQLQueryExecuteError
import json
from flask_cors import CORS

bp = Blueprint('graphs', __name__, url_prefix='/api/graphs')


@bp.route('/', methods=(['GET']))
def list_graphs():
    try:
        list_graphs = ArangoDB.connection.graphs()
        return jsonify(list_graphs)
    except KeyError as e:
        abort(400, description=e)
    except BadRequest as e:
        abort(400, description=e.description)
    except Unauthorized as e:
        abort(401, description=e.description)
    except ServerError as e:
        abort(500, description=e.description)


@bp.route('/<graph_id>', methods=(['GET']))
def get_graph(graph_id):
    try:
        nodes = []
        links = []
        cursor = ArangoDB.connection.aql.execute('FOR doc IN nodes RETURN doc')
        for document in cursor:
            document['id'] = document.pop('_id')
            nodes.append(document)
        cursor = ArangoDB.connection.aql.execute('FOR doc IN edges RETURN doc')
        for document in cursor:
            document['source'] = document.pop('_from')
            document['target'] = document.pop('_to')
            links.append(document)
        result = {
            'nodes': nodes,
            'links': links
        }
        return jsonify(result)
    except KeyError as e:
        abort(400, description=e)
    except BadRequest as e:
        abort(400, description=e.description)
    except Unauthorized as e:
        abort(401, description=e.description)
    except ResourceNotFound as e:
        abort(404, description=e.description)
    except ServerError as e:
        abort(500, description=e.description)
    except AQLQueryExecuteError as e:
        return jsonify({})
