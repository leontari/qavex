<<<<<<< HEAD
<<<<<<< HEAD
worker-service (optional)

objective:
  - heavy tasks:
    - backend tests
    - reports
    - periodic calculations
  
interface:
  - triggered by a queue (RabbitMQ/Kafka/Redis Streams) or
  - CRONJob in k8s 
=======
db-service (Postgres/Timescale/ClickHouse)
=======
worker-service (optional)
>>>>>>> 9149960 (feature: project structure (#1))

objective:
  - heavy tasks:
    - backend tests
    - reports
    - periodic calculations
  
interface:
<<<<<<< HEAD
>>>>>>> 3f129e9 (feature: project structure (#1))
=======
  - triggered by a queue (RabbitMQ/Kafka/Redis Streams) or
  - CRONJob in k8s 
>>>>>>> 9149960 (feature: project structure (#1))
  
