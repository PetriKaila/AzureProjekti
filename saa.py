import requests, json, time

# Enter your API key here
api_key = "51c8c3fbf02769e5eb1fd567b3555e0d"

# base_url variable to store url
base_url = "http://api.openweathermap.org/data/2.5/weather?"

# Give city name
city_name = "Kalajoki"

# complete_url variable to store
# complete url address
complete_url = base_url + "appid=" + api_key + "&q=" + city_name + "&units=metric"


from azure.iot.device import IoTHubDeviceClient, Message

CONNECTION_STRING = "HostName=Projektihubi.azure-devices.net;DeviceId=raspberry-pi;SharedAccessKey=iQHZUy8uPKizBA5RyivpOSSLcBVDubHk7XtjlWQtcaE="

# Define the JSON message to send to IoT Hub.
MSG_TXT = '{{{city_name}: {current_temperature}}}'

def iothub_client_init():
    # Create an IoT Hub client
    client = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING)
    return client

def iothub_client_telemetry():

    try:
        client = iothub_client_init()
        print ( "IoT Hub device lähettää lämpötilaa tunnin välein, press Ctrl-C to exit" )
        while True:
            # get method of requests module
            # return response object
            response = requests.get(complete_url)

            # json method of response object
            # convert json format data into
            # python format data
            x = response.json()

            # Now x contains list of nested dictionaries
            # Check the value of "cod" key is equal to
            # "404", means city is found otherwise,
            # city is not found
            if x["cod"] != "404":
                y = x["main"]
                current_temperature = y["temp"]
                # print(" Lämpötila = " + str(current_temperature))
    
            # Build the message with simulated telemetry values
            msg_txt_formatted = MSG_TXT.format(city_name = city_name, current_temperature = current_temperature)
            message = Message(data=msg_txt_formatted, content_encoding = "utf-8", content_type = "application/json")
            # Send the message.
            print( "Sending temperature: {}".format(message) )
            client.send_message(message)
            print ( "Temperature successfully sent" )
            time.sleep(3600)
    
    except KeyboardInterrupt:
        print ( "IoTHubClient sample stopped" )
if __name__ == '__main__':
        
    print ( "IoT Hub - Kalajoen lämpötila" )
    print ( "Press Ctrl-C to exit" )
    iothub_client_telemetry()
