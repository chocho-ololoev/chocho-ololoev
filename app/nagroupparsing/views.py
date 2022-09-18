from flask import flash, redirect, render_template, url_for
from flask_login import login_required
from datetime import datetime

from instance.config import FLASK_CONFIG
from . import nagroupparsing
from .forms import StartParseData
from ..import db
from ..admin.views import check_admin

from ..models import ParsingLog, ParsingTask

@nagroupparsing.route('/nagroupparsing', methods=['GET', 'POST'])
@login_required
# NaGroup Views
def list_parse_log():
    """
    List all groups parsing logs
    """
    check_admin()
    groupparseloglist = ParsingLog.query.all()
    add_parse_task()
    return render_template('nagroupparsing/nagroupparser.html',
                           form=StartParseData(), nagroups=groupparseloglist, title="NaGroups")

def add_parse_task():
    """ adding site link to parse data for the bot"""
    check_admin()
    form = StartParseData()
    if form.validate_on_submit():
        parsing_log = ParsingLog(source_link=form.parse_link.data,
                                 last_update=datetime.now())
        db.session.add(parsing_log)
        db.session.commit()
        flash('Parsing task added')


    else:
        flash('Zalupa')
    return redirect(url_for('nagroupparsing.list_parse_log'))

@nagroupparsing.route('/parsingtask/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def proceedparsingtask(id):
    """
    Edit parsingtask
    """
    check_admin()

    parsingtask = ParsingTask.query.get_or_404(id)

    return render_template('nagroupparsing/parsingtask.html',
                           parsingtask=parsingtask, title="Parsing task")

@nagroupparsing.route('/nagrouptasks', methods=['GET', 'POST'])
@login_required
# NaGroup Views
def list_parsetasks():
    """
    List all groups parsing tasks
    """
    check_admin()
    parsingtasks = ParsingTask.query.all()

    return render_template('nagroupparsing/parsingtasks.html',
                           parsingtasks=parsingtasks, title="Parsing task")