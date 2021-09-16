import time
from counterfit_shims_grove.adc import ADC
from counterfit_shims_grove.grove_relay import GroveRelay
import json
from azure.iot.device import IoTHubDeviceClient, Message, MethodResponse
from counterfit_connection import CounterFitConnection

connection_string = ""
device_client = None
relay = None
adc = None

def initialise(new_connection_string):
    if not new_connection_string:
        raise ValueError('connection string empty!')
    connection_string = new_connection_string

def connect():
    CounterFitConnection.init('127.0.0.1', 5000)
    adc = ADC()
    relay = GroveRelay(5)

    device_client = IoTHubDeviceClient.create_from_connection_string(connection_string)

    print('Connecting')
    device_client.connect()
    print('Connected')


def handle_method_request(request):
    print("Direct method received - ", request.name)

    if request.name == "relay_on":
        relay.on()
    elif request.name == "relay_off":
        relay.off()

    method_response = MethodResponse.create_from_method_request(request, 200)
    device_client.send_method_response(method_response)

def read_sensor():
    soil_moisture = adc.read(0)
    print("Soil moisture:", soil_moisture)

    message = Message(json.dumps({'soil_moisture': soil_moisture}))
    device_client.send_message(message)

def run():
    initialise((
    'HostName=ECM3440JetskiHub.azure-devices.net;'
    'DeviceId=soil-moisture-sensor;'
    'SharedAccessKey=ijkvLn9ZOI7/aw3IyoBnQdxOD7LM5MCC9/vtgmMDF5s='))
    connect()
    device_client.on_method_request_received = handle_method_request

    while True:
        read_sensor()
        time.sleep(10)
        
if __name__ == "__main__":
    run()
