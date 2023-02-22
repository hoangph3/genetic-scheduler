from collections import defaultdict
from loguru import logger
import random as rnd
import pandas as pd
import signal
import json
import math
import os
import time

from utils.data import Data


POPULATION_SIZE = int(os.getenv("POPULATION_SIZE", "300"))
NUMB_OF_ELITE_SCHEDULES = int(os.getenv("NUMB_OF_ELITE_SCHEDULES", "2"))
TOURNAMENT_SELECTION_SIZE = int(os.getenv("TOURNAMENT_SELECTION_SIZE", "4"))
CROSSOVER_RATE = float(os.getenv("CROSSOVER_RATE", "0.90"))
MUTATION_RATE = float(os.getenv("MUTATION_RATE", "0.03"))
JOB_TIMEOUT = int(os.getenv("JOB_TIMEOUT", "60"))
THREAD_TIMEOUT = int(os.getenv("THREAD_TIMEOUT", "1200"))


class Schedule:
    def __init__(self, _data):
        self._data = _data
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
        classroom = self._data
        for subject in classroom.subjects:
            for i in range(subject.n_lessons):
                newClass = Class(self._classNumb, subject, subject.n_lessons, classroom)
                self._classNumb += 1
                newClass.set_instructor(subject.instructor)
                free_times = list(subject.instructor.free_times.values())
                if not len(free_times):
                    logger.info("Exceed the teaching hours of {}".format(subject.instructor))
                newClass.set_meeting_time(rnd.choice(free_times))
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
                        # constraint distance between two lessons in week
                        if (classes[i].subject == classes[j].subject):
                            if math.fabs(classes[i].meeting_time.day - classes[j].meeting_time.day) == 1:
                                self._numberOfConflicts += 1
                            if classes[i].meeting_time.day == classes[j].meeting_time.day:
                                # constraint subjects with less than 2 lessons
                                if classes[i].subject.n_lessons <= 2:
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
                lessons_dist = []
                for i in range(len(v2) - 1):
                    lessons_dist.append(v2[i+1] - v2[i])
                if len(lessons_dist):
                    if max(lessons_dist) > 1:
                        self._numberOfConflicts += 1
                # constraint starting from 1st lesson
                if k2 != 2:
                    if len(v2) == 4 and (1 not in v2):
                        self._numberOfConflicts += 1
                # constraint Thursday has the least lessons
                if k2 == 5:
                    if len(v2) > lessons_counter[k1]['average_lessons_per_day']:
                        self._numberOfConflicts += 1

        return 1 / (self._numberOfConflicts + 1)


class Population:
    def __init__(self, size, _data):
        self._size = size
        self._schedules = [Schedule(_data).initialize() for _ in range(size)]

    def get_schedules(self):
        return self._schedules


class GeneticAlgorithm:
    def __init__(self, _data):
        self._data = _data

    def evolve(self, population):
        return self._mutate_population(self._crossover_population(population))

    def _crossover_population(self, pop):
        crossover_pop = Population(0, self._data)
        for i in range(NUMB_OF_ELITE_SCHEDULES):
            crossover_pop.get_schedules().append(pop.get_schedules()[i])
        i = NUMB_OF_ELITE_SCHEDULES
        while i < POPULATION_SIZE:
            if CROSSOVER_RATE > rnd.random():
                schedule1 = self._select_tournament_population(pop).get_schedules()[0]
                schedule2 = self._select_tournament_population(pop).get_schedules()[0]
                crossover_pop.get_schedules().append(self._crossover_schedule(schedule1, schedule2))
            else:
                crossover_pop.get_schedules().append(pop.get_schedules()[i])
            i += 1
        return crossover_pop

    def _mutate_population(self, population):
        for i in range(NUMB_OF_ELITE_SCHEDULES, POPULATION_SIZE):
            self._mutate_schedule(population.get_schedules()[i])
        return population

    def _crossover_schedule(self, schedule1, schedule2):
        crossoverSchedule = Schedule(self._data).initialize()
        for i in range(0, len(crossoverSchedule.get_classes())):
            if rnd.random() > 0.5:
                crossoverSchedule.get_classes()[i] = schedule1.get_classes()[i]
            else:
                crossoverSchedule.get_classes()[i] = schedule2.get_classes()[i]
        return crossoverSchedule

    def _mutate_schedule(self, mutateSchedule):
        schedule = Schedule(self._data).initialize()
        for i in range(len(mutateSchedule.get_classes())):
            if MUTATION_RATE > rnd.random():
                mutateSchedule.get_classes()[i] = schedule.get_classes()[i]
        return mutateSchedule

    def _select_tournament_population(self, pop):
        tournament_pop = Population(0, self._data)
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


