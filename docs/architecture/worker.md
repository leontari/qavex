worker-service (optional)

objective:
  - heavy tasks:
    - backend tests
    - reports
    - periodic calculations
  
interface:
  - triggered by a queue (RabbitMQ/Kafka/Redis Streams) or
  - CRONJob in k8s 
