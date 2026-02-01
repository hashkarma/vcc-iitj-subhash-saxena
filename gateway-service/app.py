from flask import Flask, jsonify, Response
import os
import requests

app = Flask(__name__)

CUSTOMER_SERVICE_URL = os.getenv("CUSTOMER_SERVICE_URL", "http://192.168.56.5:3001")
ORDER_SERVICE_URL    = os.getenv("ORDER_SERVICE_URL",    "http://192.168.56.2:3002")

@app.get("/health")
def health():
    return jsonify(
        status="UP",
        service="gateway-service",
        customer_service=CUSTOMER_SERVICE_URL,
        order_service=ORDER_SERVICE_URL
    )

# --------- Proxy: Customer Service ---------
@app.get("/customers/<customer_id>")
def proxy_customer(customer_id):
    r = requests.get(f"{CUSTOMER_SERVICE_URL}/customers/{customer_id}", timeout=3)
    return Response(r.content, status=r.status_code, content_type=r.headers.get("Content-Type", "application/json"))

# --------- Proxy: Order Service ---------
@app.get("/orders/<order_id>")
def proxy_order(order_id):
    r = requests.get(f"{ORDER_SERVICE_URL}/orders/{order_id}", timeout=3)
    return Response(r.content, status=r.status_code, content_type=r.headers.get("Content-Type", "application/json"))

# --------- Aggregation Demo (calls both) ---------
@app.get("/aggregate/<order_id>/customer/<customer_id>")
def aggregate(order_id, customer_id):
    o = requests.get(f"{ORDER_SERVICE_URL}/orders/{order_id}", timeout=3).json()
    c = requests.get(f"{CUSTOMER_SERVICE_URL}/customers/{customer_id}", timeout=3).json()
    return jsonify(order=o, customer=c, source_vm="gateway-service-vm")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
