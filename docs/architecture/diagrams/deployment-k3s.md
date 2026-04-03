# Deployment Diagram (k3s, ASCII)
```
                   ┌────────────────────────────┐
                   │        k3s Cluster         │
                   └────────────────────────────┘
                                 │
 ┌──────────────────────────────────────────────────────────┐
 │                       NAMESPACES                         │
 └──────────────────────────────────────────────────────────┘

 [frontend]      Deployment → Pods → Service → Ingress
 [api]           Deployment → Pods → Service
 [market-data]   Deployment → Pods
 [analytics]     Deployment → Pods
 [alerts]        Deployment → Pods
 [worker]        Deployment + CronJobs
 [db]            StatefulSet + PVC
 [redis/kafka]   StatefulSet + PVC (optional)

Ingress → API → Services → DB/Queues
```
