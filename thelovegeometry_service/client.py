import json
import pprint
import time
from http import HTTPStatus

import requests as requests

from thelovegeometry_service import SEMANTICVALIDATED_ENDPOINT, DEFAULT_ENDPOINT, API_URL

SEMANTIC_VALIDATION_REQUIRED: bool = False

INPUTS_TO_SEND = [
    "A loves B but A hates B, A hates B and A loves A.",  # contains every checked errors
    "A hates B, A loves D while B loves C and D hates A.",
    """A loves B but B hates A
    D loves B and C loves A. 
    """,
    """
    A loves B but B hates A and A loves D.
    A hates B, A loves D while B loves C and D hates A.
    A loves B, B loves A and B loves D.
    A loves B but B hates A
    D loves B and C loves A.
    """,
    "A loves B but B hates A",  # invalid one
    ""  # invalid one
]


def call_flask_endpoint(api_full_url: str):
    for input_to_send in INPUTS_TO_SEND:
        result = requests.post(api_full_url, input_to_send)

        print("\n\nInput sent:", input_to_send, "\n\tAPI request resultcode: ", result, "\n\tParsed result:", )
        if result.status_code != HTTPStatus.BAD_REQUEST and result.content:
            pprint.pprint(json.loads(result.content.decode('utf-8')))
        else:
            print(result.content)

        time.sleep(2)


def main():
    print("Api URL:", API_URL)

    if SEMANTIC_VALIDATION_REQUIRED:
        semantic_validated_endpoint_url = API_URL + SEMANTICVALIDATED_ENDPOINT
        call_flask_endpoint(semantic_validated_endpoint_url)
    else:
        default_endpoint_url = API_URL + DEFAULT_ENDPOINT
        call_flask_endpoint(default_endpoint_url)


if __name__ == '__main__':
    main()
