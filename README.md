# Generating Schedule based on Genetic Algorithm

## Install dependencies (python 3.7+)
```sh
pip3 install -r requirements.txt
```

## Deploy mongodb

1. Run db:
```sh
docker-compose up -d
```

2. Init db:
```sh
python3 utils.py
```

3. Access the UI:
* [mongo express](http://localhost:8081)
You can view or edit the schedule database here.

## Generating schedule
```
python3 scheduler.py
```
Verify the schedule with the constraints in `logs` directory.
