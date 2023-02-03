from domain import Classroom, Subject, Instructor, MeetingTime


class Data(object):
  def __init__(self):
    self.meeting_times = []
    self.instructors = []
    self.subjects = []
    self.classrooms = []
    self.initialize()

  def initialize(self):
    # env
    N_LESSON_EACH_DAY = 5
    DAYS_OF_WEEK = [2,3,4,5,6,7]

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
      Instructor(name="T02", classroom="6C"),
      Instructor(name="T03"),
      Instructor(name="T04"),
      Instructor(name="T05"),
      Instructor(name="T06", classroom="7A"),
      Instructor(name="T07", classroom="7B"),
      Instructor(name="T08", classroom="7C"),
      Instructor(name="T09"),
      Instructor(name="T10"),
      Instructor(name="T11"),
      Instructor(name="T12", classroom="8A"),
      Instructor(name="T13", classroom="8B"),
      Instructor(name="T14", classroom="8C"),
      Instructor(name="T15"),
      Instructor(name="T16"),
      Instructor(name="T17"),
    ]

    # create subjects
    self.subjects = [
      Subject(name="Toan", n_lessons=4, instructors=[self.instructors[0], self.instructors[2]]),
      Subject(name="Ly", n_lessons=3, instructors=[self.instructors[1], self.instructors[3]]),
      Subject(name="Hoa", n_lessons=3, instructors=[self.instructors[4], self.instructors[6]]),
      Subject(name="Van", n_lessons=4, instructors=[self.instructors[5], self.instructors[7]]),
      Subject(name="Anh", n_lessons=2, instructors=[self.instructors[8], self.instructors[10]]),
      Subject(name="Sinh", n_lessons=2, instructors=[self.instructors[9], self.instructors[11]]),
      Subject(name="Su", n_lessons=1, instructors=[self.instructors[12]]),
      Subject(name="Dia", n_lessons=1, instructors=[self.instructors[13]]),
      Subject(name="GDCD", n_lessons=1, instructors=[self.instructors[14]]),
      Subject(name="Tin", n_lessons=2, instructors=[self.instructors[0], self.instructors[15]]),
      Subject(name="CN", n_lessons=1, instructors=[self.instructors[2], self.instructors[16]]),
      Subject(name="The", n_lessons=2, instructors=[self.instructors[14], self.instructors[17]]),
    ]

    # create classrooms
    self.classrooms = [
      Classroom(name="6A", subjects=self.subjects),
      # Classroom(name="6B", subjects=self.subjects),
      # Classroom(name="6C", subjects=self.subjects),
      # Classroom(name="7A", subjects=self.subjects),
      # Classroom(name="7B", subjects=self.subjects),
      # Classroom(name="7C", subjects=self.subjects),
      # Classroom(name="8A", subjects=self.subjects),
      # Classroom(name="8B", subjects=self.subjects),
      # Classroom(name="8C", subjects=self.subjects),
    ]

  def get_meeting_times(self):
    return self.meeting_times

  def get_instructors(self):
    return self.instructors

  def get_subjects(self):
    return self.subjects

  def get_classrooms(self):
    return self.classrooms
