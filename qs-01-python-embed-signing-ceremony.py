# Python3 Quick start example: embedded signing ceremony.
# Copyright (c) 2018 by DocuSign, Inc.
# License: The MIT License -- https://opensource.org/licenses/MIT

import base64, os
from flask import Flask, request, redirect
from docusign_esign import ApiClient, EnvelopesApi, EnvelopeDefinition, Signer, SignHere, Tabs, Recipients, Document, RecipientViewRequest

# Settings
# Fill in these constants
#
# Obtain an OAuth access token from https://developers.docusign.com/oauth-token-generator
access_token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImtpZCI6IjY4MTg1ZmYxLTRlNTEtNGNlOS1hZjFjLTY4OTgxMjIwMzMxNyJ9.eyJUb2tlblR5cGUiOjUsIklzc3VlSW5zdGFudCI6MTU3OTgxODczOCwiZXhwIjoxNTc5ODQ3NTM4LCJVc2VySWQiOiIyZjE0YWI4Ni0wZGZkLTQ5NDctODZmMS01NjQxY2E2MGVlY2UiLCJzaXRlaWQiOjEsInNjcCI6WyJzaWduYXR1cmUiLCJjbGljay5tYW5hZ2UiLCJvcmdhbml6YXRpb25fcmVhZCIsInJvb21fZm9ybXMiLCJncm91cF9yZWFkIiwicGVybWlzc2lvbl9yZWFkIiwidXNlcl9yZWFkIiwidXNlcl93cml0ZSIsImFjY291bnRfcmVhZCIsImRvbWFpbl9yZWFkIiwiaWRlbnRpdHlfcHJvdmlkZXJfcmVhZCIsImR0ci5yb29tcy5yZWFkIiwiZHRyLnJvb21zLndyaXRlIiwiZHRyLmRvY3VtZW50cy5yZWFkIiwiZHRyLmRvY3VtZW50cy53cml0ZSIsImR0ci5wcm9maWxlLnJlYWQiLCJkdHIucHJvZmlsZS53cml0ZSIsImR0ci5jb21wYW55LnJlYWQiLCJkdHIuY29tcGFueS53cml0ZSJdLCJhdWQiOiJmMGYyN2YwZS04NTdkLTRhNzEtYTRkYS0zMmNlY2FlM2E5NzgiLCJhenAiOiJmMGYyN2YwZS04NTdkLTRhNzEtYTRkYS0zMmNlY2FlM2E5NzgiLCJpc3MiOiJodHRwczovL2FjY291bnQtZC5kb2N1c2lnbi5jb20vIiwic3ViIjoiMmYxNGFiODYtMGRmZC00OTQ3LTg2ZjEtNTY0MWNhNjBlZWNlIiwiYW1yIjpbImludGVyYWN0aXZlIl0sImF1dGhfdGltZSI6MTU3OTgxODczNiwicHdpZCI6ImY3YzM0NzY0LTg0NjgtNGZlYy05ZjIxLWYzMDlmNGI2YzVjZiJ9.sqbZh1qr_kirVIoOduaqIwiSBS_Np4jo6oxZjQQT2DX2BI3-ZrAOZLHCyca-z8v6n6nCGUE10L6mt2n7qrC9fU_Vb040h3p4Ae6rAG0L974HJS80k6n0Yff7R-FNQpRllJh4rEhPyp9qXhZtTYoOqXkE4WiGgm3LJTuIhxe94Sb7mYIIgD3ehZOwKnG5P52zPYg07IsRrdSGkVgSuBInYy9ai_QrWlPJeSaDFGyIIINqWScZTbInvhzO32xgwZ68onYb3gWfRP7qWQNo55gmXubUiCj2xpGlCj2aTm2oaR0ev-uZ0KnVivS1x9MB2FOpFadi_MXQXjArsTgZYk4xaA'
# Obtain your accountId from demo.docusign.com -- the account id is shown in the drop down on the
# upper right corner of the screen by your picture or the default picture. 
account_id = '9872080'
# Recipient Information:
signer_name = 'Joe Schmoe'
signer_email = 'jasonmpal@gmail.com'
# The document you wish to send. Path is relative to the root directory of this repo.
file_name_path = 'demo_documents/World_Wide_Corp_lorem.pdf'
# The url of this web application
base_url = 'http://localhost:5000'
client_user_id = '123' # Used to indicate that the signer will use an embedded
                       # Signing Ceremony. Represents the signer's userId within
                       # your application.
