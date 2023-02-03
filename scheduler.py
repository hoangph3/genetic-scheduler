from data import Data
import random as rnd
import pandas as pd
from IPython.display import display
import numpy as np
from collections import defaultdict
import math


POPULATION_SIZE = 9
NUMB_OF_ELITE_SCHEDULES = 1
TOURNAMENT_SELECTION_SIZE = 3
MUTATION_RATE = 0.05

# rnd.seed()
data = Data()


class Schedule:
    def __init__(self):
        self._data = data
        self._classes = []
        self._numberOfConflicts = 0
        self._fitness = -1
        self._classNumb = 0
        self._isFitnessChanged = True

    def get_classes(self):
        self._isFitnessChanged = True
        return self._classes

    def get_numbOfConflicts(self): return self._numberOfConflicts

    def get_fitness(self):
        if self._isFitnessChanged:
            self._fitness = self.calculate_fitness()
            self._isFitnessChanged = False
        return self._fitness

    def initialize(self):
        for classroom in data.get_classrooms():
            for subject in classroom.subjects:
                for i in range(subject.n_lessons):
                    subject_instructions = subject.instructors
                    newClass = Class(self._classNumb, subject, subject.n_lessons, classroom)
                    self._classNumb += 1
                    newClass.set_meeting_time(data.get_meeting_times()[rnd.randrange(0, len(data.meeting_times))])
                    newClass.set_instructor(subject_instructions[rnd.randrange(0, len(subject_instructions))])
                    self._classes.append(newClass)

        return self

    def calculate_fitness(self):
        self._numberOfConflicts = 0
        classes = self.get_classes()
        for i in range(len(classes)):
            for j in range(len(classes)):
                if j > i:
                    if (classes[i].room == classes[j].room):
                        # constraint overlap meeting time
                        if (classes[i].meeting_time == classes[j].meeting_time):
                            self._numberOfConflicts += 1
                        # constraint different instructor for one subject
                        if (classes[i].subject == classes[j].subject) and (classes[i].instructor != classes[j].instructor):
                            self._numberOfConflicts += 1
                        # constraint distance between two lessons in week
                        if (classes[i].subject == classes[j].subject):
                            if math.fabs(classes[i].meeting_time.day - classes[j].meeting_time.day) == 1:
                                self._numberOfConflicts += 1
                            if classes[i].meeting_time.day == classes[j].meeting_time.day:
                                # constraint lessons on (2,4,6) or (3,5,7)
                                if classes[i].subject.n_lessons <= 6/2:
                                    self._numberOfConflicts += 1
                                else:
                                    if math.fabs(classes[i].meeting_time.lesson - classes[j].meeting_time.lesson) >= 2:
                                        self._numberOfConflicts += 1
                    else: # (classes[i].room != classes[j].room):
                        if (classes[i].meeting_time == classes[j].meeting_time) and (classes[i].instructor == classes[j].instructor):
                            self._numberOfConflicts += 1

        # constraint main instructor
        instructors_stats = defaultdict(lambda: defaultdict(list))
        for i in range(len(classes)):
            if classes[i].meeting_time.day in [2, 7]:
                instructors_stats[str(classes[i].room)][classes[i].meeting_time.day].append(str(classes[i].instructor.classroom))
        for k1, v1 in instructors_stats.items():
            for k2, v2 in v1.items():
                if k1 not in v2:
                    self._numberOfConflicts += 1

        # constraint lessons
        lessons_counter = defaultdict(lambda: defaultdict(int))
        for i in range(len(classes)):
            lessons_counter[str(classes[i].room)]['num_lessons_per_week'] += 1
        for k, v in lessons_counter.items():
            lessons_counter[k]['average_lessons_per_day'] = lessons_counter[k]['num_lessons_per_week'] // 6

        lessons_stats = defaultdict(lambda: defaultdict(list))
        for i in range(len(classes)):
            lessons_stats[str(classes[i].room)][classes[i].meeting_time.day].append(classes[i].meeting_time.lesson)

        for k1, v1 in lessons_stats.items():
            for k2 in [2, 3, 4, 5, 6, 7]: # DAYS_OF_WEEK
                v2 = lessons_stats[k1][k2]
                v2 = sorted(v2)
                lessons_stats[k1][k2] = v2
                # constraint average number of lessons
                if len(v2) < lessons_counter[k1]['average_lessons_per_day']:
                    self._numberOfConflicts += 1
                # constraint distance between two lessons in one day
                for i in range(len(v2) - 1):
                    if v2[i + 1] - v2[i] > 1:
                        self._numberOfConflicts += 1
                # constraint starting from 1st lesson
                if k2 not in [2, 7]:
                    if len(v2) == 4 and (5 in v2):
                        self._numberOfConflicts += 1
                # constraint Thursday has the least lessons
                if k2 == 5:
                    if len(v2) > lessons_counter[k1]['average_lessons_per_day']:
                        self._numberOfConflicts += 1

        return 1 / (1.0 * self._numberOfConflicts + 1)


