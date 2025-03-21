import json

def lambda_handler(event, context):
    # Parse the query parameters from the event
    query_params = event.get('queryStringParameters', {})
    a = query_params.get('a')
    b = query_params.get('b')
    op = query_params.get('op')

    # Check if the parameters are valid
    if not a or not b or not op:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Missing parameters'})
        }

    # Perform the operation
    result = 0
    if op == 'add':
        result = float(a) + float(b)
    elif op == 'sub':
        result = float(a) - float(b)
    elif op == 'mul':
        result = float(a) * float(b)
    elif op == 'div':
        if float(b) == 0:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'Division by zero'})
            }
        result = float(a) / float(b)
    else:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Invalid operation'})
        }

    # Return the result
    return {
        'statusCode': 200,
        'body': json.dumps(result)
    }
