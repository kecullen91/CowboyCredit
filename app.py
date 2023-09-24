from flask import Flask, render_template, request, flash
import requests

app = Flask(__name__)
app.secret_key = "AnotherOne"


@app.route("/alloy")


def index():
	return render_template("index.html")

@app.route('/send_api_request', methods=["POST", "GET"])
def send_api_request():
    
    # Get data from the form inputs
    data = {
        'name_first': request.form['name_first'],
        'name_last': request.form['name_last'],
        'address_line_1': request.form['address_line_1'],
        'address_line_2': request.form['address_line_2'],
        'address_city': request.form['address_city'],
        'address_state': request.form['address_state'],
        'address_postal_code': request.form['address_postal_code'],
        'address_country_code': request.form['address_country_code'],
        'document_ssn': request.form['document_ssn'],
        'email_address': request.form['email_address'],
        'birth_date': request.form['birth_date']
    }

    # Print or log the data before sending the request
    print("Data being sent to the API:", data)

    # Define the URL of the Alloy API endpoint
    api_url = 'https://sandbox.alloy.co/v1/evaluations'

    # Set the headers, including the Authorization header with your Alloy API token
    headers = {
        'Authorization': 'Basic eUtaWWVCUEpOdUJPSWc1SWVqR01XcGNFMzNIQldLb1E6SGlwUXIyclB0ZHBEQm1PSlJHdWtXdEdmR1pSQnZNaUo=',
        'Content-Type': 'application/json'
    }

    # Send the POST request using the requests library
    response = requests.post(api_url, json=data, headers=headers)

    # Log the API response details
    print("API response status code:", response.status_code)
    print("API response text:", response.text)

    # Check the response status code and return a response
    if response.status_code in {200, 201, 206}:
        # Check if "outcome" is "Approved" in the response JSON
        response_data = response.json()
        summary = response_data.get('summary', {})
        outcome = summary.get('outcome', '')
        
        if outcome == 'Approved':
            response_message = 'Yeehaw! Your Application to Cowboy Credit was a Success!'
        elif outcome == 'Manual Review':
        	response_message = 'Hold on to your horses! We\'re reviewing your application and will be in touch soon.'
        elif outcome == 'Denied':
        	response_message = 'Sorry Partner, your application was not successful.'

        else:
            response_message = 'Submission Error'
    else:
        response_message = f'API request to Alloy failed with status code: {response.status_code}'
    return render_template("response.html", response_message=response_message)
    

if __name__ == '__main__':
    app.run(debug=True)
