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
from tests import UACapHTTPStubber, patch_load_service_model

FAKE_SERVICE_MODEL = {
    "version": "2.0",
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

FAKE_RULE_SET = {
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
        patched_session, monkeypatch, FAKE_SERVICE_MODEL, FAKE_RULE_SET
    )
    client = patched_session.create_client(
        'otherservice', region_name='us-west-2'
    )
    with UACapHTTPStubber(client) as stub_client:
        client.mock_operation(MockOpParam='mock-op-param-value')
    uafields = stub_client.captured_ua_string.split(' ')
    feature_field = [field for field in uafields if field.startswith('m/')][0]
    feature_list = feature_field[2:].split(',')
    assert 'M' in feature_list
