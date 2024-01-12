from collections import defaultdict

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
            print('Trying %s with %s... ' % (male, female), end='')

        prev_male = matches.get(female, None)
        if male not in female_prefs[female]:
            print("rejected")
            continue
        if not prev_male:
            matches[male] = female
            matches[female] = male
            if not silent:
                print('auto')
        elif female_prefs[female].index(male) < \
             female_prefs[female].index(prev_male):
            matches[male] = female
            matches[female] = male

            del matches[prev_male]
            if not silent:
                print('matched')
        elif not silent:
            print('rejected')
    return {male: matches[male] for male in male_prefs.keys()}






def check_stable(male_prefs, female_prefs, pairs):
    pairs_woman = {v:k for k, v in pairs.items()}
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
                    curr_female_match_index = female_prefs[woman].index(current_female_match)
                else:
                    curr_female_match_index = len(female_prefs[woman])
                potential_female_match_index = female_prefs[woman].index(male)
                if potential_female_match_index < curr_female_match_index:
                    blocking_pairs.append((male, woman))
            except Exception as e:
                blocking_pairs.append((woman, woman))
    return blocking_pairs


male_prefs = {
    "Joey": ["Rachel", "Monica", "Phoebe"],
    "Ross": ["Rachel", "Phoebe"],
    "Chandler": ["Monica", "Phoebe", "Rachel"]
}

female_prefs = {
    "Rachel": ["Ross", "Joey", "Chandler"],
    "Monica": ["Chandler", "Joey"],
    "Phoebe": ["Joey", "Ross", "Chandler"]
}

for pairs in [
    {"Joey": "Rachel", "Chandler": "Phoebe"},
    {"Joey": "Rachel", "Ross": "Monica", "Chandler": "Phoebe"},
    {"Ross": "Rachel", "Joey": "Monica", "Chandler": "Phoebe"},
    deferred_acceptance(male_prefs, female_prefs),
    {v:k for k, v in deferred_acceptance(female_prefs, male_prefs).items()}
]:
    print(check_stable(male_prefs, female_prefs, pairs))
    print()
