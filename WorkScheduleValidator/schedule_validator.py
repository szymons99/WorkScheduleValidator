from datetime import datetime, timedelta
import calendar
def read_schedule_from_file(file_name):
    schedule = {}
    try:
        with open(file_name, 'r') as file:
            for line in file:
                day, hours = line.strip().split(',')
                schedule[int(day)] = int(hours)
    except FileNotFoundError:
        print("File not found.")
    return schedule

def count_calendar_workdays():
    calendar_workdays = 0
    cal = calendar.Calendar()

    for week in cal.monthdayscalendar(2023, 8):
        for i, day in enumerate(week):
            # not this month's day or a weekend
            if day == 0 or i == 6: # 6 is Sunday
                continue
            calendar_workdays += 1
    return calendar_workdays

def count_overtime_hours(schedule):
    total_overtime = 0

    for day, hours in schedule.items():
        day_date = datetime(year=2023, month=8, day=day)
        if day_date.weekday() == 6 and hours > 0:  # Sunday
            total_overtime += hours
            print("Validation 2: Work is planned on a Sunday:", day_date.strftime("%d-%m"))
        elif 0 <= day_date.weekday() <= 5:  # Monday - Saturday
            total_overtime += max(0, hours - 8)

    # Calculate Sunday overtime
    sunday_hours = schedule.get(7, 0)
    total_overtime += max(0, sunday_hours - 8)
    return total_overtime

def validate_schedule(schedule):
    total_workhours = sum(schedule.values())

    if total_workhours > 8 * count_calendar_workdays():
        print("Validation 1: Total work hours exceeded.")

    print("Validation 3: Total overtime hours:", count_overtime_hours(schedule))

    for i in range(1, 31):
        if i in schedule and i + 1 in schedule:
            current_day_end = datetime(year=2023, month=8, day=i, hour=0) + timedelta(hours=schedule[i])
            next_day_start = datetime(year=2023, month=8, day=i + 1, hour=0)
            if next_day_start - current_day_end < timedelta(hours=11):
                print("Validation 4: Less than 11 hours between days", i, "and", i + 1)

def main():
    file_name = "schedule1.txt"
    schedule = read_schedule_from_file(file_name)
    if schedule:
        validate_schedule(schedule)

if __name__ == "__main__":
    main()