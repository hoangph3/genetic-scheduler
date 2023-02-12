db = db.getSiblingDB('schedule');

db.createCollection('classroom');

db.classroom.insertMany([
  {
        "name": "6A", 
        "subject": [
            {"name": "Toan", "instructor": "To6", "n_lessons": 4},
            {"name": "Ly", "instructor": "Ly6", "n_lessons": 3},
            {"name": "Hoa", "instructor": "Ho6", "n_lessons": 3},
            {"name": "Van", "instructor": "Va6", "n_lessons": 4},
            {"name": "Anh", "instructor": "An6", "n_lessons": 2},
            {"name": "Sinh", "instructor": "Si6", "n_lessons": 2},
            {"name": "Su", "instructor": "Su6", "n_lessons": 1},
            {"name": "Dia", "instructor": "Di6", "n_lessons": 1},
            {"name": "GDCD", "instructor": "GD6", "n_lessons": 1},
            {"name": "Tin", "instructor": "Ti6", "n_lessons": 2},
            {"name": "CN", "instructor": "CN6", "n_lessons": 1},
            {"name": "The", "instructor": "Th6", "n_lessons": 2}
        ],
        "main_instructor": "To6"
    },
    {
        "name": "6B", 
        "subject": [
            {"name": "Toan", "instructor": "To6", "n_lessons": 4},
            {"name": "Ly", "instructor": "Ly6", "n_lessons": 3},
            {"name": "Hoa", "instructor": "Ho6", "n_lessons": 3},
            {"name": "Van", "instructor": "Va6", "n_lessons": 4},
            {"name": "Anh", "instructor": "An6", "n_lessons": 2},
            {"name": "Sinh", "instructor": "Si6", "n_lessons": 2},
            {"name": "Su", "instructor": "Su6", "n_lessons": 1},
            {"name": "Dia", "instructor": "Di6", "n_lessons": 1},
            {"name": "GDCD", "instructor": "GD6", "n_lessons": 1},
            {"name": "Tin", "instructor": "Ti6", "n_lessons": 2},
            {"name": "CN", "instructor": "CN6", "n_lessons": 1},
            {"name": "The", "instructor": "Th6", "n_lessons": 2}
        ],
        "main_instructor": "Ly6"
    }
]);