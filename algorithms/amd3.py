from itertools import product, permutations
import pandas as pd
import networkx as nx
import networkx.exception

preferences = {
    "s1": ["A", "B", "C"],
    "s2": ["C", "B", "A"],
    "s3": ["C", "A", "B"],
    "s4": ["A", "C", "B"],
    "s5": ["C", "A", "B"]
}

schools = {
    "preferences":
        {"A": ['s2', 's3', 's5', 's4', 's1'],
         "B": ['s3', 's2', 's5', 's4', 's1'],
         'C': ['s4', 's5', 's1', 's2', 's3']
         },
    "seats":
        {
            "A": 1, "B": 2, "C": 1
        }
}


def boston_mechanism(preferences, schools):
    assignments = {k: None for k in preferences}
    prefs_copy = preferences.copy()
    free_seats = schools['seats'].copy()
    while len(prefs_copy) and sum(free_seats.values()):
        for seat, num_seats in free_seats.items():
            candidates = [k for k, v in prefs_copy.items() if v[0] == seat]
            schools_prefs = schools['preferences'][seat]
            priorities = {k: v for v, k in enumerate(schools_prefs)}
            sorted_candidates = sorted(candidates, key=lambda x: priorities[x])[:num_seats]
            for candidate in sorted_candidates:
                assignments[candidate] = seat
                free_seats[seat] -= 1
                prefs_copy.pop(candidate)
        prefs_copy = {k: v[1:] for k, v in prefs_copy.items()}
    return assignments


from collections import defaultdict


def deferred_acceptance(student_preferences, school_preferences, school_seats, silent=False):
    student_queue = defaultdict(int)
    students = list(student_preferences.keys())
    schools = list(school_preferences.keys())
    matches = {school: [] for school in schools}  # Initialize all schools with empty student lists
    unmatched_students = set(student_preferences.keys())  # Initialize all students as unmatched

    while unmatched_students:
        student = unmatched_students.pop()

        if not silent:
            print(f"\nStudent {student} is currently unmatched. Checking their preferences.")

        while student_queue[student] < len(student_preferences[student]):
            school = student_preferences[student][student_queue[student]]
            student_queue[student] += 1

            if not silent:
                print(f"Student {student} is proposing to School {school}.")

            if student in school_preferences[school]:
                current_students = matches[school]
                if len(current_students) < school_seats[school]:
                    # There's room in the school for the student
                    matches[school].append(student)
                    if not silent:
                        print(f"School {school} accepts Student {student}.")
                    break
                else:
                    all_students = current_students + [student]
                    ranked_students = sorted(all_students, key=lambda s: school_preferences[school].index(s))
                    if ranked_students.index(student) < len(current_students):
                        replaced_student = ranked_students[-1]
                        matches[school].remove(replaced_student)
                        matches[school].append(student)
                        unmatched_students.add(replaced_student)
                        if not silent:
                            print(f"School {school} replaces Student {replaced_student} with Student {student}.")
                        break
                    else:
                        if not silent:
                            print(f"Student {student} is rejected by School {school} (no higher preference).")
            else:
                if not silent:
                    print(f"Student {student} is not listed in School {school}'s preferences. Rejected.")

            if student_queue[student] == len(student_preferences[student]):
                if not silent:
                    print(f"Student {student} has exhausted their preference list. No more schools to propose to.")
    answer = {student: school for school, students in matches.items() for student in students}

    return {student: answer.get(student) for student in students}


def is_pareto_efficient(preferences: dict[str, list[str]], allocation):
    if isinstance(allocation, tuple) or isinstance(allocation, list):
        allocation = {k: v for k, v in zip(list(preferences.keys()), allocation)}
    blocks = []
    for human1 in preferences:
        got_human1 = allocation.get(human1)
        if got_human1 is None:
            continue
        for human2 in preferences:
            got_human2 = allocation.get(human2)
            if got_human2 is None:
                continue
            if human2 == human1:
                continue
            if preferences[human1].index(got_human2) < preferences[human1].index(
                    got_human1
            ) and preferences[human2].index(got_human1) < preferences[human2].index(
                got_human2
            ):
                # print(f"block: ", human2, human1)
                blocks.append((human2, human1))
    print(blocks)
    return len(blocks) == 0


class TopTradingCycle:
    def __init__(self, preferences, seats):
        self.preferences = preferences
        self.seats = seats
        self.__preferences = {k: list(v) for k, v in preferences.items()}

    def remove_key(self, key):
        self.__preferences = {
            k: [i for i in v if i != key] for k, v in self.__preferences.items()
        }

    def initialize_graph(self, ownership):
        if isinstance(ownership, tuple) or isinstance(ownership, list):
            ownership = {k: v for k, v in zip(list(self.preferences.keys()), ownership)}
        graph = nx.DiGraph()
        for k, v in ownership.items():
            graph.add_edge(k, v)
        return graph

    def remove_cycles(self, graph, results, silent):
        cycles = nx.find_cycle(graph)[1::2]
        if cycles[0][0] not in self.__preferences.keys():
            cycles = [(y, x) for x, y in cycles]
        if not silent:
            print("Cycle", nx.find_cycle(graph))
        for (human1, item1), (human2, item2) in zip(cycles[1:] + [cycles[0]], cycles[:-1] + [cycles[-1]]):
            graph.remove_nodes_from([human1, item1, item2, human2])
            self.seats[item1] -= 1
            if self.seats[item1] == 0:
                self.remove_key(item1)
            self.__preferences.pop(human1)
            results[human1] = item1
        return results

    def run(self, school_preferences, silent=True):
        ownership = {school: v[0] for school, v in school_preferences.items()}
        graph = self.initialize_graph(ownership)
        results = {k: None for k in list(self.preferences)}
        while None in results.values() and sum(self.seats.values()) != 0:
            all_points = {human: human_prefs[0] for human, human_prefs in self.__preferences.items()}
            for k, v in all_points.items():
                graph.add_edge(k, v)
            try:
                results = self.remove_cycles(graph, results, silent=silent)
            except networkx.exception.NetworkXNoCycle:
                pass
            for school, num_seats in self.seats.items():
                if num_seats != 0 and not graph.out_edges(school):
                    start_assignment = [v for v in school_preferences[school] if results[v] is None][0]
                    graph.add_edge(school, start_assignment)
        return results

# preferences = {
#     "s1": ["A", "B", "C"],
#     "s2": ["C", "B", "A"],
#     "s3": ["C", "A", "B"],
#     "s4": ["A", "C", "B"]
# }

# schools['preferences'] = {
#     "A": ["s2", "s3", "s1", "s4"],
#     "B": ["s2", "s4", "s3", "s1"],
#     "C": ["s2", "s1", "s4", "s3"]
# }
#
# schools['seats'] = {
#     "A": 1,
#     "B": 1,
#     "C": 2
# }

result = TopTradingCycle(preferences, seats=schools['seats']).run(schools['preferences'], silent=False)
de_result = deferred_acceptance(student_preferences=preferences, school_preferences=schools['preferences'], school_seats=schools['seats'])
print(result)
print(is_pareto_efficient(preferences, result))