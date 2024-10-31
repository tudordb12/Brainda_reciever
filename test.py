import numpy as np
import random
import time
from paho.mqtt import client as mqtt_client
from audio_recorder import AudioToTextRecorder

# MQTT Broker configuration
broker = 'broker.emqx.io'
port = 1883
topic = "python/mqtt"
client_id = f'publish-{random.randint(0, 1000)}'
username = 'lindacov'
password = 'iamthebest'

def connect_mqtt():
    client = mqtt_client.Client(client_id)
    client.connect(broker, port)
    return client

def publish(client, msg):
    result = client.publish(topic, msg)
    status = result[0]
    if status == 0:
        print(f"Sent {msg} to topic {topic}")
    else:
        print(f"Failed to send message to topic {topic}")

def process_text(client, text):
    print("Transcribed Text:", text)
    words_array = np.array(text.split())
    print("Words Array:", words_array)

    # Publish the transcribed text to the MQTT broker
    publish(client, text)  # Send the text as a message to the MQTT server

if __name__ == '__main__':
    # Initialize the MQTT client
    mqtt_client = connect_mqtt()
    mqtt_client.loop_start()

    # Define the callback function for the transcription
    def on_transcription(text):
        process_text(mqtt_client, text)
        recorder.stop()  # Stop recording after processing a complete transcription

    # Initialize the audio recorder with the callback
    recorder = AudioToTextRecorder(language='en', on_final_transcription=on_transcription)
    recorder.start()  # Start listening and transcribing

    # Run until the recorder is stopped by the callback
    mqtt_client.loop_stop()
