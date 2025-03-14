def receive_exact(sock, n):
    data = bytearray()
    while len(data) < n:
        packet = sock.recv(min(n - len(data), 4096))
        if not packet:
            return None
        data.extend(packet)
    return data