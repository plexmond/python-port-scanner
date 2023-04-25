from flask import Flask, request, render_template
import socket

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        hostname = request.form['hostname']
        start_port = int(request.form['startport'])
        end_port = int(request.form['endport'])

        open_ports = scan_ports(hostname, start_port, end_port)

        return render_template('result.html', 
                               hostname=hostname,
                               start_port=start_port,
                               end_port=end_port,
                               total_ports=end_port - start_port + 1,
                               open_ports=open_ports)

    return render_template('index.html')

def scan_ports(hostname, start_port, end_port):
    open_ports = []
    for port in range(start_port, end_port+1):
        address = (hostname, port)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)
        result = s.connect_ex(address)
        if result == 0:
            open_ports.append(port)
        s.close()
    return open_ports

if __name__ == '__main__':
    app.run(debug=True)
