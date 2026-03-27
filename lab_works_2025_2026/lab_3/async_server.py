import asyncio
import random


async def run_ml_model(data: str) -> str:
    """Simulates a model processing data."""
    await asyncio.sleep(10)  # Simulate processing time

    # In a real scenario, you'd parse 'data' and pass it to your model.predict()
    return f"Model output for [{data}]: {random.random():.4f}"


async def worker(queue: asyncio.Queue):
    """Pulls tasks from the queue and processes them."""

    print("ML Worker started, waiting for tasks...")
    while True:
        # Get the network connection streams and the data from the queue
        reader, writer, data = await queue.get()
        try:
            print(f"Worker processing: {data}")

            # Run the model
            result = await run_ml_model(data)

            # Send the result back to the client
            writer.write(f"RESULT: {result}\n".encode())
            await writer.drain()

        finally:
            # Always close the connection when done
            writer.close()
            await writer.wait_closed()
            queue.task_done()


# 3. The Connection Handler
async def handle_client(reader: asyncio.StreamReader, writer: asyncio.StreamWriter, queue: asyncio.Queue):
    """Handles incoming network connections."""
    data = await reader.read(100)  # Read up to 100 bytes
    message = data.decode().strip()
    addr = writer.get_extra_info('peername')

    print(f"Received message '{message}' from {addr}")

    # Optional: Send an immediate acknowledgment
    writer.write(b"Task queued. Waiting for ML prediction...\n")
    await writer.drain()

    # Put the task in the worker's queue
    await queue.put((reader, writer, message))


# 4. Main Application Loop
async def main():
    # Create the task queue
    queue = asyncio.Queue()

    # Start the background ML worker task
    _ = asyncio.create_task(worker(queue))

    # Start the TCP server
    server = await asyncio.start_server(
        lambda r, w: handle_client(r, w, queue), '0.0.0.0', 8888)

    addr = server.sockets[0].getsockname()
    print(f'Async ML Server listening on {addr}')

    # Keep the server running forever
    async with server:
        await server.serve_forever()


if __name__ == '__main__':
    asyncio.run(main())
