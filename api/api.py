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
    """
    @api {get} /projects List All Projects
    @apiVersion 1.0.0
    @apiName get_projects
    @apiGroup Project
    @apiSuccess {Object[]} projects Project list
    @apiSuccess {Number}    projects.id  Project id
    @apiSuccess {String}    projects.name  Project name
    @apiSuccess {Number}    projects.builds_count  Number of builds
    @apiSuccessExample {json} Success-Response:
        HTTP/1.1 200 OK
        [
            {
              "id": 1,
              "name": "Huma",
              "builds_count": 13
            },
            {
              "id": 2,
              "name": "LetzNav",
              "builds_count": 36
            }
        ]
    """
    project_list = []
    projects = Project.query.all()
    for project in projects:
        project_list.append(
            {
                'id': project.id,
                'name': project.name,
                'builds': len(project.builds)
            }
        )

    return jsonify(project_list)


@api.route('/projects/<int:project_id>', methods=['GET'])
@api.route('/projects/<string:project_name>', methods=['GET'])
def get_project(project_id=None, project_name=None):
    """
    @api {get} /projects/:project Get a Project
    @apiVersion 1.0.0
    @apiName get_project
    @apiGroup Project
    @apiDescription The :project parameter can be either project name or project id
    @apiSuccess {Number}    id  Project id
    @apiSuccess {String}    name  Project name
    @apiSuccessExample {json} Success-Response:
        HTTP/1.1 200 OK
        {
          "id": 15,
          "name": "New Project"
        }
    """
    project = get_project_by_id_or_name(project_id, project_name)
    if not project:
        abort(404)
    return jsonify(id=project.id,
                   name=project.name)


@api.route('/projects', methods=['POST'])
def create_project():
    """
    @api {post} /projects Create a New Project
    @apiVersion 1.0.0
    @apiName create_project
    @apiGroup Project
    @apiParam {String}      name Project name
    @apiParamExample {json} Input
        {
          "name": "New Project"
        }
    @apiSuccess {Number}    id  Project id
    @apiSuccess {String}    name  Project name
    @apiSuccess {Number}    builds_count  Number of builds
    @apiSuccessExample {json} Success-Response:
        HTTP/1.1 200 OK
        {
          "id": 15,
          "name": "New Project",
          "builds_count": 0
        }
    """
    payload = request.json
    name = payload.get("name")

    project = get_or_create(db.session, Project, name=name)
    db.session.commit()
    return jsonify(id=project.id, name=project.name), 201


@api.route('/projects/<int:project_id>', methods=['PATCH'])
@api.route('/projects/<string:project_name>', methods=['PATCH'])
def update_project(project_id=None, project_name=None):
    """
    @api {patch} /projects/:project Update a Project
    @apiVersion 1.0.0
    @apiName update_project
    @apiGroup Project
    @apiDescription The :project parameter can be either project name or project id
    @apiParam {String}      name Project name
    @apiParamExample {json} Input
        {
          "name": "New Project Name"
        }
    @apiSuccess {Number}    id  Project id
    @apiSuccess {String}    name  Project name
    @apiSuccessExample {json} Success-Response:
        HTTP/1.1 200 OK
        {
          "id": 15,
          "name": "New Project Name"
        }
    @apiErrorExample {json} Error-Response:
        HTTP/1.1 404 Not Found
        {
          "message": "Project not found"
        }
    """
    project = get_project_by_id_or_name(project_id, project_name)
    if not project:
        return jsonify(message="Project not found"), 404
    else:
        payload = request.json
        project.name = payload.get("name")
        db.session.commit()
        return jsonify(id=project.id, name=project.name), 200


# BUILDS

@api.route('/projects/<int:project_id>/builds', methods=['GET'])
@api.route('/projects/<string:project_name>/builds', methods=['GET'])
def get_builds(project_id=None, project_name=None):
    """
     @api {get} /projects/:project_id/builds List All Builds of a Project
     @apiVersion 1.0.0
     @apiName get_builds
     @apiGroup Build
     @apiSuccess {Object[]} builds Builds list
     @apiSuccess {Number}    builds.build_nr  Build number
     @apiSuccess {String}    builds.comment  Build comment
     @apiSuccess {Date}    builds.created  Date created
     @apiSuccessExample {json} Success-Response:
         HTTP/1.1 200 OK
         [
             {
               "build_nr": 1,
               "comment": "Build manually",
               "created": "Fri, 15 Dec 2017 10:43:52 GMT"
             },
             {
               "build_nr": 2,
               "comment": "CCI build",
               "created": "Sat, 16 Dec 2017 11:20:12 GMT"
             }
         ]
    """
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

    return jsonify(build_list)


@api.route('/projects/<int:project_id>/builds/<build_nr>', methods=['GET'])
@api.route('/projects/<string:project_name>/builds/<build_nr>', methods=['GET'])
def get_build(build_nr, project_id=None, project_name=None):
    project = get_project_by_id_or_name(project_id, project_name)
    build = Build.query.filter_by(project_id=project.id, build_nr=build_nr).first_or_404()
    return jsonify(build_nr=build.build_nr,
                   created=build.created,
                   comment=build.comment)


@api.route('/projects/<int:project_id>/builds', methods=['POST'])
@api.route('/projects/<string:project_name>/builds', methods=['POST'])
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


# TEST RUNS
@api.route('/projects/<int:project_id>/builds/<build_nr>/runs', methods=['POST'])
@api.route('/projects/<string:project_name>/builds/<build_nr>/runs', methods=['POST'])
def create_run(build_nr, project_id=None, project_name=None):
    project = get_project_by_id_or_name(project_id, project_name)
    build = Build.query.filter_by(project_id=project.id, build_nr=build_nr).first_or_404()
    payload = request.json
    status = payload.get("status")
    comment = payload.get("comment")

    run = get_or_create(db.session, TestRun, build_nr=build_nr, status=status)
    run.comment = comment
    db.session.commit()
    return jsonify(id=run.id, comment=run.comment), 201


# Utils

def get_project_by_id_or_name(project_id, project_name):
    project = None
    if project_id:
        project = Project.query.get(project_id)
    elif project_name:
        project = Project.query.filter(Project.name.ilike(project_name)).first()
    return project
