import pika

def publish_message(message, rabbitmq_host = 'localhost', queue_name = 'queue'):

    # Step 1: Establish a connection to RabbitMQ server
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitmq_host))
    channel = connection.channel()

    # Step 2: Declare a queue (ensure it exists before publishing)
    channel.queue_declare(queue=queue_name, durable=True)

    # Step 3: Publish a message to the queue
    channel.basic_publish(
        exchange='',  # Default exchange
        routing_key=queue_name,  # Queue name as the routing key
        body=message,  # Message body
        properties=pika.BasicProperties(
            delivery_mode=2,  # Make message persistent
        ),
    )

    # Step 4: Close the connection
    connection.close()

if __name__ == "__main__":
    publish_message("Hello")
