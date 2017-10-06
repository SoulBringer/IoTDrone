from __future__ import print_function

import boto3
import json


def respond(err, res=None):
    return {
        'statusCode': '400' if err else '200',
        'body': err.message if err else json.dumps(res),
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
        },
    }


def lambda_handler(event, context):
    #print("Received event: " + json.dumps(event, indent=2))

    operation = event['httpMethod']
    if (operation == 'GET'):
        table = boto3.resource('dynamodb').Table('drone_table')
        attitude = table.get_item(Key={"mavpackettype": "ATTITUDE"})["Item"]
        optical_flow_rad = table.get_item(
            Key={"mavpackettype": "OPTICAL_FLOW_RAD"})["Item"]

        response = {
            'roll': float(attitude["roll"]),
            'pitch': float(attitude["pitch"]),
            'altitude': float(optical_flow_rad["distance"]),
            'heading': float(attitude["yaw"]),
            'offset_x': float(optical_flow_rad["integrated_x"]),
            'offset_y': float(optical_flow_rad["integrated_y"])
        }
        return respond(None, response)

    return respond(ValueError('Unsupported method "{}"'.format(operation)))
