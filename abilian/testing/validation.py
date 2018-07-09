# coding=utf-8
from __future__ import absolute_import, print_function, unicode_literals

import json
import os
import subprocess
from tempfile import NamedTemporaryFile

import requests
from flask import Response, current_app, request
from hyperlink import URL

SKIPPED_PATHS = [
    # FIXME: later
    "/admin/settings"
]


class ValidationError(AssertionError):
    pass


def validate_response(response):
    assert_valid(response)
    return response


def assert_valid(response):
    # type: (Response) -> None
    if response.direct_passthrough:
        return

    data = response.data
    assert isinstance(data, bytes)
    # assert response.status_code in [200, 302, 401]

    if response.status_code == 302:
        return

    if URL.from_text(request.url).path in SKIPPED_PATHS:
        return

    if response.mimetype == "text/html":
        assert_html_valid(response)

    elif response.mimetype == "application/json":
        assert_json_valid(response)

    else:
        raise AssertionError("Unknown mime type: " + response.mimetype)

    return


def assert_html_valid(response):
    assert_html_valid_using_htmlhint(response)
    assert_html_valid_using_external_service(response)


def assert_html_valid_using_htmlhint(response):
    with NamedTemporaryFile() as tmpfile:
        tmpfile.write(response.data)
        tmpfile.flush()
        try:
            subprocess.check_output(["htmlhint", tmpfile.name])
        except subprocess.CalledProcessError as e:
            print("htmllhint output:")
            print(e.output)
            msg = "HTML was not valid for URL: {}".format(request.url)
            raise ValidationError(msg)


def assert_html_valid_using_external_service(response):
    config = current_app.config
    validator_url = config.get("VALIDATOR_URL") or os.environ.get("VALIDATOR_URL")

    if not validator_url:
        return

    validator_response = requests.post(
        validator_url + "?out=json",
        response.data,
        headers={"Content-Type": response.mimetype},
    )

    body = validator_response.json()

    for message in body["messages"]:
        if message["type"] == "error":
            detail = "on line {} [{}]\n{}".format(
                message["lastLine"], message["extract"], message["message"]
            )
            msg = "Got a validation error for {}:\n{}".format(request.url, detail)
            raise ValidationError(msg)


def assert_json_valid(response):
    try:
        json.loads(response.data)
    except BaseException:
        msg = "JSON was not valid for URL: {}".format(request.url)
        raise ValidationError(msg)
