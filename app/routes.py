from app import app
from datastore import DataStore
from flask import jsonify, request
from werkzeug.http import HTTP_STATUS_CODES
import time

store = DataStore()

@app.route('/customers', methods=['GET'])
def get_customers():
    page = int(request.args.get('page'))
    per_page = int(request.args.get('per_page'))
    print(page)
    print(per_page)
    customers = store.paginated_collection(page, per_page)
    total = store.get_user_total()
    if customers:
        response = {
            'customers' : customers,
            'meta' : {
                'page': page,
                'per_page': per_page,
                'total': total
            }
        }
        return jsonify(response)
    else:
        return error_response(404, 'customers not found')


@app.route('/customers/<id>', methods=['GET'])
def get_customer(id):
    customer = store.find_user_by_id(int(id))
    if customer:
        return jsonify({'customer': customer})
    else:
        return error_response(404, 'customer not found')

@app.route('/customers/<id>', methods=['DELETE'])
def delete_customer(id):
    customer = store.find_user_by_id(int(id))
    if customer & store.delete_user_by_id(int(id)):
        payload = {'message': 'customer deleted by user_id'}
        response = jsonify(payload)
        response.status_code = 201
        return response
    else:
        return error_response(404, 'customer not found')

@app.route('/customers', methods=['POST'])
def create_customer():
    data = request.get_json()
    potential_customer = data['customer']
    user_id = potential_customer['id']
    user_data = potential_customer['attributes']
    if not store.find_user_by_id(user_id):
        store.create_user(user_data, user_id)
        customer = store.find_user_by_id(user_id)
        if customer:
            return jsonify({'customer': customer})
    else:
        return bad_request("customer already exists")

@app.route('/customers/<id>', methods=['PATCH'])
def update_customer(id):
    customer = store.find_user_by_id(int(id))
    if customer:
        body = request.get_json()
        attrs = body['customer']['attributes']
        update_data = {
            'data': attrs,
            'user_id': id,
            'timestamp': int(time.time())
        }
        updated_customer = store.update_user_attributes(update_data)
        return jsonify({'customer': updated_customer})
    else:
        return bad_request("customer doesn't exist")


def bad_request(message):
    return error_response(400, message)

def error_response(code, message=None):
    payload = {
        'error': HTTP_STATUS_CODES.get(code, 'Unknown error')
    }
    if message:
        payload['message'] = message
    response = jsonify(payload)
    response.status_code = code
    return response

