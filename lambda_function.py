import json
import boto3
import uuid
from decimal import Decimal

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('WaterReports')


class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return super().default(obj)


def lambda_handler(event, context):
    method = event.get('requestContext', {}).get('http', {}).get('method', 'POST')

    if method == 'GET':
        return handle_get()
    else:
        return handle_post(event)


def handle_get():
    try:
        result = table.scan()
        items = result.get('Items', [])
        # Drop photo data from the list response to keep it light;
        # the map only needs lat/lng/severity/timestamp per pin.
        slim_items = [
            {
                'reportID': i.get('reportID'),
                'lat': i.get('lat'),
                'lng': i.get('lng'),
                'severity': i.get('severity'),
                'timestamp': i.get('timestamp')
            }
            for i in items
        ]
        return response(200, {'reports': slim_items}, cls=DecimalEncoder)
    except Exception as e:
        return response(500, {'error': str(e)})


def handle_post(event):
    try:
        body = json.loads(event.get('body', '{}'))

        lat = body.get('lat')
        lng = body.get('lng')
        severity = body.get('severity')
        photo = body.get('photo')  # base64 data URL, or None
        timestamp = body.get('timestamp')

        if lat is None or lng is None or not severity:
            return response(400, {'error': 'Missing required fields: lat, lng, severity'})

        item = {
            'reportID': str(uuid.uuid4()),
            'lat': Decimal(str(lat)),
            'lng': Decimal(str(lng)),
            'severity': severity,
            'timestamp': timestamp
        }

        # Only store photo if present, and only a reasonable size
        # (DynamoDB items are capped at 400KB total)
        if photo and len(photo) < 350000:
            item['photo'] = photo

        table.put_item(Item=item)

        return response(200, {'message': 'Report saved', 'reportID': item['reportID']})

    except Exception as e:
        return response(500, {'error': str(e)})


def response(status_code, body_dict, cls=None):
    return {
        'statusCode': status_code,
        'headers': {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Methods': 'GET, POST, OPTIONS'
        },
        'body': json.dumps(body_dict, cls=cls) if cls else json.dumps(body_dict)
    }
