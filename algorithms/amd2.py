from collections import defaultdict
from itertools import product, permutations
import networkx as nx
import networkx.exception


# preferences = {
#     "p1": ["D", "C", "A", "B"],
#     "p2": ["C", "B", "A", "D"],
#     "p3": ["B", "D", "A", "C"],
#     "p4": ["D", "A", "B", "C"],
# }
#
# preferences = {
#     "p1": ["B", "C", "A", "D"],
#     "p2": ["A", "B", "C", "D"],
#     "p3": ["A", "D", "C", "B"],
#     "p4": ["B", "A", "C", "D"],
# }


def is_pareto_efficient(preferences: dict[str, list[str]], allocation):
    if isinstance(allocation, tuple) or isinstance(allocation, list):
        allocation = {k: v for k, v in zip(list(preferences.keys()), allocation)}
    blocks = []
    for human1 in preferences:
        got_human1 = allocation[human1]
        for human2 in preferences:
            got_human2 = allocation[human2]
            if human2 == human1:
                continue
            if preferences[human1].index(got_human2) < preferences[human1].index(
                    got_human1
            ) and preferences[human2].index(got_human1) < preferences[human2].index(
                got_human2
            ):
                # print(f"block: ", human2, human1)
                blocks.append((human2, human1))
    return len(blocks) == 0


def is_core(preferences, ownership, allocation):
    if isinstance(allocation, tuple) or isinstance(allocation, list):
        allocation = {k: v for k, v in zip(list(preferences.keys()), allocation)}
    if isinstance(ownership, tuple) or isinstance(ownership, list):
        ownership = {k: v for k, v in zip(list(preferences.keys()), ownership)}
    blocks = []
    for human in preferences:
        current = ownership[human]
        new = allocation[human]
        if preferences[human].index(new) > preferences[human].index(current):
            # print(f"block: {human}")
            blocks.append(human)
    return (len(blocks) == 0) and is_pareto_efficient(preferences, allocation)


def generate_all_possible_allocations(preferences):
    return list(permutations(list(preferences.values())[0]))


class SerialDictatorship:
    def __init__(self, preferences: dict[str, list[str]]):
        self.preferences = preferences
        self.__preferences_copy = {k: list(v) for k, v in preferences.items()}

    def remove_key(self, key: str) -> None:
        """
        Removes key from preferences to reorder them
        :param key: str, key to remove
        :return: None
        """

        self.__preferences_copy = {
            k: [i for i in v if i != key] for k, v in self.__preferences_copy.items()
        }

    def generate_all_orders(self):
        return list(permutations(self.__preferences_copy))

    def check_all_orders(self):
        orders = self.generate_all_orders()
        results = {}
        for order in orders:
            results[order] = self.run(order)
        return results

    def find_all_res(self):
        seen = []
        for v in self.check_all_orders().values():
            if v not in seen:
                seen.append(v)
        return seen

    def find_all_pe(self):
        res = []
        for perm in permutations(list(self.preferences.values())[0]):
            if is_pareto_efficient(self.preferences, perm):
                res.append(perm)
        return res

    def run(self, order=None):
        """
        Run algorithm
        :param order: specify keys in desirable order
        :return:
        """
        if order is None:
            order = list(self.preferences.keys())
        self.__preferences_copy = {k: list(v) for k, v in self.preferences.items()}
        result = {k: None for k in self.preferences.keys()}
        for human in order:
            key = self.__preferences_copy[human][0]
            result[human] = key
            self.remove_key(key)
        return result


class TopTradingCycle:
    def __init__(self, preferences):
        self.preferences = preferences
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
            graph.add_edge(v, k)
        return graph

    def remove_cycles(self, graph, results, silent):
        cycles = nx.find_cycle(graph)[1::2]
        if cycles[0][0] not in self.__preferences.keys():
            cycles = [(y, x) for x, y in cycles]
        if not silent:
            print("Cycle", nx.find_cycle(graph))
        for (human1, item1), (human2, item2) in zip(cycles[1:] + [cycles[0]], cycles[:-1] + [cycles[-1]]):
            graph.remove_nodes_from([human1, item1, item2, human2])
            self.remove_key(item1)
            self.__preferences.pop(human1)
            results[human1] = item1
        return results

    def run(self, ownership, silent=True):
        graph = self.initialize_graph(ownership)
        results = {k: None for k in list(self.preferences)}
        while None in results.values():
            all_points = {human: human_prefs[0] for human, human_prefs in self.__preferences.items()}
            for k, v in all_points.items():
                graph.add_edge(k, v)
            try:
                results = self.remove_cycles(graph, results, silent=silent)
            except networkx.exception.NetworkXNoCycle:
                pass
        return results


class PriorityLine(TopTradingCycle):
    def __init__(self, preferences):
        self.preferences = preferences
        super().__init__(preferences)
        self.__preferences = {k: list(v) for k, v in preferences.items()}

    def remove_key(self, key):
        self.__preferences = {
            k: [i for i in v if i != key] for k, v in self.__preferences.items()
        }

    def run(self, ownership, order=None, silent=False):
        if order is None:
            order = list(self.preferences.keys())
        graph = self.initialize_graph(ownership)
        results = {k: None for k in list(self.preferences)}
        queue = {}
        while order:
            human = order[0]
            desired_item = self.__preferences[human][0]
            if graph.has_node(desired_item) and len(graph[desired_item]):
                owner = list(graph[desired_item].keys())[0]
                if owner in order and owner not in queue:
                    if not silent:
                        print(f"{human} wants {desired_item}, but it's occupied by {owner}.")
                    if order.index(owner) >= order.index(human):
                        order.remove(owner)
                        order.insert(0, owner)
                        order.append(human)
                        queue[human] = desired_item
                        continue
                else:
                    if not silent:
                        print(f"{human} requests {desired_item}")
                    if owner in queue:
                        if not silent:
                            print(f"Time for {owner} to request {queue[owner]}")
                        graph.add_edge(owner, queue.pop(owner))
            else:
                print(f"{human} takes {desired_item}")
                graph.add_edge(desired_item, human)
            graph.add_edge(human, desired_item)
            try:
                results = super().remove_cycles(graph, results, silent=silent)
                order = [x for x in order if results[x] is None]
            except networkx.exception.NetworkXNoCycle:
                pass
        return results


preferences = {
    "p1": list("DABC"),
    'p2': list("DBCA"),
    'p3': list("CABD"),
    'p4': list("CDBA")
}
ownership = {"p2": "A", "p3": "B"}
algorithm = PriorityLine(preferences)
res = algorithm.run(ownership, order=['p' + x for x in list('1243')], silent=False)
print(res)
print(list(res.values()))
print(is_pareto_efficient(preferences, list(res.values())))
