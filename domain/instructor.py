class Instructor(object):
  def __init__(self, name, classroom="", free_times=[]):
    self.name = name
    self.classroom = classroom
    self.free_times = free_times

  def __str__(self) -> str:
    return self.name
