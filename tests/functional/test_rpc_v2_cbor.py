# Copyright 2025 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"). You
# may not use this file except in compliance with the License. A copy of
# the License is located at
#
# http://aws.amazon.com/apache2.0/
#
# or in the "license" file accompanying this file. This file is
# distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF
# ANY KIND, either express or implied. See the License for the specific
# language governing permissions and limitations under the License.

from tests import ClientHTTPStubber, patch_load_service_model
from tests.functional.test_useragent import (
    get_captured_ua_strings,
    parse_registered_feature_ids,
)

FAKE_SERVICE_MODEL = {
    "version": "1.0",
    "documentation": "",
    "metadata": {
        "apiVersion": "2020-02-02",
        "endpointPrefix": "otherservice",
        "protocols": ["smithy-rpc-v2-cbor"],
        "protocol": "smithy-rpc-v2-cbor",
        "serviceFullName": "Other Service",
        "serviceId": "otherservice",
        "signatureVersion": "v4",
        "signingName": "otherservice",
        "targetPrefix": "otherservice",
        "uid": "otherservice-2020-02-02",
    },
    "operations": {
        "MockOperation": {
            "name": "MockOperation",
            "http": {"method": "GET", "requestUri": "/"},
            "input": {"shape": "MockOperationRequest"},
            "documentation": "",
        },
    },
    "shapes": {
        "MockOpParam": {
            "type": "string",
        },
        "MockOperationRequest": {
            "type": "structure",
            "required": ["MockOpParam"],
            "members": {
                "MockOpParam": {
                    "shape": "MockOpParam",
                    "documentation": "",
                    "location": "uri",
                    "locationName": "param",
                },
            },
        },
    },
}

FAKE_RULESET = {
    "version": "1.0",
    "parameters": {},
    "rules": [
        {
            "conditions": [],
            "endpoint": {
                "url": "https://otherservice.us-west-2.amazonaws.com/"
            },
            "type": "endpoint",
        },
    ],
}


def test_user_agent_has_cbor_feature_id(patched_session, monkeypatch):
    patch_load_service_model(
        patched_session, monkeypatch, FAKE_SERVICE_MODEL, FAKE_RULESET
    )
    client = patched_session.create_client(
        'otherservice', region_name='us-west-2'
    )
    with ClientHTTPStubber(client) as stub_client:
        stub_client.add_response()
        # The mock CBOR operation registers `'PROTOCOL_RPC_V2_CBOR': 'M'`
        client.mock_operation(MockOpParam='mock-op-param-value')
    ua_string = get_captured_ua_strings(stub_client)[0]
    feature_list = parse_registered_feature_ids(ua_string)
    assert 'M' in feature_list
