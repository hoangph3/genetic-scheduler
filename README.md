# Generating Schedule based on Genetic Algorithm

## Deploy services

1. Run compose:
```sh
docker-compose up -d --build
```

## Use

1. Generating schedules:

```sh
curl -X POST http://localhost:8080/schedule/generate -H 'Content-Type: application/json' -d @data.json
```

2. View schedules:
```
[GET] http://localhost:8080/schedule/view
```