authentication_method = 'None' # How is this application authenticating
                               # the signer? See the `authenticationMethod' definition
                               # https://developers.docusign.com/esign-rest-api/reference/Envelopes/EnvelopeViews/createRecipient

# The API base_path
base_path = 'https://demo.docusign.net/restapi'

# Set FLASK_ENV to development if it is not already set
if 'FLASK_ENV' not in os.environ:
    os.environ['FLASK_ENV'] = 'development'

# Constants
APP_PATH = os.path.dirname(os.path.abspath(__file__))

def embedded_signing_ceremony():
    """
    The document <file_name> will be signed by <signer_name> via an
    embedded signing ceremony.
    """

    #
    # Step 1. The envelope definition is created.
    #         One signHere tab is added.
    #         The document path supplied is relative to the working directory
    #
    with open(os.path.join(APP_PATH, file_name_path), "rb") as file:
        content_bytes = file.read()
    base64_file_content = base64.b64encode(content_bytes).decode('ascii')

    # Create the document model
    document = Document( # create the DocuSign document object 
        document_base64 = base64_file_content, 
        name = 'Example document', # can be different from actual file name
        file_extension = 'pdf', # many different document types are accepted
        document_id = 1 # a label used to reference the doc
    )

    # Create the signer recipient model 
    signer = Signer( # The signer
        email = signer_email, name = signer_name, recipient_id = "1", routing_order = "1",
        client_user_id = client_user_id, # Setting the client_user_id marks the signer as embedded
    )

    # Create a sign_here tab (field on the document)
    sign_here = SignHere( # DocuSign SignHere field/tab
        document_id = '1', page_number = '1', recipient_id = '1', tab_label = 'SignHereTab',
        x_position = '195', y_position = '147')

    # Add the tabs model (including the sign_here tab) to the signer
    signer.tabs = Tabs(sign_here_tabs = [sign_here]) # The Tabs object wants arrays of the different field/tab types

    # Next, create the top level envelope definition and populate it.
    envelope_definition = EnvelopeDefinition(
        email_subject = "Please sign this document sent from the Python SDK",
        documents = [document], # The order in the docs array determines the order in the envelope
        recipients = Recipients(signers = [signer]), # The Recipients object wants arrays for each recipient type
        status = "sent" # requests that the envelope be created and sent.
    )
    
    #
    #  Step 2. Create/send the envelope.
    #
    api_client = ApiClient()
    api_client.host = base_path
    api_client.set_default_header("Authorization", "Bearer " + access_token)

    envelope_api = EnvelopesApi(api_client)
    results = envelope_api.create_envelope(account_id, envelope_definition=envelope_definition)

    #
    # Step 3. The envelope has been created.
    #         Request a Recipient View URL (the Signing Ceremony URL)
    #
    envelope_id = results.envelope_id
    recipient_view_request = RecipientViewRequest(
        authentication_method = authentication_method, client_user_id = client_user_id,
        recipient_id = '1', return_url = base_url + '/dsreturn',
        user_name = signer_name, email = signer_email
    )

    results = envelope_api.create_recipient_view(account_id, envelope_id,
        recipient_view_request = recipient_view_request)
    
    #
    # Step 4. The Recipient View URL (the Signing Ceremony URL) has been received.
    #         Redirect the user's browser to it.
    #
    return results.url


# Mainline
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def homepage():
    if request.method == 'POST':
        return redirect(embedded_signing_ceremony(), code=302)
    else:
        return '''
            <html lang="en"><body><form action="{url}" method="post">
            <input type="submit" value="Sign the document!"
                style="width:13em;height:2em;background:#1f32bb;color:white;font:bold 1.5em arial;margin: 3em;"/>
            </form></body>
        '''.format(url=request.url)
@app.route('/dsreturn', methods=['GET'])
def dsreturn():
    return '''
        <html lang="en"><body><p>The signing ceremony was completed with
          status {event}</p>
          <p>This page can also implement post-signing processing.</p></body>
    '''.format(event=request.args.get('event'))

app.run()
