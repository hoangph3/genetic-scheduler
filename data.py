from domain import Classroom, Subject, Instructor, MeetingTime


class Data(object):
  def __init__(self):
    self.meeting_times = []
    self.instructors = []
    self.subjects = []
    self.classrooms = []
    self.initialize()

  def initialize(self):
    # number of lessons in a week
    N_LESSON_EACH_DAY = 5
    DAYS_OF_WEEK = [2, 3, 4, 5, 6, 7]

    # create meeting times
    lessons = [_ for _ in range(1, N_LESSON_EACH_DAY + 1)]
    for day in DAYS_OF_WEEK:
      for lesson in lessons:
        if (day == 2 and lesson == 1) or (day == 7 and lesson == 5):
          continue
        self.meeting_times.append(MeetingTime(day=day, lesson=lesson))

    # creating instructors
    self.instructors = [
      Instructor(name="T00", classroom="6A"),
      Instructor(name="T01", classroom="6B"),
      Instructor(name="T02"),
      Instructor(name="T03"),
      Instructor(name="T04"),
      Instructor(name="T05"),
      Instructor(name="T06"),
      Instructor(name="T07"),
      Instructor(name="T08"),
      Instructor(name="T09"),
      Instructor(name="T10"),
      Instructor(name="T11"),
      Instructor(name="T12")
    ]

    # create classrooms with subjects
    self.classrooms = [
      Classroom(name="6A", subjects=[
        Subject(name="Toan", n_lessons=4, instructor=self.instructors[0]),
        Subject(name="Ly", n_lessons=3, instructor=self.instructors[1]),
        Subject(name="Hoa", n_lessons=3, instructor=self.instructors[2]),
        Subject(name="Van", n_lessons=4, instructor=self.instructors[3]),
        Subject(name="Anh", n_lessons=2, instructor=self.instructors[4]),
        Subject(name="Sinh", n_lessons=2, instructor=self.instructors[5]),
        Subject(name="Su", n_lessons=1, instructor=self.instructors[6]),
        Subject(name="Dia", n_lessons=1, instructor=self.instructors[7]),
        Subject(name="GDCD", n_lessons=1, instructor=self.instructors[8]),
        Subject(name="Tin", n_lessons=2, instructor=self.instructors[0]),
        Subject(name="CN", n_lessons=1, instructor=self.instructors[10]),
        Subject(name="The", n_lessons=2, instructor=self.instructors[11]),
      ]),
      Classroom(name="6B", subjects=[
        Subject(name="Toan", n_lessons=4, instructor=self.instructors[12]),
        Subject(name="Ly", n_lessons=3, instructor=self.instructors[1]),
        Subject(name="Hoa", n_lessons=3, instructor=self.instructors[2]),
        Subject(name="Van", n_lessons=4, instructor=self.instructors[3]),
        Subject(name="Anh", n_lessons=2, instructor=self.instructors[4]),
        Subject(name="Sinh", n_lessons=2, instructor=self.instructors[5]),
        Subject(name="Su", n_lessons=1, instructor=self.instructors[6]),
        Subject(name="Dia", n_lessons=1, instructor=self.instructors[7]),
        Subject(name="GDCD", n_lessons=1, instructor=self.instructors[8]),
        Subject(name="Tin", n_lessons=2, instructor=self.instructors[9]),
        Subject(name="CN", n_lessons=1, instructor=self.instructors[12]),
        Subject(name="The", n_lessons=2, instructor=self.instructors[11]),
      ]),
    ]

  def get_meeting_times(self):
    return self.meeting_times

  def get_instructors(self):
    return self.instructors

  def get_classrooms(self):
    return self.classrooms
