from flask import Flask, jsonify

app = Flask(__name__)

@app.get("/health")
def health():
    return jsonify(status="UP", service="customer-service")

@app.get("/customers/<customer_id>")
def get_customer(customer_id):
    return jsonify(
        id=customer_id,
        name="Subhash Saxena",
        tier="gold",
        source_vm="customer-service-vm"
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3001)


