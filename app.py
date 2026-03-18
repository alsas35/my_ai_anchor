from flask import Flask, render_template, request, jsonify
from engine import NewsAgent

app = Flask(__name__)
AGENT = NewsAgent(api_key="")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/summarize', methods=['POST'])
def summarize():
    topic = request.json.get('topic')
    if not topic:
        return jsonify({"error": "No topic provided"}), 400
    try:
        summary, sources = AGENT.generate_broadcast(topic)
        return jsonify({"summary": summary,
                        "sources": sources})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
