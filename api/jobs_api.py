from datetime import datetime

import flask
from flask import jsonify, make_response, request

from data import db_session
from data.jobs import Jobs
from data.users import User

blueprint = flask.Blueprint(
    'jobs_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/jobs')
def get_jobs():
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).all()

    return jsonify(
        {
            'jobs':
                [job.to_dict(
                    only=(
                        'id', 'team_leader_id', 'job', 'work_size',
                        'collaborators', 'start_date', 'end_date',
                        'is_finished'
                    ))
                    for job in jobs]
        }
    )


@blueprint.route('/api/jobs/<int:job_id>', methods=['GET'])
def get_one_jobs(job_id):
    db_sess = db_session.create_session()
    job = db_sess.query(Jobs).get(job_id)
    if not job:
        return make_response(jsonify({'error': 'Not found'}), 404)
    return jsonify(
        {
            'jobs': [job.to_dict(only=(
                'id', 'team_leader_id', 'job', 'work_size',
                'collaborators', 'start_date', 'end_date',
                'is_finished'))]
        }
    )


@blueprint.route("/api/jobs/", methods=["POST"])
def create_job():
    if not request.json:
        return make_response(jsonify({'error': 'Empty request'}), 400)
    allowed_fields = ["team_leader_id", "job", "work_size", "collaborators", "is_finished"]
    if not all(key in request.json for key in allowed_fields):
        return make_response(jsonify({'error': 'Missing fields'}), 400)
    db_sess = db_session.create_session()
    start_date = request.json.get("start_date")
    if start_date:
        start_date = datetime.fromisoformat(start_date)
    end_date = request.json.get("end_date")
    if end_date:
        end_date = datetime.fromisoformat(end_date)
    job = Jobs(
        team_leader_id=request.json["team_leader_id"],
        job=request.json["job"],
        work_size=request.json["work_size"],
        collaborators=request.json["collaborators"],
        start_date=start_date,
        end_date=end_date,
        is_finished=request.json["is_finished"]
    )
    if not db_sess.query(User).filter(User.id == job.team_leader_id).first():
        return make_response(jsonify({'error': 'team_leader_id unknown'}), 400)
    db_sess.add(job)
    db_sess.commit()
    return jsonify(
        {
            'Success': 'OK',
            'id': job.id
        })


@blueprint.route("/api/jobs/<int:job_id>", methods=["DELETE"])
def delete_job(job_id):
    db_sess = db_session.create_session()
    job: Jobs = db_sess.get(Jobs, job_id)
    if not job:
        return make_response(jsonify({'error': 'Not found'}), 404)
    db_sess.delete(job)
    db_sess.commit()
    return jsonify({'success': 'OK'})


@blueprint.route("/api/jobs/<int:job_id>", methods=["PUT"])
def edit_job(job_id):
    db_sess = db_session.create_session()
    job: Jobs = db_sess.get(Jobs, job_id)
    if not job:
        return make_response(jsonify({'error': 'Not found'}), 404)
    if not request.json:
        return make_response(jsonify({'error': 'Empty request'}), 400)
    allowed_fields = ["team_leader_id", "job", "work_size", "collaborators", "start_date",
                      "end_date", "is_finished"]
    if not all(key in request.json for key in allowed_fields):
        return make_response(jsonify({'error': 'Missing fields'}), 400)
    start_date = request.json["start_date"]
    if start_date:
        start_date = datetime.fromisoformat(start_date)
    end_date = request.json["end_date"]
    if end_date:
        end_date = datetime.fromisoformat(end_date)
    job.team_leader_id = request.json["team_leader_id"]
    job.job = request.json["job"]
    job.work_size = request.json["work_size"]
    job.collaborators = request.json["collaborators"]
    job.start_date = start_date
    job.end_date = end_date
    job.is_finished = request.json["is_finished"]
    db_sess.commit()
    return jsonify({'success': 'OK'})
