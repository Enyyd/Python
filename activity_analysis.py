def parse_log(log):
    # приймає список логів і повертає список кортежів
    parsed = []
    for entry in log:
        user_id, timestamp = entry.split(',')
        date, time = timestamp.strip().split(' ')
        year, month, day = map(int, date.split('-'))
        hour, minute, second = map(int, time.split(':'))
        parsed.append((user_id.strip(), (year, month, day, hour, minute, second)))
    return parsed

def calculate_activity(logs):
    """
    Аналізує активність користувачів:
    Загальну кількість активностей
    Кількість унікальних користувачів
    Найактивнішого користувача
    Метрики активності за днями
    """
    total_activities = len(logs)
    user_activities = {}
    daily_activities = {}

    for user_id, timestamp in logs:
        # активність користувачів
        user_activities[user_id] = user_activities.get(user_id, 0) + 1

        # активність за днями
        day = (timestamp[0], timestamp[1], timestamp[2])
        daily_activities[day] = daily_activities.get(day, 0) + 1

    unique_users = len(user_activities)
    most_active_user = max(user_activities, key=user_activities.get)
    return {
        "total_activities": total_activities,
        "unique_users": unique_users,
        "most_active_user": most_active_user,
        "daily_activities": daily_activities,
    }

# txt файл
def save_to_file(stats, filename="activity_report.txt"):
    with open(filename, "w") as file:
        file.write("User Activity Analysis:\n")
        file.write(f"Total number of activities: {stats['total_activities']}\n")
        file.write(f"Number of unique users: {stats['unique_users']}\n")
        file.write(f"Most active user: {stats['most_active_user']}\n")
        file.write("Activity by day:\n")
        for day, count in stats['daily_activities'].items():
            file.write(f"  {day}: {count}\n")

#тести
def test_parse_log():
    log = ["user1, 2024-12-20 12:00:00", "user2, 2024-12-20 13:00:00"]
    parsed = parse_log(log)
    assert parsed == [
        ("user1", (2024, 12, 20, 12, 0, 0)),
        ("user2", (2024, 12, 20, 13, 0, 0)),
    ], "parse_log test failed!"

def test_calculate_activity():
    logs = [
        ("user1", (2024, 12, 20, 12, 0, 0)),
        ("user2", (2024, 12, 20, 13, 0, 0)),
        ("user1", (2024, 12, 21, 17, 0, 0)),
        ("user3", (2024, 12, 20, 15, 0, 0)),
        ("user1", (2024, 12, 22, 16, 0, 0)),
    ]
    stats = calculate_activity(logs)

    #обчислення значень активності
    expected_total_activities = len(logs)
    expected_unique_users = len(set(log[0] for log in logs))
    expected_user_activity = {user_id: sum(1 for log in logs if log[0] == user_id) for user_id, _ in logs}
    expected_most_active_user = max(expected_user_activity, key=expected_user_activity.get)

    expected_daily_activities = {}
    for _, timestamp in logs:
        day = timestamp[:3]  # (рік, місяць, день)
        expected_daily_activities[day] = expected_daily_activities.get(day, 0) + 1

    # Автоматичні перевірки
    assert stats["total_activities"] == expected_total_activities, "Erorre"
    assert stats["unique_users"] == expected_unique_users,"Erorre"
    assert stats["most_active_user"] == expected_most_active_user,"Erorre"
    assert stats["daily_activities"] == expected_daily_activities,"Erorre"

def run_tests():
    test_parse_log()
    test_calculate_activity()

if __name__ == "__main__":
    logs = [
        "user1, 2024-12-20 12:00:00",
        "user2, 2024-12-20 13:00:00",
        "user1, 2024-12-21 14:00:00",
        "user3, 2024-12-20 15:00:00",
        "user1, 2024-12-22 16:00:00",
        "user3, 2024-12-22 16:00:00",
        "user1, 2024-12-22 16:00:00",
        "user4, 2024-12-23 12:00:00",
    ]

    parsed_logs = parse_log(logs)
    activity_stats = calculate_activity(parsed_logs)

    save_to_file(activity_stats)
    run_tests()