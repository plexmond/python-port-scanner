from flask import Flask, request, render_template
import socket

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        hostname = request.form['hostname']
        start_port = int(request.form['startport'])
        end_port = int(request.form['endport'])
        scan_option = request.form['option']

        if scan_option == 'custom':
            open_ports = scan_ports(hostname, start_port, end_port)
        elif scan_option == 'common10':
            start_port = 1
            end_port = 1024
            open_ports = scan_common_ports(hostname, [21, 22, 23, 25, 53, 80, 110, 143, 443, 3389])
        elif scan_option == 'common50':
            start_port = 1
            end_port = 65535
            open_ports = scan_common_ports(hostname, [21, 22, 23, 25, 53, 80, 110, 143, 443, 3389, 1723, 3306, 5900, 8080, 8443, 8888, 9999, 10000, 32768, 49152, 49153, 49154, 49155, 49156, 49157, 49158, 49159, 49160, 49161, 49162, 49163, 49164, 49165, 49166, 49167, 49168, 49169, 49170, 49171, 49172, 49173, 49174, 49175, 49176, 49177, 49178, 49179, 49180])

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
            service = get_service_name(port)
            open_ports.append((port, service))
        s.close()
    return open_ports

def scan_common_ports(hostname, port_list):
    open_ports = []
    for port in port_list:
        address = (hostname, port)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)
        result = s.connect_ex(address)
        if result == 0:
            service = get_service_name(port)
            open_ports.append((port, service))
        s.close()
    return open_ports

def get_service_name(port):
    try:
        return socket.getservbyport(port)
    except OSError:
        return "Unknown"

if __name__ == '__main__':
    app.run(debug=True)
