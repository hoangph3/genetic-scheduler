import pymongo
from domain import Classroom, Subject, Instructor, MeetingTime
from utils.database import get_mongo_uri


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
    myclient = pymongo.MongoClient(get_mongo_uri())
    mydb = myclient["schedule"]
    mycol = mydb["classroom"]

    instructors = {}
    classes = list(mycol.find({}))
    for classroom in classes:
      for subject in classroom["subject"]:
        if subject['instructor'] not in instructors:
          instructors[subject['instructor']] = len(instructors)
          self.instructors.append(Instructor(name=subject['instructor'], classroom=''))

    for instructor in self.instructors:
      for classroom in classes:
        if instructor.name == classroom['main_instructor']:
          instructor.classroom = classroom['name']
          break

    instructors = {}
    for instructor in self.instructors:
      instructors[instructor.name] = instructor

    for classroom in classes:
      subjects = []
      for subject in classroom['subject']:
        subjects.append(Subject(name=subject['name'], n_lessons=subject['n_lessons'], instructor=instructors[subject['instructor']]))
      self.classrooms.append(Classroom(name=classroom['name'], subjects=subjects))

    # for instructor in self.instructors:
    #   print(instructor.name, instructor.classroom)
    # for classroom in self.classrooms:
    #   print(classroom.name)
    #   for subject in classroom.subjects:
    #     print(subject.name, subject.n_lessons, subject.instructor.name, subject.instructor.classroom)


  def get_meeting_times(self):
    return self.meeting_times


  def get_instructors(self):
    return self.instructors


  def get_classrooms(self):
    return self.classrooms


if __name__ == "__main__":
  data = Data()
