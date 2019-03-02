# -*- coding: utf-8 -*-
#
# Copyright (C) 2019 CESNET.
#
# invenio-oarepo-ui is free software; you can redistribute it and/or modify it under
# the terms of the MIT License; see LICENSE file for more details.

"""OARepo UI module for invenio"""

from __future__ import absolute_import, print_function

import os
from urllib.parse import urlencode

from flask import Blueprint, current_app, jsonify, session, url_for, request
from flask import render_template
from flask_login import current_user

blueprint = Blueprint(
    'invenio_oarepo_ui',
    __name__,
    url_prefix='/oarepo/1.0',
    template_folder=os.path.join(os.path.dirname(__file__), 'templates')
)


@blueprint.route("/collections")
def collections():
    # get all record rest endpoints and present them as collections
    collections = current_app.config.get('INVENIO_OAREPO_UI_COLLECTIONS', {})
    collections = [
        {
            'code': k,
            **v
        } for k, v in collections.items()
    ]

    return jsonify(collections)


@blueprint.route('/auth/state')
def login_status():
    if current_user.is_anonymous:
        resp = {
            'logged_in': False,
            'user': None,
            'user_info': None
        }
    else:
        resp = {
            'logged_in': True,
            'user': {
                'id': current_user.id,
                'email': current_user.email,
                'roles': [
                    {
                        'id': x.name,
                        'label': x.description
                    } for x in current_user.roles
                ]
            },
            'user_info': session.get('user_info', None).to_dict()
        }

    return jsonify(resp)


@blueprint.route('/auth/login')
def perform_login():
    print(request.headers)
    login_complete_url = current_app.config['INVENIO_OAREPO_UI_LOGIN_URL'] or '/login'
    nextparam = urlencode({
        'next': url_for('invenio_oarepo_ui.login_complete')
    })
    if '?' in login_complete_url:
        login_complete_url += '&' + nextparam
    else:
        login_complete_url += '?' + nextparam
    resp = render_template('login.html', complete=login_complete_url)
    return current_app.response_class(
        resp,
        status=302,
        mimetype='text/html',
        headers={
            'Location': login_complete_url,
        }
    )


@blueprint.route('/auth/complete')
def login_complete():
    return render_template('login_complete.html')