class Population:
    def __init__(self, size):
        self._size = size
        self._data = data
        self._schedules = [Schedule().initialize() for i in range(size)]

    def get_schedules(self):
        return self._schedules


class GeneticAlgorithm:
    def evolve(self, population):
        return self._mutate_population(self._crossover_population(population))

    def _crossover_population(self, pop):
        crossover_pop = Population(0)
        for i in range(NUMB_OF_ELITE_SCHEDULES):
            crossover_pop.get_schedules().append(pop.get_schedules()[i])
        i = NUMB_OF_ELITE_SCHEDULES
        while i < POPULATION_SIZE:
            schedule1 = self._select_tournament_population(pop).get_schedules()[0]
            schedule2 = self._select_tournament_population(pop).get_schedules()[0]
            crossover_pop.get_schedules().append(self._crossover_schedule(schedule1, schedule2))
            i += 1
        return crossover_pop

    def _mutate_population(self, population):
        for i in range(NUMB_OF_ELITE_SCHEDULES, POPULATION_SIZE):
            self._mutate_schedule(population.get_schedules()[i])
        return population

    def _crossover_schedule(self, schedule1, schedule2):
        crossoverSchedule = Schedule().initialize()
        for i in range(0, len(crossoverSchedule.get_classes())):
            if rnd.random() > 0.5:
                crossoverSchedule.get_classes()[i] = schedule1.get_classes()[i]
            else:
                crossoverSchedule.get_classes()[i] = schedule2.get_classes()[i]
        return crossoverSchedule

    def _mutate_schedule(self, mutateSchedule):
        schedule = Schedule().initialize()
        for i in range(len(mutateSchedule.get_classes())):
            if MUTATION_RATE > rnd.random():
                mutateSchedule.get_classes()[i] = schedule.get_classes()[i]
        return mutateSchedule

    def _select_tournament_population(self, pop):
        tournament_pop = Population(0)
        i = 0
        while i < TOURNAMENT_SELECTION_SIZE:
            tournament_pop.get_schedules().append(pop.get_schedules()[rnd.randrange(0, POPULATION_SIZE)])
            i += 1
        tournament_pop.get_schedules().sort(key=lambda x: x.get_fitness(), reverse=True)
        return tournament_pop


class Class:
    def __init__(self, name, subject, n_lessons, room):
        self.name = name
        self.subject = subject
        self.n_lessons = n_lessons
        self.room = room
        self.instructor = None
        self.meeting_time = None

    def get_name(self):
        return self.name

    def get_subject(self):
        return self.subject

    def get_instructor(self):
        return self.instructor

    def get_meeting_time(self):
        return self.meeting_time

    def set_instructor(self, instructor):
        self.instructor = instructor

    def set_meeting_time(self, meeting_time):
        self.meeting_time = meeting_time


def timetable():
    schedule = []
    population = Population(POPULATION_SIZE)
    generation_num = 0
    population.get_schedules().sort(key=lambda x: x.get_fitness(), reverse=True)
    geneticAlgorithm = GeneticAlgorithm()
    while population.get_schedules()[0].get_fitness() != 1.0:
        generation_num += 1
        print('\n> Generation #' + str(generation_num))
        population = geneticAlgorithm.evolve(population)
        population.get_schedules().sort(key=lambda x: x.get_fitness(), reverse=True)
        schedule = population.get_schedules()[0].get_classes()
        print('\n> Number of conflicts #' + str(population.get_schedules()[0]._numberOfConflicts))
        # break

    return schedule


schedule = timetable()
result = []
for lesson in schedule:
    result.append(
        {
            "classroom": str(lesson.room),
            "subject": str(lesson.subject),
            "day": int(lesson.meeting_time.day),
            "lesson": int(lesson.meeting_time.lesson),
            "instructor": str(lesson.instructor)
        }
    )

result = pd.DataFrame(result)
# pd.set_option('mode.chained_assignment', None)
for classroom, df in result.groupby("classroom"):
    df: pd.DataFrame
    df = df.sort_values(by=["day", "lesson"], inplace=False).to_dict("records")
    new_df = pd.DataFrame(np.nan, index=[1, 2, 3, 4, 5], columns=[2, 3, 4, 5, 6, 7])  
    print('\n> Classroom #' + str(classroom))
    for d in df:
        new_df.loc[d["lesson"], d["day"]] = d["subject"] + "_" + d["instructor"]
    display(new_df)
    new_df.to_csv("timetable.csv")
