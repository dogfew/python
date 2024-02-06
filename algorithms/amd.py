from collections import defaultdict
from itertools import product, permutations


def male_without_match(matches, males):
    for male in males:
        if male not in matches:
            return male


def deferred_acceptance(male_prefs, female_prefs, silent=False):
    female_queue = defaultdict(int)

    males = list(male_prefs.keys())

    matches = {}

    while True:
        male = male_without_match(matches, males)
        if not male:
            break

        female_index = female_queue[male]
        female_queue[male] += 1

        try:
            female = male_prefs[male][female_index]
        except IndexError:
            matches[male] = male
            continue
        if not silent:
            print("Trying %s with %s... " % (male, female), end="")

        prev_male = matches.get(female, None)
        if male not in female_prefs[female]:
            print("rejected")
            continue
        if not prev_male:
            matches[male] = female
            matches[female] = male
            if not silent:
                print("auto")
        elif female_prefs[female].index(male) < female_prefs[female].index(prev_male):
            matches[male] = female
            matches[female] = male

            del matches[prev_male]
            if not silent:
                print("matched")
        elif not silent:
            print("rejected")
    return {male: matches[male] for male in male_prefs.keys()}


def check_stable(male_prefs, female_prefs, pairs):
    pairs_woman = {v: k for k, v in pairs.items()}
    pairs_man = pairs
    pairs_man.update({k: None for k in set(male_prefs) - set(pairs_man)})
    pairs_woman.update({k: None for k in set(female_prefs) - set(pairs_woman)})
    blocking_pairs = []
    for male in male_prefs:
        current_match = pairs_man[male]
        if current_match not in male_prefs[male] and current_match is not None:
            blocking_pairs.append((male, male))
        for i, woman in enumerate(male_prefs[male]):
            if woman == current_match:
                break
            try:
                current_female_match = pairs_woman[woman]
                if current_female_match is not None:
                    curr_female_match_index = female_prefs[woman].index(
                        current_female_match
                    )
                else:
                    curr_female_match_index = len(female_prefs[woman])
                potential_female_match_index = female_prefs[woman].index(male)
                if potential_female_match_index < curr_female_match_index:
                    blocking_pairs.append((male, woman))
            except Exception as e:
                blocking_pairs.append((woman, woman))
    return blocking_pairs


def all_possible_combinations(male_prefs, female_prefs, current_match={}):
    males = list(male_prefs.keys())
    females = list(female_prefs.keys())

    if len(current_match) == len(males):
        return [current_match.copy()]

    current_male = males[len(current_match)]
    possible_matches = []

    for female in females + [None]:
        if female is None or female not in current_match.values():
            current_match[current_male] = female
            possible_matches.extend(
                all_possible_combinations(male_prefs, female_prefs, current_match)
            )
            current_match.pop(current_male)

    return possible_matches


def all_stable_combinations(male_prefs, female_prefs):
    res = []
    for pairs in all_possible_combinations(male_prefs, female_prefs):
        if len(check_stable(male_prefs, female_prefs, pairs)) == 0:
            res.append(pairs)
    return res


def get_achievable_parners(male_prefs, female_prefs):
    """wrt to male"""
    stable_combinations = all_stable_combinations(male_prefs, female_prefs)
    return {
        male: set(
            stable_combination.get(male, None)
            for stable_combination in stable_combinations
        )
        for male in male_prefs
    }


def make_priorities(
    male_prefs,
    female_prefs,
):
    priorities = []
    for i in range(len(male_prefs)):
        for j in range(len(female_prefs)):
            if j != i and (j, i) not in priorities:
                priorities.append((j, i))
            if (i, j) not in priorities:
                priorities.append((i, j))
    return priorities


def priority_match(male_prefs, female_prefs, priorities=None, silent=False):
    from copy import deepcopy

    priorities = [(i - 1, j - 1) for i, j in priorities]
    if priorities is None:
        priorities = make_priorities()
    male_prefs_copy = deepcopy(male_prefs)
    female_prefs_copy = deepcopy(female_prefs)
    pairs = {}
    i = 0
    while len(female_prefs_copy) != 0 or len(male_prefs_copy) != 0:
        flag = False
        for i, j in priorities:
            matches_men = {man: prefs[i] for man, prefs in male_prefs_copy.items()}
            for woman, prefs in female_prefs_copy.items():
                man = prefs[j]
                if man in matches_men.keys() and matches_men[prefs[j]] == woman:
                    print(f"Match: ({i+1}-{j+1})", man, woman)
                    # male_prefs_copy = {
                    #     k: [v for v in prefs if v != woman]
                    #     for k, prefs in male_prefs_copy.items()
                    #     if k != man
                    # }
                    # female_prefs_copy = {
                    #     k: [v for v in prefs if v != man]
                    #     for k, prefs in female_prefs_copy.items()
                    #     if k != woman
                    # }
                    pairs[man] = woman
                    flag = True
            for man, woman in pairs.items():
                male_prefs_copy = {
                    k: [v for v in prefs if v != woman]
                    for k, prefs in male_prefs_copy.items()
                    if k != man
                }
                female_prefs_copy = {
                    k: [v for v in prefs if v != man]
                    for k, prefs in female_prefs_copy.items()
                    if k != woman
                }
            if flag:
                break
    return pairs


male_prefs = {
    "m1": ["w2", "w3", "w1"],
    "m2": ["w1", "w3", "w2"],
    "m3": ["w1", "w3", "w2"],
}

female_prefs = {
    "w1": ["m1", "m2", "m3"],
    "w2": ["m2", "m3", "m1"],
    "w3": ["m1", "m3", "m2"],
}

res = priority_match(
        male_prefs,
        female_prefs,
        priorities=(
            [(1, 1), (2, 1), (1, 2),
              (1, 3), (3, 1), (2, 2),
              (3, 2), (2, 3), (3, 3)]
        ),
    )
print(res)
print(check_stable(male_prefs, female_prefs, res))

# for pairs in [
#     {"Joey": "Rachel", "Chandler": "Phoebe"},
#     {"Joey": "Rachel", "Ross": "Monica", "Chandler": "Phoebe"},
#     {"Ross": "Rachel", "Joey": "Monica", "Chandler": "Phoebe"},
#     deferred_acceptance(student_prefs, school_prefs),
#     {v: k for k, v in deferred_acceptance(school_prefs, student_prefs).items()},
# ]:
#     check_stable(student_prefs, school_prefs, pairs)

# print((male_prefs, female_prefs))
# print(get_achievable_parners(male_prefs, female_prefs))
# # print(all_stable_combinations(student_prefs, school_prefs))
# print(deferred_acceptance(student_prefs, school_prefs))
# print(deferred_acceptance(student_prefs, school_prefs))
# print(get_achievable_parners(student_prefs, school_prefs))


# student_prefs = {f"m{i}":[] for i in range(1, 4)}
# school_prefs = {f"f{i}" :[] for i in range(1, 6)}

# combos = [d
#         for d in
#         all_possible_combinations(student_prefs, school_prefs)
#         if None not in d.values()]
# print(len(combos))
