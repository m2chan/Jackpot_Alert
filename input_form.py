# Create user input form using Flask WTForms

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, ValidationError
from wtforms.validators import DataRequired, Length, Email, EqualTo, NumberRange
import phonenumbers

class RegistrationForm(FlaskForm):
    
    # Initialize form fields
    lotto_649_threshold = IntegerField('Notify me when the Lotto 6/49 Jackpot exceeds.. (in millions)', render_kw={'placeholder': 'Enter a number between 1 and 20'}, validators=[NumberRange(min=0, max=70, message='Please enter a number between 1 and 70, or enter 0 if you don\'t want to follow Lotto 6/49')])
    lotto_max_threshold = IntegerField('Notify me when the Lotto Max Jackpot exceeds.. (in millions)', render_kw={'placeholder': 'Enter a number between 10 and 70'}, validators=[NumberRange(min=0, max=70, message='Please enter a number between 1 and 70, or enter 0 if you don\'t want to follow Lotto Max')])
    email = StringField('Email address', render_kw={'placeholder': 'name@email.com'}, validators=[DataRequired(), Email()])
    phone = StringField('Phone number (optional)', render_kw={'placeholder': '999-123-4567'})
    lucky_number_bool = BooleanField('Include some lucky numbers in my notification (optional)')
    submit = SubmitField('Subscribe')

    # Extra validation method for phone numbers
    def validate_phone(form, field):
        if not len(field.data):
            pass
        elif len(field.data) > 16:
            raise ValidationError('Invalid phone number.')
        else:
            try:
                input_number = phonenumbers.parse(field.data)
                if not phonenumbers.is_valid_number(input_number):
                    raise ValidationError('Invalid phone number.')
            except:
                try:
                    input_number = phonenumbers.parse("+1"+field.data)
                    if not phonenumbers.is_valid_number(input_number):
                        raise ValidationError('Invalid phone number.')
                except:
                    raise ValidationError('Invalid phone number.')


