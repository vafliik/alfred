from flask import Flask, render_template, make_response, request, jsonify, Blueprint, abort

from database import db, get_or_create
from models.build import Build
from models.result import Result
from models.test_run import TestRun
from models.test import Test
from models.project import Project

api = Blueprint("api", "api", url_prefix="/api/v1")

# PROJECTS

@api.route('/projects', methods=['GET'])
def get_projects():
    project_list = []
    projects = Project.query.all()
    for project in projects:
        project_list.append(
            {
                'id': project.id,
                'name': project.name,
            }
        )

    return jsonify(projects=project_list)


@api.route('/projects/<int:project_id>', methods=['GET'])
@api.route('/projects/<string:project_name>', methods=['GET'])
def get_project(project_id=None, project_name=None):
    project = get_project_by_id_or_name(project_id, project_name)
    if not project:
        abort(404)
    return jsonify(id=project.id,
                   name=project.name)


@api.route('/projects', methods=['POST'])
def create_project():
    payload = request.json
    name = payload.get("name")

    project = get_or_create(db.session, Project, name=name)
    db.session.commit()
    return jsonify(id=project.id, name=project.name), 201


@api.route('/projects/<int:project_id>', methods=['PATCH'])
@api.route('/projects/<string:project_name>', methods=['PATCH'])
def update_project(project_id=None, project_name=None):
    project = get_project_by_id_or_name(project_id, project_name)
    payload = request.json
    project.name = payload.get("name")
    db.session.commit()
    return jsonify(id=project.id, name=project.name), 200


# BUILDS

@api.route('/projects/<int:project_id>/builds', methods=['GET'])
@api.route('/projects/<string:project_name>/builds', methods=['GET'])
def get_builds(project_id=None, project_name=None):
    project = get_project_by_id_or_name(project_id, project_name)
    build_list = []
    builds = project.builds
    for build in builds:
        build_list.append(
            {
                'build_nr': build.build_nr,
                'created': build.created,
                'comment': build.comment,
            }
        )

    return jsonify(builds=build_list)


@api.route('/projects/<int:project_id>/builds/<build_nr>', methods=['GET'])
@api.route('/projects/<string:project_name>/builds/<build_nr>', methods=['GET'])
def get_build(build_nr, project_id=None, project_name=None):
    project = get_project_by_id_or_name(project_id, project_name)
    build = Build.query.filter_by(project_id=project.id, build_nr=build_nr).first_or_404()
    return jsonify(build_nr=build.build_nr,
                   created=build.created,
                   comment=build.comment)


@api.route('/projects/<int:project_id>/builds', methods=['POST'])
@api.route('/projects/<int:project_name>/builds', methods=['POST'])
def create_build(project_id=None, project_name=None):
    project = get_project_by_id_or_name(project_id, project_name)
    payload = request.json
    build_nr = payload.get("build_nr")
    comment = payload.get("comment")

    build = get_or_create(db.session, Build, project_id=project.id, build_nr=build_nr)
    build.comment = comment
    db.session.commit()
    return jsonify(build_nr=build.build_nr, comment=build.comment), 201


@api.route('/projects/<int:project_id>/builds/<build_nr>', methods=['PATCH'])
@api.route('/projects/<string:project_name>/builds/<build_nr>', methods=['PATCH'])
def update_build(build_nr, project_id=None, project_name=None):
    project = get_project_by_id_or_name(project_id, project_name)
    build = Build.query.filter_by(project_id=project.id, build_nr=build_nr).first_or_404()
    payload = request.json
    build.comment = payload.get("comment")
    db.session.commit()
    return jsonify(build_nr=build.build_nr, comment=build.comment), 200


# Utils

def get_project_by_id_or_name(project_id, project_name):
    project = None
    if project_id:
        project = Project.query.get(project_id)
    elif project_name:
        project = Project.query.filter(Project.name.ilike(project_name)).first()
    return project
