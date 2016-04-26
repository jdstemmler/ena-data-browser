from flask import Flask, render_template, request, url_for, redirect
from dateutil.parser import parse
import datetime

app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == "POST":
        result = request.form.get('date')
        if result is not None:
            return redirect(url_for('date_page', date=result))
    else:
        return render_template('index.html')
    # return "<h1 style='color:blue'>Hello World!!</h1>"

@app.route('/date/<date>')
def date_page(date):

    date_as_dt = parse(date)
    dt_fmt = '%Y-%m-%d'

    date_as_string = date_as_dt.strftime(dt_fmt)

    next_date = (date_as_dt + datetime.timedelta(days=1)).strftime(dt_fmt)
    prev_date = (date_as_dt - datetime.timedelta(days=1)).strftime(dt_fmt)

    aer_figure = url_for('static', filename='figures/{}_aerosol.png'.format(date_as_string))
    met_figure = url_for('static', filename='figures/{}_met.png'.format(date_as_string))

    args = {'aer': aer_figure,
            'met': met_figure,
            'date': date_as_string,
            'next': next_date,
            'prev': prev_date}

    return render_template('date_page.html', **args)

if __name__ == '__main__':
    app.run(debug=True, port=8080)
