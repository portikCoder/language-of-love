import json
import logging
from http import HTTPStatus
from typing import Any

from flask import Flask, request, Response
from flask_restx import Api, Resource

from thelovegeometry.love_story_semantic_validator import LoveStorySemanticValidator
from thelovegeometry.parser_executor import parse_input_text
from thelovegeometry_service import HOST, PORT, BASE_API_ENDPOINT, SEMANTICVALIDATED_ENDPOINT
from thelovegeometry_service.utils import clean_request_text_input

app = Flask(__name__)
api = Api(app=app,
          version="1.0",
          title="Flask API",
          description="API solution dedicated for the You guys!",
          prefix=f"/{BASE_API_ENDPOINT}", )

name_space = api.namespace('', description='All the endpoints here')
api.add_namespace(name_space)


# this is a view, so should be inside the views.py
@name_space.route('/', methods=['POST'])
class LoveStoryParser(Resource):

    def post(self):
        input_: Any = request.get_data()
        if not input_:
            return Response('There is no input given!', status=HTTPStatus.BAD_REQUEST)

        logging.debug(f'input for "{self.post}" is "{input_}"')

        try:
            parsed_story = parse_input_text(input_text=clean_request_text_input(input_))
        except SyntaxError as se:
            logging.debug(str(se))
            return Response('The input is NOT VALID!', status=HTTPStatus.BAD_REQUEST)
        except Exception as e:
            logging.debug(e)
            return Response('Strange issue happened!', status=HTTPStatus.INTERNAL_SERVER_ERROR)

        return Response(str(json.dumps(parsed_story.__dict__(), indent=4)),
                        status=HTTPStatus.OK,
                        mimetype='application/json')


# this is a view, so should be inside the views.py
@name_space.route(SEMANTICVALIDATED_ENDPOINT, methods=['POST'])
class LoveStoryParser(Resource):

    def post(self):
        input_: Any = request.get_data()
        if not input_:
            return Response('There is no input given!', status=HTTPStatus.BAD_REQUEST)

        logging.debug(f'input for "{self.post}" is "{input_}"')

        try:
            parsed_story = parse_input_text(input_text=clean_request_text_input(input_))
        except SyntaxError as se:
            logging.debug(str(se))
            return Response('The input is NOT VALID!', status=HTTPStatus.BAD_REQUEST)
        except Exception as e:
            logging.debug(e)
            return Response('Strange issue happened!', status=HTTPStatus.INTERNAL_SERVER_ERROR)

        error_messages = [{love_states.__str__(): messages} for love_states, messages in
                          LoveStorySemanticValidator(parsed_story).validate_and_get_brokens()]

        if error_messages:
            # Forgive me: I do know, my error differentiation is not the best, as it is now inconsistent compared to the case for eg. when the sentence has no '.' ending
            return Response(str(json.dumps(error_messages, indent=4)),
                            status=HTTPStatus.CONFLICT,
                            mimetype='application/json')

        return Response(str(json.dumps(parsed_story.__dict__(), indent=4)),
                        status=HTTPStatus.OK,
                        mimetype='application/json')


if __name__ == '__main__':
    # i know, we all know, should use a WSGI server instead this dumb run
    app.run(debug=False, host=HOST, port=PORT)
else:
    app.run(host='0.0.0.0')
