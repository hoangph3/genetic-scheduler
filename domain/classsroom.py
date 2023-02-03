class Classroom(object):
  def __init__(self, name, subjects):
    self.name = name
    self.subjects = subjects

  def __str__(self) -> str:
    return self.name
