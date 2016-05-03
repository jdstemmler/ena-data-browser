from flask import Flask, render_template, request, url_for, redirect
import pandas as pd
from dateutil.parser import parse
import datetime

app = Flask(__name__)


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == "POST":
        date = request.form.get('date')
        radar = request.form.get('radar', 'bl')
        if date is not None:
            return redirect(url_for('date_page', date=date, radar=radar))
    else:
        return render_template('index.html')


@app.route('/<date>')
@app.route('/date/<date>')
def redirect_to_date(date):
    return redirect(url_for('date_page', date=date, radar='full'))


@app.route('/<radar>/<date>') #, methods=['POST', 'GET'])
def date_page(date, radar='bl'):

    date_as_dt = parse(date)
    dt_fmt = '%Y-%m-%d'

    date_as_string = date_as_dt.strftime(dt_fmt)

    next_date = (date_as_dt + datetime.timedelta(days=1)).strftime(dt_fmt)
    prev_date = (date_as_dt - datetime.timedelta(days=1)).strftime(dt_fmt)

    s3_prefix = 'https://s3-us-west-2.amazonaws.com/arm-ena-data/figures/'

    # radar_change = request.form.get('radar', None)
    # if radar_change is not None:
    #     radar = radar_change

    args = {'aer':  '{}{}_aerosol.png'.format(s3_prefix, date_as_string),
            'met':  '{}{}_met_{}.png'.format(s3_prefix, date_as_string, radar),
            'rose': '{}{}_windrose.png'.format(s3_prefix, date_as_string),
            'date': date_as_string,
            'next': next_date,
            'prev': prev_date,
            'radar': radar}

    return render_template('date_page.html', **args)


@app.route('/interesting_cases')
def cases():
    # table = pd.read_csv('https://docs.google.com/spreadsheets/d/' +
    #                 '1j-yL-SXwPXMxEzhrx7plkggPYJ6WlHD3EM7gVte7Ba8/' +
    #                 'pub?gid=1851660263&single=true&output=csv',
    #                 names=['tstamp', 'case_date', 'description', 'category'],
    #                 parse_dates=[0,],
    #                 header=0)

    table = pd.read_csv('interesting_cases.csv',
                        names=['tstamp', 'case_date', 'description', 'category'],
                        parse_dates=[0,],
                        header=0)

    table['case_dt'] = table['case_date'].apply(lambda x: datetime.datetime.strptime(x, '%m/%d/%Y'))
    new_table = table.set_index('case_dt')[['description', 'category']].sort_index()

    d = new_table.groupby('category').apply(lambda x: x.to_dict()).to_dict()

    return render_template('interesting_cases.html', cases=d)

if __name__ == '__main__':
    app.run(debug=True, port=8080, host='0.0.0.0')
