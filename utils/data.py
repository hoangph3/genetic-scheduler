from domain import Classroom, Subject, Instructor, MeetingTime


class Data(object):
  def __init__(self, data):
    self.meeting_times = []
    self.instructors = []
    self.subjects = []
    self.classrooms = []
    self.data = data
    self.initialize()

  def initialize(self):
    # number of lessons in a week
    N_LESSON_EACH_DAY = 5
    DAYS_OF_WEEK = [2, 3, 4, 5, 6, 7]

    # create meeting times
    self.free_times = {}
    lessons = [_ for _ in range(1, N_LESSON_EACH_DAY + 1)]
    for day in DAYS_OF_WEEK:
      for lesson in lessons:
        if (day == 2 and lesson == 1) or (day == 7 and lesson == 5):
          continue
        meeting_time = MeetingTime(day=day, lesson=lesson)
        self.meeting_times.append(meeting_time)
        self.free_times[str(meeting_time)] = meeting_time

    instructors = {}
    for classroom in self.data:
      for subject in classroom["subjects"]:
        if subject['instructor'] not in instructors:
          instructors[subject['instructor']] = len(instructors)
          self.instructors.append(Instructor(name=subject['instructor'], classroom='', free_times=self.free_times))

    for instructor in self.instructors:
      for classroom in self.data:
        if instructor.name == classroom['main_instructor']:
          instructor.classroom = classroom['name']
          break

    instructors = {}
    for instructor in self.instructors:
      instructors[instructor.name] = instructor

    for classroom in self.data:
      subjects = []
      for subject in classroom['subjects']:
        subjects.append(Subject(name=subject['name'], n_lessons=subject['n_lessons'], instructor=instructors[subject['instructor']]))
      self.classrooms.append(Classroom(name=classroom['name'], subjects=subjects))

    # for instructor_name, instructor in instructors.items():
      # print(instructor, instructor.classroom, list(instructor.free_times.keys()))


  def get_meeting_times(self):
    return self.meeting_times


  def get_free_times(self):
    return self.free_times


  def get_instructors(self):
    return self.instructors


  def get_classrooms(self):
    return self.classrooms
