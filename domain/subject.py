class Subject(object):
  def __init__(self, name, n_lessons, instructor):
    self.name = name
    self.n_lessons = n_lessons
    self.instructor = instructor

  def __str__(self) -> str:
    return self.name
