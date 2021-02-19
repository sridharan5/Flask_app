from flask import Flask, render_template, request, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from werkzeug.utils import redirect
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, URL
import csv

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'
Bootstrap(app)


class CafeForm(FlaskForm):
    cafe = StringField('Cafe name', validators=[DataRequired()])
    location = StringField('Cafe location on Google Maps (URL)',validators=[DataRequired(), URL()])
    open = StringField('Opening Time e.g.8AM', validators=[DataRequired()])
    close = StringField('Closing Time e.g.5PM', validators=[DataRequired()])
    coffee = SelectField('Coffee Rating', choices=['☕', '☕☕', '☕☕☕', '☕☕☕☕','☕☕☕☕☕'])
    wifi = SelectField('Wifi Strength Rating', choices=['💪', ' 💪 💪', ' 💪 💪 💪', ' 💪 💪 💪 💪', ' 💪 💪 💪 💪 💪'])
    power = SelectField('Power Socket Availability', choices=['🔌', ' 🔌 🔌', ' 🔌 🔌 🔌', ' 🔌 🔌 🔌 🔌', ' 🔌 🔌 🔌 🔌 🔌'])
    submit = SubmitField('Submit')

# all Flask routes below
@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add', methods=['post', 'get'])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        cafe_ = request.form['cafe']
        location_ = request.form['location']
        open_ = request.form['open']
        close_ = request.form['close']
        coffee_ = request.form['coffee']
        wifi_ = request.form['wifi']
        power_ = request.form['power']
        with open('cafe-data.csv', 'a', encoding='UTF8') as fd:
            fd.write(f'\n{cafe_},{location_},{open_},{close_},{coffee_},{wifi_},{power_}')
        return redirect(url_for('cafes'))
    return render_template('add.html', form=form)


@app.route('/cafes')
def cafes():
    with open('cafe-data.csv', newline='', encoding='UTF8') as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)
    return render_template('cafes.html', cafes=list_of_rows)

if __name__ == '__main__':
    app.run(debug=True)
