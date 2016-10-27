from flask import Flask, render_template, request, url_for, redirect, make_response, jsonify, session
import requests
import pandas as pd
from dateutil.parser import parse
import datetime
from collections import OrderedDict
from bs4 import BeautifulSoup

from secret import SECRET
from plot_types import prefix_to_type, type_to_prefix, prefix_labels

app = Flask(__name__)
app.secret_key = SECRET

@app.route('/', methods=['GET',])
def index():
    return render_template('index.html')

@app.route('/favicon.ico')
def favicon():
    return redirect(url_for("static", filename="images/favicon.ico"))

@app.route('/apple-touch-icon-precomposed.png')
@app.route('/apple-touch-icon.png')
def apple_touch():
    return redirect(url_for("static", filename="images/apple-touch-icon-precomposed.png"))

@app.route('/_get_figures_page', methods=['POST',])
def _get_figures_page():
    if request.method == 'POST':
        date = request.form.get('date')
        if date is not None:
            return redirect(url_for('figures_page', date=date))
    else:
        return render_template('index.html')

@app.route('/_get_default_prefix')
def _get_default_prefix():
    default_params = {
        'radar': 'boundary-layer-radar',
        'precip': 'precip',
        'wind': 'wind',
        'rose': 'wind-rose',
        'uhsas': 'uhsas',
        'aerosol': 'aerosol-concentration-linear',
        'scattering': '1um-scattering-linear',
        'ccn': 'ccn',
        'cn': 'cn-log',
        'co': 'co-linear',
        'soundings': [],
              }
    return default_params

@app.route('/_set_session_prefix', methods=['POST',])
def _set_session_prefix():

    new_prefix = request.form.get('new_prefix', None)

    if new_prefix is not None:
        plot_type = prefix_to_type[new_prefix]

        current_prefixes = session['prefixes']
        current_prefixes[plot_type] = new_prefix

        session['prefixes'] = current_prefixes

        return jsonify(plot_type=plot_type, new_prefix=new_prefix)

# @app.route('/_list_soundings', methods=['POST',])
def _list_soundings(url):
    try:
        r = requests.get(url, timeout=2)
        if r.status_code != 200:
            return []

        s = BeautifulSoup(r.content, "html.parser")
        links = s.findAll('a')

        soundings = [a['href'] for a in links if 'sounding' in a['href']]

        return soundings

    except requests.exceptions.Timeout:
        return []

@app.route('/date/<date>', methods=['GET', ])
def figures_page(date):

    if not isinstance(date, datetime.datetime):
        dt = parse(date)
    else:
        dt = date

    global_params = {
        'date': dt,
        'next_day': dt + datetime.timedelta(days=1),
        'prev_day': dt - datetime.timedelta(days=1),
        'date_str': dt.strftime('%Y-%m-%d'),
        'plot_url': 'http://atmos.uw.edu/~jstemm/ena-figures/browser-figures/{}/'.format(dt.strftime('%Y-%m-%d')),
        # 'plot_url': url_for('static', filename='figures/{}/'.format(dt.strftime('%Y-%m-%d')))
    }

    soundings = _list_soundings(global_params['plot_url'])

    if 'prefixes' not in session:
        session['prefixes'] = _get_default_prefix()

    return render_template('new_page_of_figures.html', types=type_to_prefix, labels=prefix_labels, soundings=soundings, **global_params)

@app.route('/worldview/<resource>/<date>')
def worldview_image(resource, date):

    #worldview page
    # https://worldview.earthdata.nasa.gov/?
    # p=geographic&
    # l=MODIS_Aqua_CorrectedReflectance_TrueColor,MODIS_Terra_CorrectedReflectance_TrueColor(hidden),
    #   MODIS_Aqua_CorrectedReflectance_Bands721(hidden),MODIS_Terra_CorrectedReflectance_Bands721(hidden),,
    #   Calipso_Orbit_Asc,Coastlines,,,,,,AMSR2_Cloud_Liquid_Water_Day(hidden),AMSR2_Cloud_Liquid_Water_Night(hidden),
    #   AMSR2_Wind_Speed_Day(hidden),AMSR2_Wind_Speed_Night(hidden),&
    # t=2016-08-19

    # static image
    # http://gibs.earthdata.nasa.gov/image-download?
    # TIME=2016300&
    # extent=extent=-79.875,0,0,60.75&
    # epsg=4326&
    # layers=MODIS_Aqua_CorrectedReflectance_TrueColor,Coastlines&
    # opacities=1,1&
    # worldfile=false&
    # format=image/jpeg&
    # width=909&height=691

    if resource == 'static':

        params = {'base_url': 'http://gibs.earthdata.nasa.gov/image-download',
                  'TIME': datetime.datetime.strptime(date, '%Y-%m-%d').strftime('%Y%j'),
                  'extent': '-79.875,0,0,60.75',
                  'layers': 'MODIS_Aqua_CorrectedReflectance_TrueColor,Coastlines',
                  'opacities': '1,1',
                  'worldfile': 'false',
                  'format': 'image/jpeg',
                  'epsg': 4326,
                  'width': '909',
                  'height': '691'}

        full_url = '{base_url}?TIME={TIME}&extent={extent}&epsg={epsg}&layers={layers}&opacities={opacities}&' \
                   'worldfile={worldfile}&format={format}&width={width}&height={height}'.format(**params)
        return redirect(full_url)

    elif resource == 'dynamic':

        base_url = 'https://worldview.earthdata.nasa.gov/'

        layers = 'MODIS_Aqua_CorrectedReflectance_TrueColor,MODIS_Terra_CorrectedReflectance_TrueColor(hidden),' \
                 'MODIS_Aqua_CorrectedReflectance_Bands721(hidden),MODIS_Terra_CorrectedReflectance_Bands721(hidden),,' \
                 'Calipso_Orbit_Asc,Coastlines,,,,,,AMSR2_Cloud_Liquid_Water_Day(hidden),AMSR2_Cloud_Liquid_Water_Night(hidden),' \
                 'AMSR2_Wind_Speed_Day(hidden),AMSR2_Wind_Speed_Night(hidden),'
        v = '-160.453125,-57.09375,74.390625,78.1875'

        full_url = '{base_url}?p=geographic&l={layers}&t={date}&v={v}'.format(base_url=base_url, layers=layers, date=date, v=v)

        return redirect(full_url)

    else:

        return None

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
