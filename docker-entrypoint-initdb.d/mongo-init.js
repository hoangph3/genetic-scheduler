db = db.getSiblingDB('schedule');

db.createCollection('classroom');

db.classroom.insertMany([
   {
        "name": "6A",
        "subject": [
            {"name": "Toan", "instructor": "To01", "n_lessons": 4},
            {"name": "Ly", "instructor": "Ly01", "n_lessons": 3},
            {"name": "Hoa", "instructor": "Ho01", "n_lessons": 3},
            {"name": "Van", "instructor": "Va01", "n_lessons": 4},
            {"name": "Anh", "instructor": "An01", "n_lessons": 2},
            {"name": "Sinh", "instructor": "Si01", "n_lessons": 2},
            {"name": "Su", "instructor": "Su01", "n_lessons": 1},
            {"name": "Dia", "instructor": "Di01", "n_lessons": 1},
            {"name": "GDCD", "instructor": "GD01", "n_lessons": 1},
            {"name": "Tin", "instructor": "Ti01", "n_lessons": 2},
            {"name": "CN", "instructor": "To01", "n_lessons": 1},
            {"name": "The", "instructor": "Th01", "n_lessons": 2}
        ],
        "main_instructor": "To01"
    },
    {
        "name": "6B",
        "subject": [
            {"name": "Toan", "instructor": "To01", "n_lessons": 4},
            {"name": "Ly", "instructor": "Ly01", "n_lessons": 3},
            {"name": "Hoa", "instructor": "Ho01", "n_lessons": 3},
            {"name": "Van", "instructor": "Va01", "n_lessons": 4},
            {"name": "Anh", "instructor": "An01", "n_lessons": 2},
            {"name": "Sinh", "instructor": "Si01", "n_lessons": 2},
            {"name": "Su", "instructor": "Su01", "n_lessons": 1},
            {"name": "Dia", "instructor": "Di01", "n_lessons": 1},
            {"name": "GDCD", "instructor": "GD01", "n_lessons": 1},
            {"name": "Tin", "instructor": "Ti01", "n_lessons": 2},
            {"name": "CN", "instructor": "To01", "n_lessons": 1},
            {"name": "The", "instructor": "Th01", "n_lessons": 2}
        ],
        "main_instructor": "Ly01"
    },
    {
        "name": "6C",
        "subject": [
            {"name": "Toan", "instructor": "To01", "n_lessons": 4},
            {"name": "Ly", "instructor": "Ly01", "n_lessons": 3},
            {"name": "Hoa", "instructor": "Ho01", "n_lessons": 3},
            {"name": "Van", "instructor": "Va01", "n_lessons": 4},
            {"name": "Anh", "instructor": "An01", "n_lessons": 2},
            {"name": "Sinh", "instructor": "Si01", "n_lessons": 2},
            {"name": "Su", "instructor": "Su01", "n_lessons": 1},
            {"name": "Dia", "instructor": "Di01", "n_lessons": 1},
            {"name": "GDCD", "instructor": "GD01", "n_lessons": 1},
            {"name": "Tin", "instructor": "Ti01", "n_lessons": 2},
            {"name": "CN", "instructor": "To01", "n_lessons": 1},
            {"name": "The", "instructor": "Th01", "n_lessons": 2}
        ],
        "main_instructor": "Ho01"
    }
]);