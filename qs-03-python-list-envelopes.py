# Python3 Quick start example: list envelopes in the user's account
# Copyright (c) 2018 by DocuSign, Inc.
# License: The MIT License -- https://opensource.org/licenses/MIT

import base64, os
from docusign_esign import ApiClient, EnvelopesApi
import pendulum # pip install pendulum
import pprint

# Settings
# Fill in these constants
#
# Obtain an OAuth access token from https://developers.hqtest.tst/oauth-token-generator
access_token = 'eyJ0eXAiOiJNVCIsImFsZyI6IlJTMjU2Iiwia2lkIjoiNjgxODVmZjEtNGU1MS00Y2U5LWFmMWMtNjg5ODEyMjAzMzE3In0.AQkAAAABAAUABwCAHwOwfizWSAgAgF8mvsEs1kgCAFCYSRTxQ4RBlE9V5f7RiHAVAAEAAAAYAAEAAAAFAAAADQAkAAAAZjBmMjdmMGUtODU3ZC00YTcxLWE0ZGEtMzJjZWNhZTNhOTc4EgACAAAABwAAAG1hbmFnZWQLAAAAaW50ZXJhY3RpdmUwAIDFoK1-LNZI.JgIKrks7B_wSJ_7l5ojXFgC7B1bedlRh-6jCOFMbdAG73EcYGjFdAQAaiSvQcJlWmE-k-KPcZuufwE2R_1xvueaWxPWujNC7_30isDYw8b9cojcTuEa5nAACELtrdLHuADHGY2oiOdJSbfiWiw8fIArWE6EAC2L707J7Kg6u0n8IRq0OD3Brua4U68ehjGdQi7_Py9D76gjLVjWOnFjYVCRe0N13Rg05x_MYMBPxF3CnV8MiNdNwQ4H5CTouJ41lGeBxrkEVcO1qg7A9sn41jS1Mjz2g2JKAd8HrQ9LSz4pRL3D6vEs03_xs6y8d4BU-j3ZoHiTzv3GxsZyZIYkGXA'
# Obtain your accountId from demo.docusign.com -- the account id is shown in the drop down on the
# upper right corner of the screen by your picture or the default picture. 
account_id = '3964103'; 
base_path = 'https://demo.docusign.net/restapi'

def list_envelopes():
    """
    Lists the user's envelopes created in the last 10 days
    """
    
    #
    # Step 1. Prepare the options object
    #
    from_date = pendulum.now().subtract(days=10).to_iso8601_string()
    #
    # Step 2. Get and display the results
    # 
    api_client = ApiClient()
    api_client.host = base_path
    api_client.set_default_header("Authorization", "Bearer " + access_token)

    envelope_api = EnvelopesApi(api_client)
    results = envelope_api.list_status_changes(account_id, from_date = from_date)
    return results

# Mainline
results = list_envelopes()
print("\nEnvelopes:\n")
pprint.pprint(results, indent=4, width=80)

