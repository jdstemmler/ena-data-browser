from flask import Flask, render_template, request, url_for, redirect
import pandas as pd
from dateutil.parser import parse
import datetime
from collections import OrderedDict

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

    date = parse(date)
    dt_fmt = '%Y %b %d'
    s3_fmt = '%Y-%m-%d'
    link_fmt = '%Y-%b-%d'

    date_as_string = date.strftime(s3_fmt)

    next_date = (date + datetime.timedelta(days=1)) # .strftime(dt_fmt)
    prev_date = (date - datetime.timedelta(days=1)) # .strftime(dt_fmt)

    s3_prefix = 'https://s3-us-west-2.amazonaws.com/arm-ena-data/figures/'

    # radar_change = request.form.get('radar', None)
    # if radar_change is not None:
    #     radar = radar_change

    args = {'aer':  date.strftime('{}{}_aerosol.png'.format(s3_prefix, s3_fmt)).lower(),
            'met':  date.strftime('{}{}_met_{}.png'.format(s3_prefix, s3_fmt, radar)).lower(),
            'rose': date.strftime('{}{}_windrose.png'.format(s3_prefix, s3_fmt)).lower(),
            'dates': (prev_date.strftime(link_fmt), date.strftime(link_fmt), next_date.strftime(link_fmt)),
            'current': date_as_string,
            'next': next_date.strftime(dt_fmt),
            'prev': prev_date.strftime(dt_fmt),
            'radar': radar}

    return render_template('new_date_page.html', **args)


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

    grouped = new_table.groupby('category')
    sorted_categories = grouped.count().sort_values('description', ascending=False)

    d = OrderedDict()
    for i, j in sorted_categories.iterrows():
        d[i] = grouped.get_group(i).to_dict()

    #d = new_table.groupby('category').apply(lambda x: x.to_dict()).to_dict()

    return render_template('interesting_cases.html', cases=d)

if __name__ == '__main__':
    # app.run(debug=True, port=8080, host='0.0.0.0')
    app.run(debug=True, port=8080)
