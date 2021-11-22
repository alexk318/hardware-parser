from json import dumps

from flask import Flask, request

from parser_classes import ParserShop, ParserForcecom, ParserTomas
from config import URLS_SHOP, URLS_FORCECOM, URLS_TOMAS

app = Flask(__name__)


@app.route('/', methods=['POST'])
def start_parsing():
    parsing_parameters = request.get_json(force=True)

    hardware = parsing_parameters['hardware']

    use_shop = parsing_parameters['useShop']
    use_forcecom = parsing_parameters['useForcecom']
    use_tomas = parsing_parameters['useTomas']

    data_json = {"shop": None, "forcecom": None, "tomas": None}

    if use_shop:
        parser = ParserShop(URLS_SHOP[hardware])
        data_json['shop'] = parser.get_data()

    if use_forcecom:
        parser = ParserForcecom(URLS_FORCECOM[hardware])
        data_json['forcecom'] = parser.get_data()

    if use_tomas:
        parser = ParserTomas(URLS_TOMAS[hardware])
        data_json['tomas'] = parser.get_data()

    return dumps(data_json)


if __name__ == '__main__':
    app.run(host="192.168.1.110", debug=True)
