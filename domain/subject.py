class Subject(object):
  def __init__(self, name, n_lessons, instructors):
    self.name = name
    self.n_lessons = n_lessons
    self.instructors = instructors

  def __str__(self) -> str:
    return self.name
