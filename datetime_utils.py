def format_days(d):
	days_dict = {'M': "MO", 'T':"TU", 'W':"WE", 'R': "TH", 'F':"FR"}

	days = list(d)

	ret = ""

	for i in range(0, len(days)):
		char = days[i]
		ret += days_dict.get(char)
		if (i != (len(days) - 1)):
			ret += ","

	return ret

def get_times(times):
	start_time, end_time = times.split(" - ", 1)
	start_time = format_time(start_time)
	end_time = format_time(end_time)
	return start_time, end_time

def format_time(t):
	time, ampm = t.split(' ', 1)
	hours, minutes = time.split(':', 1)
	hours = int(hours)
	if ampm == "am":
		if hours == 12:
			hours = "00"
		else:
			if hours < 10:
				hours = "0" + str(hours)
			else:
				hours = str(hours)
	else:
		if hours == 12:
			hours = "12"
		else:
			hours = str(hours + 12)
	return (hours + ":" + minutes)

def format_start(date, start_day):
	days_to_add_dict = {"MO": 0, "TU": 1, "WE": 2, "TH": 3, "FR": 4}
	month_dict = {"Jan": "01", "Feb": "02", "Mar": "03", "Apr": "04", "May": "05", "Jun": "06", "Jul": "07", "Aug": "08", "Sep": "09", "Oct": "10", "Nov": "11", "Dec": "12"}
	month, day_year = date.split(' ', 1)
	day, year = day_year.split(", ", 1)
	day = str(int(day) + days_to_add_dict[start_day])
	retDate = year + "-" + month_dict[month] + "-" + day
	return retDate

def format_end(date):
	month_dict = {"Jan": "01", "Feb": "02", "Mar": "03", "Apr": "04", "May": "05", "Jun": "06", "Jul": "07", "Aug": "08", "Sep": "09", "Oct": "10", "Nov": "11", "Dec": "12"}
	month, day_year = date.split(' ', 1)
	day, year = day_year.split(", ", 1)
	retDate = year + month_dict[month] + day
	return retDate

def get_start_and_end(date_range, start_day):
	start, end = date_range.split(" - ")
	start = format_start(start, start_day)
	end = format_end(end)
	return start, end