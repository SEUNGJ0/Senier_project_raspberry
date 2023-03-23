#! /usr/bin/python2

import time
import sys
import random
import time
import threading
import RPi.GPIO as GPIO


from azure.iot.device import IoTHubDeviceClient, Message, MethodResponse
from hx711 import HX711

CONNECTION_STRING = "HostName=xxx.azure-devices.net;DeviceId=xxx;SharedAccessKey=xxx"

IOT_MSG = '{{"Weight": {weight}, "Device": "1"}}'

def cleanAndExit():
    print("Cleaning...")
    GPIO.cleanup()
    sys.exit()

GPIO.setwarnings(False)
hx = HX711(5, 6)

hx.set_reading_format("MSB", "MSB")

hx.set_reference_unit(630)
hx.reset()
hx.tare()


def iothub_client_init():
    # Create an IoT Hub client
    client = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING)
    return client

def device_method_listener(device_client):
    global INTERVAL
    while True:
        method_request = device_client.receive_method_request()
        print (
            "nMethod callback called with:nmethodName = {method_name}npayload = {payload}".format(
                method_name=method_request.name,
                payload=method_request.payload
            )
        )
        if method_request.name == "SetTelemetryInterval":
            try:
                INTERVAL = int(method_request.payload)
            except ValueError:
                response_payload = {"Response": "Invalid parameter"}
                response_status = 400
            else:
                response_payload = {"Response": "Executed direct method {}".format(method_request.name)}
                response_status = 200
        else:
            response_payload = {"Response": "Direct method {} not defined".format(method_request.name)}
            response_status = 404

        method_response = MethodResponse(method_request.request_id, response_status, payload=response_payload)
        device_client.send_method_response(method_response)


client = iothub_client_init()

while True:
    try:

        val = hx.get_weight(5)

        msg_txt_formatted = IOT_MSG.format(weight=val)
        message = Message(msg_txt_formatted)
        print( "Sending message: {}".format(message) )
        client.send_message(message)
        print( "Message sent" )


        hx.power_down()
        hx.power_up()
        time.sleep(2)

    except KeyboardInterrupt:
        print ( "IoTHubClient sample stopped" )


