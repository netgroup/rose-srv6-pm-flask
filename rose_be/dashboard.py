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
import json
from flask_cors import CORS
from arango.exceptions import AQLQueryExecuteError


bp = Blueprint('dashboard', __name__, url_prefix='/api/dashboard')


@bp.route('/', methods=(['GET']))
def dashboard():
    try:
        result = {
            'devices': {'total': 0}
        }
        aql_query = "FOR u IN nodes COLLECT type = u.type WITH COUNT INTO length RETURN { \"type\": type, \"count\": length}"
        cursor = ArangoDB.connection.aql.execute(aql_query)
        for c in cursor:
            result['devices'][c['type']] = c['count']
            result['devices']['total'] += int(c['count'])

        return jsonify(result)
    except KeyError as e:
        abort(400, description=e)
    except BadRequest as e:
        abort(400, description=e.description)
    except Unauthorized as e:
        abort(401, description=e.description)
    except ServerError as e:
        abort(500, description=e.description)
    except AQLQueryExecuteError as e:
        return jsonify({})
