from flask import Flask, render_template, make_response, request, jsonify, Blueprint

from database import db, get_or_create
from models.build import Build
from models.result import Result
from models.test_run import TestRun
from models.test import Test
from models.project import Project

api = Blueprint("api", "api", url_prefix="/api/v1")

# BUILDS

@api.route('/builds', methods=['GET'])
def get_builds():
    build_list = []
    builds = Build.query.all()
    for build in builds:
        build_list.append(
            {
                'build_nr': build.build_nr,
                'created': build.created,
                'comment': build.comment,
            }
        )

    return jsonify(builds=build_list)


@api.route('/builds', methods=['POST'])
def create_build():
    payload = request.json
    build_nr = payload.get("build_nr")
    comment = payload.get("comment")

    build = get_or_create(db.session, Build, project_id=1, build_nr=build_nr)
    build.comment = comment
    db.session.commit()
    return jsonify(build_nr=build.build_nr, comment=build.comment), 201

@api.route('/builds/<build_nr>', methods=['PATCH'])
def update_build(build_nr):
    build = Build.query.get(build_nr)
    payload = request.json
    build.comment = payload.get("comment")
    db.session.commit()
    return jsonify(build_nr=build.build_nr), 200

