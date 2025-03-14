from socket import socket, SOCK_DGRAM, SOL_SOCKET, SO_REUSEADDR, SO_BROADCAST
import threading
import time

DISCOVERY_PORT = 12345  # Use the appropriate discovery port

def discovery_listener():
    """Listen for discovery broadcasts"""
    sock = socket(SOCK_DGRAM)
    sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    sock.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
    sock.bind(('', DISCOVERY_PORT))
    print(f"Discovery listener started on port {DISCOVERY_PORT}")
    
    while True:
        try:
            data, addr = sock.recvfrom(1024)
            if data.decode('utf-8') == 'DISCOVER_RECEIVER':
                print(f"Discovery request from {addr[0]}")
                sock.sendto('RECEIVER_HERE'.encode('utf-8'), addr)
        except Exception as e:
            print(f"Error in discovery listener: {e}")

def start_discovery_listener():
    listener_thread = threading.Thread(target=discovery_listener, daemon=True)
    listener_thread.start()
    print("Discovery listener thread started")

"""
import socket
import threading

DISCOVERY_PORT = 12345

def discovery_listener():
    #Listen for discovery broadcasts
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sock.bind(('', DISCOVERY_PORT))
    print(f"Discovery listener started on port {DISCOVERY_PORT}")
    
    while True:
        try:
            data, addr = sock.recvfrom(1024)
            if data.decode('utf-8') == 'DISCOVER_RECEIVER':
                print(f"Discovery request from {addr[0]}")
                sock.sendto('RECEIVER_HERE'.encode('utf-8'), addr)
        except Exception as e:
            print(f"Error in discovery listener: {e}")

def start_discovery_listener():
    threading.Thread(target=discovery_listener, daemon=True).start()
"""
