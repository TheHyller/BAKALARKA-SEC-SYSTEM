from gpiozero import MotionSensor
import time
import socket
import picamera
import io
import threading
import struct

# Config
SENDER_ID = "1"  # treb menit sender id vzdy
DISCOVERY_PORT = 12345
IMAGE_PORT = 12346
STATUS_PORT = 12347
BUFFER_SIZE = 4096

# Hardware
mw_sensor = MotionSensor(3)  # mw sensor  GPIO3
motion_sensor = MotionSensor(4)  # pohyb sensor  GPIO4
# mozno bude treba prepisat pi camera na //libcamera-* alebo rpicam-*// https://www.raspberrypi.com/documentation/computers/camera_software.html
# pozor zmena na 64bit asi v tom bude bordel
camera = picamera.PiCamera()

# Global state
receiver_ip = None
system_active = True

def discover_receiver():
    """hladame receiver použitim UDP broadcast"""
    global receiver_ip
    print("Hladam receiver...")
    broadcast_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    broadcast_sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    broadcast_sock.settimeout(5)
    
    try:
        broadcast_sock.sendto('DISCOVER_RECEIVER'.encode('utf-8'), ('<broadcast>', DISCOVERY_PORT))
        data, addr = broadcast_sock.recvfrom(1024)
        if data.decode('utf-8') == 'RECEIVER_HERE':
            receiver_ip = addr[0]
            print(f"Receiver najdeny na {receiver_ip}")
            return True
    except socket.timeout:
        print("receiver nenajdeny")
        return False
    finally:
        broadcast_sock.close()

def send_image(image_data):
    """obrazok data cez TCP"""
    if not receiver_ip:
        return False
    ## strasny bordel sam neviem ako som to ani sprejazdnil :D
    try:
        # Create TCP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((receiver_ip, IMAGE_PORT))
        
        # Send header: size (4 bytes) + sender ID (1 byte)
        size = len(image_data)
        header = struct.pack('!I', size) + SENDER_ID.encode('utf-8')
        sock.sendall(header)
        
        # Send image data
        total_sent = 0
        while total_sent < size:
            chunk = image_data[total_sent:total_sent + BUFFER_SIZE]
            if not chunk:
                break
            sent = sock.send(chunk)
            if sent == 0:
                raise RuntimeError("Spojenie prerušené")
            total_sent += sent
            
        print(f"obrazok velkosť: {total_sent}/{size} bytes")
        return True
        
    except Exception as e:
        print(f"Obrázok nebol poslaný: {e}")
        return False
    finally:
        sock.close()

def send_status():
    """updatujeme status cez UDP"""
    if not receiver_ip:
        return
        
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        message = f"{SENDER_ID}:{'1' if motion_sensor.motion_detected else '0'}"
        sock.sendto(message.encode('utf-8'), (receiver_ip, STATUS_PORT))
    except Exception as e:
        print(f"CHyba pri poslaní statusu: {e}")
    finally:
        sock.close()

def control_listener():
    """ON OFF control commands počuvač"""
    global system_active
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('', STATUS_PORT))
    print("Pocuvanie control commandov zapnute")
    
    while True:
        try:
            data, addr = sock.recvfrom(1024)
            message = data.decode('utf-8')
            if message.startswith("SYSTEM:"):
                cmd = message.split(":", 1)[1].strip().upper()
                if cmd == "ON":
                    system_active = True
                    print("System AKTIVOVANÝ")
                elif cmd == "OFF":
                    system_active = False
                    print("System DEAKTIVOVANÝ")
        except Exception as e:
            print(f"Control lis error: {e}")

def main():
    # Start control listener thread
    threading.Thread(target=control_listener, daemon=True).start()
    
    while True:
        # Ensure we have a receiver
        if not receiver_ip:
            if not discover_receiver():
                time.sleep(5)
                continue
        
        # Send status update
        send_status()
        
        # Check for motion
        if motion_sensor.motion_detected:
            print("Motion detected!")
            if system_active:
                # Capture and send image
                stream = io.BytesIO()
                camera.capture(stream, format='jpeg')
                image_data = stream.getvalue()
                if not send_image(image_data):
                    receiver_ip = None  # Force rediscovery if send fails
            else:
                print("System je vypnuty, nezachytavame fotky")
        
        time.sleep(0.5)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\nUkončenie programu")
    finally:
        camera.close()