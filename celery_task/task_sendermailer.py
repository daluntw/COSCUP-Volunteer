from __future__ import absolute_import
from __future__ import unicode_literals

from celery.utils.log import get_task_logger
from celery_task.celery import app
from markdown import markdown
from module.sender import SenderMailerCOSCUP
from module.sender import SenderMailerVolunteer

logger = get_task_logger(__name__)


@app.task(bind=True, name='sender.mailer.start',
    autoretry_for=(Exception, ), retry_backoff=True, max_retries=5,
    routing_key='cs.sender.mailer.start', exchange='COSCUP-SECRETARY')
def sender_mailer_start(sender, **kwargs):
    '''campaign_data, team, uids, layout'''
    campaign_data = kwargs['campaign_data']
    team_name = kwargs['team_name']
    user_datas = kwargs['user_datas']
    layout = kwargs['layout']
    source = kwargs.get('source')

    for user_data in user_datas:
        sender_mailer_start_one.apply_async(
                kwargs={'campaign_data': campaign_data, 'team_name': team_name, 'user_data': user_data, 'layout': layout, 'source': source})


@app.task(bind=True, name='sender.mailer.start.one',
    autoretry_for=(Exception, ), retry_backoff=True, max_retries=5,
    routing_key='cs.sender.mailer.start.one', exchange='COSCUP-SECRETARY')
def sender_mailer_start_one(sender, **kwargs):
    campaign_data = kwargs['campaign_data']
    team_name = kwargs['team_name']
    user_data = kwargs['user_data']
    layout = kwargs['layout']
    source = kwargs['source']

    if layout == '1':
        sender_template = SenderMailerVolunteer
    elif layout == '2':
        sender_template = SenderMailerCOSCUP

    sender_mailer = sender_template(
            subject=campaign_data['mail']['subject'],
            content={'preheader': campaign_data['mail']['preheader'],
                     'body': markdown(campaign_data['mail']['content']),
                     'send_by': team_name, },
            source=source,
            )

    sender_mailer.send(
        to_list=[{'name': user_data['name'],
                  'mail': user_data['mail']}, ],
        data=user_data,
    )