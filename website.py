# Flask web app

from flask import Flask, render_template, url_for, flash, redirect
from input_form import RegistrationForm
import sqlite3
from database import create_connection, create_subscriber

app = Flask(__name__)

app.config['SECRET_KEY'] = config.flask_secret_key

# Home page where a user can subscribe for updates
@app.route('/', methods=['GET', 'POST'])
def home():

    # Create an instance of the registration form
    form = RegistrationForm()

    # If the form has been validated and submitted
    if form.validate_on_submit():

        # Proceed to add new subscriber to the database
        database = 'subscribers.db'
        conn = create_connection(database)

        # Prepare user inputed date for database insertion
        subscriber_data = []
        subscriber_data.append(form.email.data)
        
        if not form.phone.data:
            subscriber_data.append(0)
        else:
            subscriber_data.append(form.phone.data)

        if form.lotto_649_threshold.data:
            subscriber_data.extend([1, form.lotto_649_threshold.data])
        else:
            subscriber_data.extend([0, 0])

        if form.lotto_max_threshold.data:
            subscriber_data.extend([1, form.lotto_max_threshold.data])
        else:
            subscriber_data.extend([0, 0])

        if form.lucky_number_bool.data:
            subscriber_data.append(1)
        else:
            subscriber_data.append(0)

        # Create subscriber
        create_subscriber(conn, subscriber_data)

        # Rediret user to "Success" page
        return redirect(url_for('success'))
    
    return render_template('home.html', form=form)

# Success page after the user has successfully subscribed
@app.route('/success')
def success():
    return render_template('success.html')

if __name__ == '__main__':
    app.run(debug=True)
    