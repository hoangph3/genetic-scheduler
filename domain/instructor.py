class Instructor(object):
  def __init__(self, name, classroom=""):
    self.name = name
    self.classroom = classroom

  def __str__(self) -> str:
    return self.name
