<<<<<<< feature/structure
db-service (Postgres/Timescale/ClickHouse)

objective:
  - store history, users, settings
  - in k3s - StatefulSet + PVC
  
interface:
  
=======
frontend (Vue or Svelte + lightweight-charts)

objective:
  - UI
  - charts
  - routing
  - authorisation
  - settings
  
interface:
  - interacts only with ```backend-api```
>>>>>>> main
