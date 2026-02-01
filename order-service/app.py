from flask import Flask, jsonify
import os
import requests

app = Flask(__name__)

CUSTOMER_SERVICE_URL = os.getenv("CUSTOMER_SERVICE_URL", "http://192.168.56.5:3001")

@app.get("/health")
def health():
    return jsonify(status="UP", service="order-service")

@app.get("/orders/<order_id>")
def get_order(order_id):
    # simple static order
    return jsonify(
        id=order_id,
        item="laptop",
        price=999,
        source_vm="order-service-vm"
    )

@app.get("/orders/<order_id>/with-customer/<customer_id>")
def order_with_customer(order_id, customer_id):
    # calls customer-service over VM network
    cust = requests.get(f"{CUSTOMER_SERVICE_URL}/customers/{customer_id}", timeout=3).json()
    return jsonify(
        order={"id": order_id, "item": "laptop", "price": 999},
        customer=cust,
        source_vm="order-service-vm",
        customer_service_url=CUSTOMER_SERVICE_URL
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3002)
