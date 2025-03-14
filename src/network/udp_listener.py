import socket
import threading
import time

BUFFER_SIZE = 4096
STATUS_PORT = 12346  # Replace with the actual port number
sender_ack = {}
motion_detected = {}

def receive_exact(sock, n):
    data = bytearray()
    while len(data) < n:
        packet = sock.recv(min(n - len(data), BUFFER_SIZE))
        if not packet:
            return None
        data.extend(packet)
    return data

def udp_listener():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('', STATUS_PORT))
    print(f"Status receiver started on port {STATUS_PORT}")
    
    while True:
        try:
            data, addr = sock.recvfrom(1024)
            message = data.decode('utf-8')
            
            if ':' in message:
                sender_id, status = message.split(':', 1)
                sender_ack[sender_id] = time.time()
                if status in ['0', '1']:
                    motion_detected[sender_id] = (status == '1')
                    print(f"Motion status from {sender_id}: {status}")
        except Exception as e:
            print(f"Error in status receiver: {e}")

def start_udp_listener():
    listener_thread = threading.Thread(target=udp_listener, daemon=True)
    listener_thread.start()
    print("UDP listener thread started")