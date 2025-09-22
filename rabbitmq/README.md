# RabbitMQ - example

This is a simple project demonstrating how to use `RabbitMQ` with `Python` for message-based communication. It uses `Docker Compose` to run a `RabbitMQ server` and includes 2 Python scripts:
- `send.py` – a producer that sends a message to the queue.
- `receive.py` – a consumer that receives and prints messages from the queue.

## Project structure

```text
rabbitmq/
│
├── docker-compose.yml
├── send.py         # Producer
├── receive.py      # Consumer
└── requirements.txt
```

## RUN

1. Start `RabbitMQ` with `Docker Compose`

From the project directory:

```bash
# Start a RabbitMQ container in the background
docker-compose up -d
```

2. Access the `RabbitMQ Management UI` (monitore queues, messages, and connections)

Open your browser and go to: http://localhost:15672

- Username: `guest`
- Password: `guest`

3. Install Python dependencies

In the project folder run:

```bash
pip install -r requirements.txt
```

This installs the pika library for working with RabbitMQ in Python.

4. Run the `Consumer` (`Receiver`)

In Terminal `1`, run:

```bash
python receive.py
```

This script waits for messages in the `hello` queue.

5. Run the `Producer` (`Sender`)

In Terminal `2`, run:
```bash
python send.py
```

This script sends a message to the `hello queue`.

6. Check the Output

The `consumer` terminal print:

```text
 [x] Received: Hello from Producer!
 ```
 
To see the message flow:
- Run `send.py` without starting the `consumer`.
- In this case, the `message` will remain in the queue (`hello`) and will be visible in the `UI` with the status `Ready`.
- Open the `RabbitMQ UI` (tab `Queues and Streams`). In the `Queues > hello` tab (http://localhost:15672/#/queues), you will see:
  - `Ready` – the number of messages waiting to be consumed
  - `Unacked` – the number of messages delivered but not yet acknowledged
  - `Total` – the total number of messages currently in the queue
