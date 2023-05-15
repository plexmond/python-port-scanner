from flask import Flask, request, render_template
import time
import datetime
from port_scanner import *
from mail import send_mail
from config import Config

# timestamp
def timestamp_to_str(timestamp):
    return datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')


app = Flask(__name__)

# main route
@app.route('/', methods=['GET', 'POST'])
def index():
    start_port = 0
    end_port = 0
    open_ports = []

    if request.method == 'POST':
        hostname = request.form['hostname']
        scan_option = request.form['option']
        concurrent = int(request.form['concurrent'])
        timeout = float(request.form['timeout'])

        if scan_option == 'custom':
            start_port = int(request.form['startport'])
            end_port = int(request.form['endport'])
        elif scan_option == 'single':
            start_port = int(request.form['startport'])
            end_port = start_port

        ports_to_scan = get_ports_to_scan(scan_option, start_port, end_port)

        start_time = time.time()
        open_ports = scan_ports(hostname, ports_to_scan, concurrent, timeout)
        end_time = time.time()

        scan_duration = end_time - start_time

        headers = None
        if request.form.get('headers'):
            headers = get_http_headers(hostname)

        port_services = get_common_port_services(open_ports) if start_port == 0 and end_port == 0 else {}
        for port in open_ports:
            service = get_service_from_csv(port)
            port_services[port] = service

        # email template
        content = render_template('email_content.html',
                                  hostname=hostname,
                                  start_port=start_port,
                                  end_port=end_port,
                                  total_ports=len(ports_to_scan),
                                  open_ports=open_ports,
                                  port_services=port_services,
                                  headers=headers,
                                  start_time=start_time,
                                  end_time=end_time,
                                  scan_duration=scan_duration,
                                  timestamp_to_str=timestamp_to_str)

        # mail info
        email = request.form.get('email')
        if email:
            subject = f'Port scan results for {hostname}'
            send_mail(email, subject, content)

        # result template
        return render_template('result.html',
                               hostname=hostname,
                               start_port=start_port,
                               end_port=end_port,
                               total_ports=len(ports_to_scan),
                               open_ports=open_ports,
                               port_services=port_services,
                               headers=headers,
                               start_time=start_time,
                               end_time=end_time,
                               scan_duration=scan_duration,
                               timestamp_to_str=timestamp_to_str)

    return render_template('index.html')


# mail results route
@app.route('/resend_results', methods=['POST'])
def resend_results():
    hostname = request.form['hostname']
    start_port = int(request.form['startport'])
    end_port = int(request.form['endport'])
    total_ports = int(request.form['total_ports'])
    open_ports = request.form['open_ports'].split(',')
    port_services = request.form['port_services']
    headers = {}  
    if request.form.get('headers'):
        headers = request.form['headers']
    start_time = float(request.form['start_time'])
    end_time = float(request.form['end_time'])
    scan_duration = float(request.form['scan_duration'])

    # email template
    content = render_template('email_content.html', 
                              hostname=hostname,
                              start_port=start_port,
                              end_port=end_port,
                              total_ports=total_ports,
                              open_ports=open_ports,
                              port_services=port_services,
                              headers=headers,
                              start_time=start_time,
                              end_time=end_time,
                              scan_duration=scan_duration,
                              timestamp_to_str=timestamp_to_str)

    # mail info
    email = request.form['email']
    if email:
        subject = f'Port scan results for {hostname}'
        send_mail(email, subject, content)

    # return original values
    return render_template('result.html', 
                           hostname=hostname,
                           start_port=start_port,
                           end_port=end_port,
                           total_ports=total_ports,
                           open_ports=open_ports,
                           port_services=port_services,
                           headers=headers,
                           start_time=start_time,
                           end_time=end_time,
                           scan_duration=scan_duration,
                           timestamp_to_str=timestamp_to_str)


# debug mode,  running the website in test mode
if __name__ == '__main__':
    app.run(debug=True)