import json
import time
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware

from classes import Message, Packet

app = FastAPI()

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



def Insert_in_list(packet: Packet):
    with open("json/packets.json", "r") as file:
        packet_list = json.load(file)

    new_packet = packet.type, packet.message.id
    packet_list.append(new_packet)

    with open("json/packets.json", "w") as f:
        json.dump(packet_list, f)


@app.get("/", response_class=HTMLResponse)
async def root():
    return


@app.post("/post")
async def recieve(messages: Message):
    for message in messages:
        if (type(message[1]) is list):
            for packet in message[1]:
                print("\n\n\nInserted Packet to:", "./json/packets.json")
                print("\nType:", packet.type)
                print("ID: ", packet.message.id)

                Insert_in_list(packet)

        elif (type(message[1] is float)):
            print("Time added:",
                  time.strftime('%Y-%m-%d %H:%M:%S',
                                time.localtime(time.time())
                                ))

    print("\n")
    return messages
