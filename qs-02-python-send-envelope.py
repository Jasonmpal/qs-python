# Python3 Quick start example: send an envelope to be signed. The signer is notified by email
# Copyright (c) 2018 by DocuSign, Inc.
# License: The MIT License -- https://opensource.org/licenses/MIT

import base64, os
from docusign_esign import ApiClient, EnvelopesApi, EnvelopeDefinition, Signer, SignHere, Tabs, Recipients, Document

# Settings
# Fill in these constants
#
# Obtain an OAuth access token from https://developers.hqtest.tst/oauth-token-generator
access_token = 'eyJ0eXAiOiJNVCIsImFsZyI6IlJTMjU2Iiwia2lkIjoiNjgxODVmZjEtNGU1MS00Y2U5LWFmMWMtNjg5ODEyMjAzMzE3In0.AQkAAAABAAUABwAAdjCovyvWSAgAALZTtgIs1kgCAFCYSRTxQ4RBlE9V5f7RiHAVAAEAAAAYAAEAAAAFAAAADQAkAAAAZjBmMjdmMGUtODU3ZC00YTcxLWE0ZGEtMzJjZWNhZTNhOTc4EgACAAAABwAAAG1hbmFnZWQLAAAAaW50ZXJhY3RpdmUwAICyZqa_K9ZI.FnMoOgjl0uZgPs2wJhYuh1vvIi8Pmxebjj5SzZUmBNOLWytKqjzGMukC91NF7HJGnuLXiP2lGMLdzg4V_cyBlx7y7f2K_u6o9w71KHBLdJdcqlHyBy1tFW9t75YOTcQBhg0Snq0NhTRv_TQLTeqomre5CMEimAuYMlWCmfX5vFAKTonL7uYUdsLO8Kv_d3Qvel4-Awh4bDkbmedMpbEZyTuYzx7ABEfIw4i79YewFZXmkU9LYA_9WIgO5dpqCKje4coFDJ3KgccdVlIAo_ItBuUu_Pzr1oo22x3RMqfO1n9ZIdji0z5gAP_P_U8DnHbr0Oenig-8RQjGOZh4dhligA'
# Obtain your accountId from demo.docusign.com -- the account id is shown in the drop down on the
# upper right corner of the screen by your picture or the default picture. 
account_id = '3964103'; 
# Recipient Information:
signer_name = 'Larry Smith';
signer_email = 'larry@kluger.com';
# The document you wish to send. Path is relative to the root directory of this repo.
file_name_path = 'demo_documents/World_Wide_Corp_lorem.pdf';
base_path = 'https://demo.docusign.net/restapi'

# Constants
APP_PATH = os.path.dirname(os.path.abspath(__file__))

def send_document_for_signing():
    """
    Sends the document <file_name> to be signed by <signer_name> via <signer_email>
    """

    # Create the component objects for the envelope definition...
    with open(os.path.join(APP_PATH, file_name_path), "rb") as file:
        content_bytes = file.read()
    base64_file_content = base64.b64encode(content_bytes).decode('ascii')

    document = Document( # create the DocuSign document object 
        document_base64 = base64_file_content, 
        name = 'Example document', # can be different from actual file name
        file_extension = 'pdf', # many different document types are accepted
        document_id = 1 # a label used to reference the doc
    )

    sign_here = SignHere( # DocuSign SignHere field/tab
        document_id = '1', page_number = '1', recipient_id = '1', tab_label = 'SignHereTab',
        x_position = '195', y_position = '147')

    signer = Signer( # The signer
        email = signer_email, name = signer_name, recipient_id = "1", routing_order = "1",
        tabs = Tabs(sign_here_tabs = [sign_here]) # The Tabs object wants arrays of the different field/tab types
    )

    # Next, create the top level envelope definition and populate it.
    envelope_definition = EnvelopeDefinition(
        email_subject = "Please sign this document sent from the Python SDK",
        documents = [document], # The order in the docs array determines the order in the envelope
        recipients = Recipients(signers = [signer]), # The Recipients object wants arrays for each recipient type
        status = "sent" # requests that the envelope be created and sent.
    )
    
    # Ready to go: send the envelope request
    api_client = ApiClient()
    api_client.host = base_path
    api_client.set_default_header("Authorization", "Bearer " + access_token)

    envelope_api = EnvelopesApi(api_client)
    results = envelope_api.create_envelope(account_id, envelope_definition=envelope_definition)
    return results

# Mainline
results = send_document_for_signing()
print("\nEnvelope status: " + results.status + ". Envelope ID: " + results.envelope_id + "\n")
