import socket
import struct
import threading
from io import BytesIO

BUFFER_SIZE = 4096
IMAGE_PORT = 12345  # Replace with the actual port number
latest_images = {}
last_images = []

def receive_exact(sock, n):
    data = bytearray()
    while len(data) < n:
        packet = sock.recv(min(n - len(data), BUFFER_SIZE))
        if not packet:
            return None
        data.extend(packet)
    return data

def handle_tcp_client(conn, addr):
    try:
        header = receive_exact(conn, 5)
        if not header:
            return
            
        image_size = struct.unpack('!I', header[:4])[0]
        sender_id = header[4:].decode('utf-8')
        print(f"Receiving {image_size} bytes from sender {sender_id}")
        
        image_data = receive_exact(conn, image_size)
        if not image_data or len(image_data) != image_size:
            print(f"Incomplete image received from {sender_id}")
            return
            
        stream = BytesIO(image_data)
        latest_images[sender_id] = stream
        last_images.append((sender_id, stream))
        print(f"Successfully received image from {sender_id}")
        
    except Exception as e:
        print(f"Error in TCP handler: {e}")
    finally:
        conn.close()

def tcp_listener():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('0.0.0.0', IMAGE_PORT))
    sock.listen(5)
    print(f"Image receiver started on port {IMAGE_PORT}")
    
    while True:
        try:
            conn, addr = sock.accept()
            threading.Thread(target=handle_tcp_client, 
                           args=(conn, addr), 
                           daemon=True).start()
        except Exception as e:
            print(f"Error accepting TCP connection: {e}")

def start_tcp_listener():
    listener_thread = threading.Thread(target=tcp_listener, daemon=True)
    listener_thread.start()
    print("TCP listener thread started")