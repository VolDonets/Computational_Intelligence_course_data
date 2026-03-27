import socket
import time


def send_prediction_task(host: str, port: int, data_row: str):
    """
    Connects to the raw TCP server, sends a data row, and waits for the result.
    """
    # Create a TCP/IP socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        print(f"Connecting to {host}:{port}...")
        s.connect((host, port))

        # 1. Send the data (must be encoded from string to bytes)
        print(f"Sending data: [{data_row}]")
        s.sendall(data_row.encode('utf-8'))

        # 2. Receive the immediate acknowledgment from the server
        # recv(1024) reads up to 1024 bytes from the socket
        ack = s.recv(1024)
        print(f"Server Ack: {ack.decode('utf-8').strip()}")

        # 3. Wait for the background worker to finish and send the result
        # The script will block (wait) right here until the server replies
        result = s.recv(1024)
        print(f"Final Prediction: {result.decode('utf-8').strip()}")
        print("-" * 30)


if __name__ == "__main__":
    HOST = '127.0.0.1'  # Localhost
    PORT = 8888

    # Simulating data extracted from a pandas DataFrame or numpy array
    sample_dataset = [
        "5.1, 3.5, 1.4, 0.2",
        "4.9, 3.0, 1.4, 0.2",
        "1.1, 3.2, 4.7, 1.4",
        "1.2, 3.2, 4.7, 1.4",
        "1.3, 3.2, 4.7, 1.4",
        "1.4, 3.2, 4.7, 1.4",
        "1.5, 3.2, 4.7, 1.4",
    ]

    print("Starting client test...\n")

    for row in sample_dataset:
        send_prediction_task(HOST, PORT, row)
        # Adding a small delay just to make the console output readable
        time.sleep(0.5)