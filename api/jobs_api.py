import flask
from flask import jsonify

from data import db_session
from data.jobs import Jobs

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
