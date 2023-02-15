# Generating Schedule based on Genetic Algorithm

## Deploy services

1. Run compose:
```sh
docker-compose up -d
```

2. Access the UI:
* [mongo express](http://localhost:8081) (you can view or edit the schedule database here)

## Use

1. Generating schedules

```sh
curl -X POST http://localhost:8080/schedule/generate -H 'Content-Type: application/json' -d '{}'
```

2. View schedules
```
[GET] http://localhost:8080/schedule/view
```