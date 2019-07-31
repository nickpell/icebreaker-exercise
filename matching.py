def match(user_ids, match_history):
    user_to_unmatched, user_to_next_match = get_unmatched_and_next_matches(user_ids, match_history)
    return get_optimal_matches(user_to_unmatched, user_to_next_match)


def get_unmatched_and_next_matches(user_ids, match_history):
    user_to_next_match = {user: [] for user in user_ids}
    user_to_unmatched = {user: set(user_ids) - set(user) for user in user_ids}
    for historical_match in reversed(match_history):
        user_1 = historical_match[0]
        user_2 = historical_match[1]
        # These two if-blocks are a candidate for de-duplication via a helper function.
        # I prefer using the rule of 3 - only de-duplicate if code is repeated 3 times, but you could
        # make a case for de-duplicating here.
        if user_2 in user_to_unmatched[user_1]:
            user_to_unmatched[user_1].remove(user_2)
            user_to_next_match[user_1].insert(0, user_2)
        if user_1 in user_to_unmatched[user_2]:
            user_to_unmatched[user_2].remove(user_1)
            user_to_next_match[user_2].insert(0, user_1)
    return user_to_unmatched, user_to_next_match


def get_optimal_matches(user_to_unmatched, user_to_next_match):
    if not user_to_unmatched:
        return []
    users_to_match = set(user_to_next_match)
    # break ties by user id for deterministic tests
    # TODO - refactor this into helper function and use Python's mock library to guarantee
    # deterministic sorting.  In production, we might not need this function to be deterministic,
    # and providing a second sort key (user) adds overhead.
    users_by_most_matched = sorted(user_to_next_match,
        key=lambda user: (len(user_to_next_match[user]), user), reverse=True)

    next_user_to_match = users_by_most_matched[0]
    users_to_match.remove(next_user_to_match)
    unmatched_users = user_to_unmatched[next_user_to_match] & users_to_match
    if unmatched_users:
        matched_user = next(filter(lambda user: user in unmatched_users, users_by_most_matched))
    else:
        matched_user = next(filter(lambda user: user in users_to_match, user_to_next_match[next_user_to_match]))
    users_to_match.remove(matched_user)

    next_user_to_unmatched = {
        user: {x for x in user_to_unmatched[user] if x not in [next_user_to_match, matched_user]} for user in user_to_unmatched
        if user not in [next_user_to_match, matched_user]
    }
    next_user_to_next_match = {
        user: [x for x in user_to_next_match[user] if x not in [next_user_to_match, matched_user]] for user in user_to_next_match
        if user not in [next_user_to_match, matched_user]
    }
    return [(next_user_to_match, matched_user)] + get_optimal_matches(next_user_to_unmatched, next_user_to_next_match)


# TODO - use Python's unittest framework
def run_test(user_ids, match_history, expected_matching):
    assert match(user_ids, match_history) == expected_matching, match(user_ids, match_history)

# Tests based on the given sequences
run_test(['A', 'B', 'C', 'D'], [],
         [('D', 'C'), ('B', 'A')])
run_test(['A', 'B', 'C', 'D'], [['D', 'C'], ['B', 'A']],
         [('D', 'B'), ('C', 'A')])
run_test(['A', 'B', 'C', 'D'], [['D', 'C'], ['B', 'A'], ['D', 'B'], ['C', 'A']],
         [('D', 'A'), ('C', 'B')])
run_test(['A', 'B', 'C', 'D'], [['D', 'C'], ['B', 'A'], ['D', 'B'], ['C', 'A'], ['D', 'A'], ['C', 'B']],
         [('D', 'C'), ('B', 'A')])

# Other sequences:

# Partial histories
run_test(['A', 'B', 'C', 'D'], [['A', 'B'], ['A', 'C']],
         [('A', 'D'), ('C', 'B')])
run_test(['A', 'B', 'C', 'D'], [['A', 'B'], ['A', 'C'], ['A', 'B']],
         [('A', 'D'), ('C', 'B')])

# When repeating matches, try to match with least recently matched user
run_test(['A', 'B', 'C', 'D'], [['A', 'B'], ['A', 'C'], ['A', 'B'], ['A', 'D']],
         [('A', 'C'), ('D', 'B')])
