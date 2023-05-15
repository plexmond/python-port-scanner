import socket
import csv
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

# full port scan with multithreading
def scan_ports(hostname, ports_to_scan, concurrent, timeout):
    open_ports = []

    # port scanning
    def is_port_open(port):
        address = (hostname, port)
        # socket
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout)
        result = s.connect_ex(address)
        # close socket each scan
        s.close()
        return result == 0

    # multithreading: https://docs.python.org/3/library/concurrent.futures.html , https://towardsdatascience.com/python-concurrency-concurrent-futures-15b56dc9a14d
    with ThreadPoolExecutor(max_workers=concurrent) as executor:
        futures = {executor.submit(is_port_open, port): port for port in ports_to_scan}
        for future in as_completed(futures):
            port = futures[future]
            if future.result():
                open_ports.append(port)

    return open_ports

# common ports file
def get_ports_to_scan(scan_option, start_port, end_port):
    if scan_option == 'common10':
        return [21, 22, 23, 25, 53, 80, 110, 143, 443, 3389]
    elif scan_option == 'common50':
        return [21, 22, 23, 25, 53, 80, 81, 110, 111, 119, 143, 443, 445, 465, 587, 993, 995, 1723, 3306, 3389, 5900, 8080, 10000,]
    elif scan_option == 'single':
        return [start_port]
    else:
        return list(range(start_port, end_port + 1))

# read tcp ports file
def get_service_from_csv(port):
    with open('tcp-ports.csv', mode='r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['port'] == str(port):
                return row['description']
    return "Unknown"

# service mapping
def get_common_port_services(open_ports):
    port_services = {}
    for port in open_ports:
        service = get_service_from_csv(port)
        port_services[port] = service
    return port_services

# get http header
def get_http_headers(hostname):
    try:
        response = requests.get(f"http://{hostname}")
        return response.headers
    except requests.exceptions.RequestException:
        return None