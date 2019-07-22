def match(user_ids, match_history):
    user_to_unmatched, user_to_next_match = get_unmatched_and_next_matches(user_ids, match_history)
    return get_optimal_matches(user_to_unmatched, user_to_next_match)


def get_unmatched_and_next_matches(user_ids, match_history):
    user_to_next_match = {user: [] for user in user_ids}
    user_to_unmatched = {user: set(user_ids) - set(user) for user in user_ids}
    for historical_match in reversed(match_history):
        user_1 = historical_match[0]
        user_2 = historical_match[1]
        if user_2 in user_to_unmatched[user_1]:
            user_to_unmatched[user_1].remove(user_2)
            user_to_next_match[user_1].insert(0, user_2)
        if user_1 in user_to_unmatched[user_2]:
            user_to_unmatched[user_2].remove(user_1)
            user_to_next_match[user_2].insert(0, user_1)
    return user_to_unmatched, user_to_next_match


def get_optimal_matches(user_to_unmatched, user_to_next_match):
    matches = []
    users_to_match = set(user_to_next_match)
    # break ties by user id for deterministic tests
    users_by_most_matched = sorted(user_to_next_match,
        key=lambda user: (len(user_to_next_match[user]), user), reverse=True)

    for next_user_to_match in users_by_most_matched:
        if next_user_to_match not in users_to_match:
            continue
        users_to_match.remove(next_user_to_match)
        unmatched_users = user_to_unmatched[next_user_to_match] & users_to_match
        if unmatched_users:
            matched_user = next(filter(lambda user: user in unmatched_users, users_by_most_matched))
        else:
            matched_user = next(filter(lambda user: user in users_to_match, user_to_next_match[next_user_to_match]))
        users_to_match.remove(matched_user)
        matches.append([next_user_to_match, matched_user])
    return matches


def run_test(user_ids, match_history, expected_matching):
    assert match(user_ids, match_history) == expected_matching, expected_matching

# Tests based on the given sequences
run_test(['A', 'B', 'C', 'D'], [],
         [['D', 'C'], ['B', 'A']])
run_test(['A', 'B', 'C', 'D'], [['D', 'C'], ['B', 'A']],
         [['D', 'B'], ['C', 'A']])
run_test(['A', 'B', 'C', 'D'], [['D', 'C'], ['B', 'A'], ['D', 'B'], ['C', 'A']],
         [['D', 'A'], ['C', 'B']])
run_test(['A', 'B', 'C', 'D'], [['D', 'C'], ['B', 'A'], ['D', 'B'], ['C', 'A'], ['D', 'A'], ['C', 'B']],
         [['D', 'C'], ['B', 'A']])

# Other sequences:
run_test(['A', 'B', 'C', 'D'], [['A', 'B'], ['A', 'C']],
         [['A', 'D'], ['C', 'B']])