def timetable(path=None, data=None):
    # log
    if not os.path.exists(path):
        os.makedirs(path)
    logger.add(os.path.join(path, 'schedule.log'), rotation="50 MB")

    # group classrooms by instructors
    groupby_instructors = defaultdict(list)
    all_classrooms = {}
    for d in data:
        all_classrooms[d['name']] = d
        for subject in d['subjects']:
            # only main subjects
            if (subject['n_lessons'] >= 3) and (d['name'] not in groupby_instructors[subject['instructor']]):
                groupby_instructors[subject['instructor']].append(d['name'])
    group_classrooms = set(list(map(tuple, sorted(groupby_instructors.values()))))
    group_classrooms = list(map(list, group_classrooms))

    # other classrooms
    other_classrooms = []
    for group_classroom in group_classrooms:
        for room in group_classroom:
            if room not in all_classrooms:
                other_classrooms.append(room)

    # aggregate classrooms
    group_classrooms.append(other_classrooms)
    group_classrooms = [x for x in group_classrooms if len(x)]
    group_classrooms = sorted(group_classrooms)
    for i in range(len(group_classrooms)):
        for j in range(len(group_classrooms[i])):
            group_classrooms[i][j] = all_classrooms[group_classrooms[i][j]]

    # save data
    with open(os.path.join(path, "data.txt"), "w") as f:
        json.dump(data, f, indent=2)

    # global vars
    temp_lessons = defaultdict(lambda: defaultdict(list))

    # optimize per batch
    process_start = time.time()
    for batch_data in group_classrooms:
        batch_data = Data(batch_data)
        # optimize per classroom
        room_idx = 0
        while room_idx < len(batch_data.get_classrooms()):
            classroom = batch_data.get_classrooms()[room_idx]
            # update free times for instructor
            for subject in classroom.subjects:
                if str(subject.instructor) in temp_lessons:
                    free_times = {}
                    busy_times = []
                    for room, time_slots in temp_lessons[str(subject.instructor)].items():
                        busy_times.extend(time_slots)
                    for meeting_time in batch_data.get_free_times():
                        if meeting_time not in busy_times:
                            free_times[meeting_time] = batch_data.get_free_times()[meeting_time]
                    subject.instructor.free_times = free_times

            # generate schedule per classroom
            schedule = []
            population = Population(POPULATION_SIZE, classroom)
            generation_num = 0
            population.get_schedules().sort(key=lambda x: x.get_fitness(), reverse=True)
            geneticAlgorithm = GeneticAlgorithm(classroom)
            job_start = time.time()
            while population.get_schedules()[0].get_fitness() != 1.0:
                generation_num += 1
                population = geneticAlgorithm.evolve(population)
                population.get_schedules().sort(key=lambda x: x.get_fitness(), reverse=True)
                schedule = population.get_schedules()[0].get_classes()
                logger.info('> Room #{}, Generation #{}, Number of conflicts #{}'.format(classroom, generation_num, population.get_schedules()[0]._numberOfConflicts))
                if time.time() - job_start > JOB_TIMEOUT:
                    logger.warning('> Job Time Limit Exceeded!')
                    break
                if time.time() - process_start > THREAD_TIMEOUT:
                    logger.error('Threading Time Limit Exceeded!')
                    os.kill(os.getpid(), signal.SIGKILL)

            if population.get_schedules()[0]._numberOfConflicts:
                # re-generate for batch
                room_idx = 0
                # remove meeting times
                for temp_classroom in batch_data.get_classrooms():
                    for temp_subject in temp_classroom.subjects:
                        if str(temp_subject.instructor) in temp_lessons:
                            temp_lessons[str(temp_subject.instructor)][str(temp_classroom.name)] = []
                continue

            # update free times for instructors
            for lesson in schedule:
                temp_lessons[str(lesson.instructor)][str(lesson.room)].append(str(lesson.meeting_time))

            # save only valid schedule
            result = {}
            idx2days = {'2': 'Monday', '3': 'Tuesday', '4': 'Wednesday', '5': 'Thursday', '6': 'Friday', '7': 'Saturday'}
            for idx, day in idx2days.items():
                result[day] = ['' for _ in range(5)]
            for lesson in schedule:
                result[idx2days[str(lesson.meeting_time.day)]][lesson.meeting_time.lesson - 1] = "{}_{}".format(lesson.subject, lesson.instructor)
            result['Monday'][0] = 'Chao Co'
            result['Saturday'][4] = 'SH Lop'

            logger.info("> Schedule #{}, Number of conflicts #{} \n {}".format(classroom, population.get_schedules()[0]._numberOfConflicts, pd.DataFrame(result).to_string()))
            with open(os.path.join(path, "{}.json".format(classroom)), "w") as f:
                json.dump(result, f, indent=2)

            room_idx += 1

    # terminate
    os.kill(os.getpid(), signal.SIGKILL)
