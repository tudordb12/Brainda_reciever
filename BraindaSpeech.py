import asyncio
import edge_tts
import os
import playsound
import openai
import random
from paho.mqtt import client as mqtt_client

# Set your OpenAI API key
openai.api_key = ""

# MQTT Broker configuration
broker = 'broker.emqx.io'
port = 1883
topic = "python/mqtt"
client_id = f'subscribe-{random.randint(0, 100)}'

# Variable to hold the latest message and a flag to check for new messages
latest_message = ""
new_message_received = False


# MQTT connection and subscription
def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(mqtt_client.CallbackAPIVersion.VERSION1, client_id)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        global latest_message, new_message_received
        latest_message = msg.payload.decode()
        new_message_received = True  # Set flag to indicate a new message
        print(f"Received {latest_message} from {msg.topic} topic")

    client.subscribe(topic)
    client.on_message = on_message


def run_mqtt():
    client = connect_mqtt()
    subscribe(client)
    client.loop_start()  # Start the loop in a separate thread




async def get_openai_response(question):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {'role':'system', 'content':'you are a personal assistant named Brainda. Give short and straight to the point responses to all prompts given.'},
            {"role": "user", "content": question}
        ]

    )
    return response.choices[0].message['content']


async def speak(text, voice="en-US-AvaMultilingualNeural"):
    output_file = "temp_audio.mp3"
    tts = edge_tts.Communicate(text, voice)

    # Save the audio file
    await tts.save(output_file)

    # Play the saved audio
    playsound.playsound(output_file)

    # Clean up the temporary file
    os.remove(output_file)


# Main function
async def main():
    global new_message_received  # Declare it as global to access and modify
    global latest_message  # Declare it as global to access

    # Introduce the bot
    introduction = "Hey there, I'm Brainda! What would you like to learn today?"
    await speak(introduction)

    while True:
        await asyncio.sleep(1)  # Prevent busy waiting
        if new_message_received:  # Check if there is a new message
            new_message_received = False  # Reset flag
            print(f"Using the latest message as a question: {latest_message}")
            answer = await get_openai_response(latest_message)
            await speak(answer)


# Execute the main coroutine
if __name__ == '__main__':
    run_mqtt()  # Start MQTT subscription in the background
    asyncio.run(main())