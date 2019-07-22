def match(user_ids, match_history):
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
        # TODO - break if each user has been matched with each other user
    matches = []
    users_to_match = set(user_ids)
    while users_to_match:
        next_user_to_match = users_to_match.pop()
        unmatched_users = user_to_unmatched[next_user_to_match] & users_to_match
        if unmatched_users:
            matched_user = unmatched_users.pop()
        else:
            matched_user = user_to_next_match[next_user_to_match][0]
        # print((next_user_to_match, matched_user))
        users_to_match.remove(matched_user)
        matches.append([next_user_to_match, matched_user])
    return matches


print(match(['A', 'B', 'C', 'D'], []))
print(match(['A', 'B', 'C', 'D'], [['A', 'C'], ['B', 'D']]))
print(match(['A', 'B', 'C', 'D'], [['A', 'C'], ['B', 'D'], ['A', 'B'], ['C', 'D']]))
print(match(['A', 'B', 'C', 'D'], [['A', 'C'], ['B', 'D'], ['A', 'B'], ['C', 'D'], ['A', 'D'], ['C', 'B']]))
