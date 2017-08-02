from bs4 import BeautifulSoup
import datetime_utils as dt
import enterprise_navigation

def get_courses():
	enterprise_navigation.get_schedule_page()
	soup = BeautifulSoup(open("schedule.html"), "html.parser")

	captions = soup.find_all("caption", class_="captiontext")

	class_names     = []
	class_times     = []
	class_days      = []
	class_locations = []
	class_length    = []
	class_type      = []

	for caption in captions:
		if caption.text != "Scheduled Meeting Times":
			class_names.append(caption.text)

	details = soup.find_all("td", class_="dddefault")

	for i in range (9, len(details), 15):
	  class_times.append(details[i].text)
	  class_days.append(details[i+1].text)
	  class_locations.append(details[i+2].text)
	  class_length.append(details[i+3].text)
	  class_type.append(details[i+4].text)

	courses = []

	for i in range(0, len(class_names)):
		days = dt.format_days(class_days[i])
		start_day_of_week = days[:2]
		start_time, end_time = dt.get_times(class_times[i])
		start_day, end_day = dt.get_start_and_end(class_length[i], start_day_of_week)
		course = {
		'summary': class_names[i],
	    'location': class_locations[i],
	    'start': {
	        'dateTime': start_day + 'T' + start_time + ':00.000-05:00',
	    	'timeZone': 'America/Chicago'
	    },
	    'end': {
	    	'dateTime': start_day + 'T' + end_time + ':00.000-05:00',
	        'timeZone': 'America/Chicago'
	    },
	    'recurrence': [
	    	'RRULE:FREQ=WEEKLY;BYDAY=' + days + ';UNTIL=' + end_day + 'T230000Z',
	    ],
		}
		courses.append(course)

	return courses
