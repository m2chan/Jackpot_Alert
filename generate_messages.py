# Generates text and email messages to send to subscribers

import random
from lotto_data import retrieve_data

def generate_text(lottery, lottery_data, lucky_number):
	'''
	Generate text message to subscriber

	Input arguments:
		lottery: The lottery that the subscriber is following 
		lottery_data: Dictionary containing all the lottery details
		lucky_number: Whether or not the subscriber wants randomly generated numbers in the text
	'''

	# Determine which lottery this text is for and generates text message
	if lottery == 'lotto_649':
		lottery_type = '6/49'
	else:
		lottery_type = 'Max'
	text = 'It\'s time, the next Lotto {} jackpot is ${} Million! Draw date is {}, {}, so get your ticket soon.'.format(lottery_type, lottery_data[lottery]['jackpot'], lottery_data[lottery]['day_of_week'], lottery_data[lottery]['date'])

	# Generates random numbers if the subscriber wanted us to send "lucky numbers" along with their reminder text
	if lucky_number == 1:
		if lottery == 'lotto_649':
			numbers = random.sample(range(1, 50), 6)
			
		else:
			numbers = random.sample(range(1, 50), 7)
		numbers = [str(n) for n in sorted(numbers)]
		numbers = ', '.join(numbers)
		text += ' By the way, we have a good feeling about these numbers.. {}. Good luck!'.format(numbers)

	return text

