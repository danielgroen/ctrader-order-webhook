import logging
from flask import Flask, jsonify
from ctrader_open_api import Client, Protobuf, TcpProtocol, EndPoints
from ctrader_open_api.messages.OpenApiCommonMessages_pb2 import *
from ctrader_open_api.messages.OpenApiMessages_pb2 import *
from ctrader_open_api.messages.OpenApiModelMessages_pb2 import *
from twisted.internet import reactor
import threading
import os
from dotenv import load_dotenv

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

# Flask app setup
app = Flask(__name__)

# Twisted client setup
host = EndPoints.PROTOBUF_DEMO_HOST # EndPoints.PROTOBUF_LIVE_HOST
client = Client(host, EndPoints.PROTOBUF_PORT, TcpProtocol)

# Order parameters (these can also come from request arguments)
account_id = os.getenv("ACCOUNT_ID")
symbol_id = 1          # Replace with your symbolId
order_type = ProtoOAOrderType.MARKET
trade_side = ProtoOATradeSide.BUY
volume = 100000

# Flag to check if client is running
client_running = False

def onError(failure):
    logger.error(f"Error: {failure}")

def onAuthSuccess(response):
    logger.info("Authentication Successful!")
    logger.info(response)
    create_order()

def create_order():
    logger.info("Inside create_order()")
    order_request = ProtoOANewOrderReq()
    order_request.ctidTraderAccountId = account_id
    order_request.symbolId = symbol_id
    order_request.orderType = order_type
    order_request.tradeSide = trade_side
    order_request.volume = volume

    logger.info(f"Order Request: {order_request}")

    deferred = client.send(order_request)
    deferred.addCallbacks(onOrderSuccess, onError)

def onOrderSuccess(response):
    logger.info("Order placed successfully!")
    logger.info(response)

def connected(client):
    logger.info("Connected to cTrader API.")
    auth_request = ProtoOAApplicationAuthReq()
    auth_request.clientId = client_id
    auth_request.clientSecret = client_secret
    deferred = client.send(auth_request)
    deferred.addCallbacks(onAuthSuccess, onError)

def disconnected(client, reason):
    logger.info(f"Disconnected: {reason}")

def onMessageReceived(client, message):
    logger.info(f"Message received: {Protobuf.extract(message)}")

# Set Twisted client callbacks
client.setConnectedCallback(connected)
client.setDisconnectedCallback(disconnected)
client.setMessageReceivedCallback(onMessageReceived)

@app.route("/webhook", methods=["GET"])
def webhook():
    global client_running
    
    logger.info("Webhook received")
    if not client_running:
        logger.info("Starting the client service...")
        client_running = True
        threading.Thread(target=client.startService).start()
    else:
        logger.info("Client is already running.")
    if client_running:
        create_order()
    
    return jsonify({"message": "Order creation initiated."}), 200

# Start Flask app
if __name__ == "__main__":
    # Start Flask in a separate thread
    flask_thread = threading.Thread(target=lambda: app.run(host="0.0.0.0", port=5000))
    flask_thread.start()

    # Start Twisted reactor in the main thread
    logger.info("Starting Twisted reactor")
    reactor.run(installSignalHandlers=0)
