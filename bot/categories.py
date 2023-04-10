def parse_day_start_end(cmd) -> tuple[str, str, str]:
    date_list = cmd.split(' ')
    day = date_list[1]
    start_time = date_list[2].split('-')[0]
    end_time = date_list[2].split('-')[1]
    return day, start_time, end_time
