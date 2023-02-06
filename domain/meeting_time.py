class MeetingTime(object):
  def __init__(self, day, lesson):
    self.day = day
    self.lesson = lesson

  def __str__(self) -> str:
    return f"D{self.day}_L{self.lesson}"
