from flask import Flask, request, jsonify, render_template
from src.predict import predict_one

app=Flask(__name__)

@app.get("/")
def home():
    return render_template("index.html")

@app.route('/predict',methods=['POST'])
def predict():
    payload=request.get_json()
    if not payload:
        return jsonify({'error':'Missing/invalid JSON'}),400
    try:
        return jsonify(predict_one(payload))
    except Exception as e:
        return jsonify({'error':str(e)}),400
    

@app.get("/health")
def health():
    return {"status": "ok"}

    
if __name__ == "__main__":
    app.run(debug=True) 