def generate_email(lottery, lottery_data, lucky_number):
	'''
	Generate emal message to subscriber

	Input arguments:
		lottery: The lottery that the subscriber is following 
		lottery_data: Dictionary containing all the lottery details
		lucky_number: Whether or not the subscriber wants randomly generated numbers in the email
	'''

	# Determine which lottery this email is for and generates email message
	if lottery == 'lotto_649':
		lottery_type = '6/49'
	else:
		lottery_type = 'Max'
	text = '<p>The next Lotto {} jackpot is <b>${} Million!</b> Draw date is <b>{}, {}</b>, so get your ticket soon.</p>\n'.format(lottery_type, 
	lottery_data[lottery]['jackpot'], lottery_data[lottery]['day_of_week'], lottery_data[lottery]['date'])

	# Generates random numbers if the subscriber wanted us to send "lucky numbers" along with their reminder email
	lucky_number_text = ''
	if lucky_number == 1:
		if lottery == 'lotto_649':
			numbers = random.sample(range(1, 50), 6)
			
		else:
			numbers = random.sample(range(1, 50), 7)
		numbers = [str(n) for n in sorted(numbers)]
		numbers = ', '.join(numbers)
		lucky_number_text += '<p>By the way, we have a good feeling about these numbers.. <b>{}</b>.</p>\n'.format(numbers)
	
	# HTML email message
	message = '''
	<!doctype html>
	<html>
	<head>
		<meta name="viewport" content="width=device-width" />
		<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
		<title>Simple Transactional Email</title>
		<style>
		/* -------------------------------------
			GLOBAL RESETS
		------------------------------------- */
		
		/*All the styling goes here*/
		
		img {
			border: none;
			-ms-interpolation-mode: bicubic;
			max-width: 100%; 
		}

		body {
			background-color: #f6f6f6;
			font-family: sans-serif;
			-webkit-font-smoothing: antialiased;
			font-size: 14px;
			line-height: 1.4;
			margin: 0;
			padding: 0;
			-ms-text-size-adjust: 100%;
			-webkit-text-size-adjust: 100%; 
		}

		table {
			border-collapse: separate;
			mso-table-lspace: 0pt;
			mso-table-rspace: 0pt;
			width: 100%; }
			table td {
			font-family: sans-serif;
			font-size: 14px;
			vertical-align: top; 
		}

		/* -------------------------------------
			BODY & CONTAINER
		------------------------------------- */

		.body {
			background-color: #f6f6f6;
			width: 100%; 
		}

		/* Set a max-width, and make it display as block so it will automatically stretch to that width, but will also shrink down on a phone or something */
		.container {
			display: block;
			margin: 0 auto !important;
			/* makes it centered */
			max-width: 600px;
			padding: 10px;
			width: 600px; 
		}

		/* This should also be a block element, so that it will fill 100% of the .container */
		.content {
			box-sizing: border-box;
			display: block;
			margin: 0 auto;
			max-width: 600px;
			padding: 10px; 
		}

		/* -------------------------------------
			HEADER, FOOTER, MAIN
		------------------------------------- */
		.main {
			background: #ffffff;
			border-radius: 3px;
			width: 100%; 
		}

		.wrapper {
			box-sizing: border-box;
			padding: 20px; 
		}

		.content-block {
			padding-bottom: 10px;
			padding-top: 10px;
		}

		.footer {
			clear: both;
			margin-top: 10px;
			text-align: center;
			width: 100%; 
		}
			.footer td,
			.footer p,
			.footer span,
			.footer a {
			color: #999999;
			font-size: 12px;
			text-align: center; 
		}

		/* -------------------------------------
			TYPOGRAPHY
		------------------------------------- */
		h1,
		h2,
		h3,
		h4 {
			color: #000000;
			font-family: sans-serif;
			font-weight: 400;
			line-height: 1.4;
			margin: 0;
			margin-bottom: 30px; 
		}

		h1 {
			font-size: 35px;
			font-weight: 300;
			text-align: center;
			text-transform: capitalize; 
		}

		p,
		ul,
		ol {
			font-family: sans-serif;
			font-size: 14px;
			font-weight: normal;
			margin: 0;
			margin-bottom: 15px; 
		}
			p li,
			ul li,
			ol li {
			list-style-position: inside;
			margin-left: 5px; 
		}

		a {
			color: #3498db;
			text-decoration: underline; 
		}



		/* -------------------------------------
			OTHER STYLES THAT MIGHT BE USEFUL
		------------------------------------- */
		.last {
			margin-bottom: 0; 
		}

		.first {
			margin-top: 0; 
		}

		.align-center {
			text-align: center; 
		}

		.align-right {
			text-align: right; 
		}

		.align-left {
			text-align: left; 
		}

		.clear {
			clear: both; 
		}

		.mt0 {
			margin-top: 0; 
		}

		.mb0 {
			margin-bottom: 0; 
		}

		.preheader {
			color: transparent;
			display: none;
			height: 0;
			max-height: 0;
			max-width: 0;
			opacity: 0;
			overflow: hidden;
			mso-hide: all;
			visibility: hidden;
			width: 0; 
		}

		.powered-by a {
			text-decoration: none; 
		}

		hr {
			border: 0;
			border-bottom: 1px solid #f6f6f6;
			margin: 20px 0; 
		}

		/* -------------------------------------
			RESPONSIVE AND MOBILE FRIENDLY STYLES
		------------------------------------- */
		@media only screen and (max-width: 620px) {
			table[class=body] h1 {
			font-size: 28px !important;
			margin-bottom: 10px !important; 
			}
			table[class=body] p,
			table[class=body] ul,
			table[class=body] ol,
			table[class=body] td,
			table[class=body] span,
			table[class=body] a {
			font-size: 16px !important; 
			}
			table[class=body] .wrapper,
			table[class=body] .article {
			padding: 10px !important; 
			}
			table[class=body] .content {
			padding: 0 !important; 
			}
			table[class=body] .container {
			padding: 0 !important;
			width: 100% !important; 
			}
			table[class=body] .main {
			border-left-width: 0 !important;
			border-radius: 0 !important;
			border-right-width: 0 !important; 
			}
			table[class=body] .btn table {
			width: 100% !important; 
			}
			table[class=body] .btn a {
			width: 100% !important; 
			}
			table[class=body] .img-responsive {
			height: auto !important;
			max-width: 100% !important;
			width: auto !important; 
			}
		}

		@media all {
			.ExternalClass {
			width: 100%; 
			}
			.ExternalClass,
			.ExternalClass p,
			.ExternalClass span,
			.ExternalClass font,
			.ExternalClass td,
			.ExternalClass div {
			line-height: 100%; 
			}
			.apple-link a {
			color: inherit !important;
			font-family: inherit !important;
			font-size: inherit !important;
			font-weight: inherit !important;
			line-height: inherit !important;
			text-decoration: none !important; 
			}
			#MessageViewBody a {
			color: inherit;
			text-decoration: none;
			font-size: inherit;
			font-family: inherit;
			font-weight: inherit;
			line-height: inherit;
			}
			.btn-primary table td:hover {
			background-color: #34495e !important; 
			}
			.btn-primary a:hover {
			background-color: #34495e !important;
			border-color: #34495e !important; 
			} 
		}

		</style>
	</head>
	<body class="">
		<span class="preheader">This is preheader text. Some clients will show this text as a preview.</span>
		<table role="presentation" border="0" cellpadding="0" cellspacing="0" class="body">
		<tr>
			<td>&nbsp;</td>
			<td class="container">
			<div class="content">

				<!-- START CENTERED WHITE CONTAINER -->
				<table role="presentation" class="main">

				<!-- START MAIN CONTENT AREA -->
				<tr>
					<td class="wrapper">
					<table role="presentation" border="0" cellpadding="0" cellspacing="0">
						<tr>
						<td>
							<p>Hi there,</p>
							<p>This is a reminder from Jackpot Alert that the jackpot threshold you set with us has been reached or exceeded.</p> \n'''
	message += text
	if lucky_number_text:
		message += lucky_number_text
	message += '''
	<p>Good luck!</p>
	<p>&#x1F91E;</p>
						</td>
						</tr>
					</table>
					</td>
				</tr>

				<!-- END MAIN CONTENT AREA -->
				</table>
				<!-- END CENTERED WHITE CONTAINER -->

				<!-- START FOOTER -->
				<div class="footer">
				<table role="presentation" border="0" cellpadding="0" cellspacing="0">
					<tr>
					<td class="content-block">
						<br> Don't like these emails? <a href="https://media.giphy.com/media/5xtDarEgBDjEoWo6VRS/giphy.gif">Unsubscribe</a>.
					</td>
					</tr>
					<tr>
					<td class="content-block powered-by">
						Powered by <a href="http://google.com">Jackpot Alert</a>.
					</td>
					</tr>
				</table>
				</div>
				<!-- END FOOTER -->

			</div>
			</td>
			<td>&nbsp;</td>
		</tr>
		</table>
	</body>
	</html>
	'''
	return message

if __name__ == '__main__':
	lottery_data = retrieve_data()
	print(lottery_data)
	print(generate_text('lotto_649', lottery_data, 1))
	print()
	print(generate_text('lotto_max', lottery_data, 1))