from bs4 import BeautifulSoup


def parse_content(content, selected_course=None):

    selected_course = selected_course or "Code Fellows 401"
    soup = BeautifulSoup(content, "html.parser")

    courses = soup.select(".course-calender-year-list .calendar-event")

    text = f"{selected_course} Courses\n\n"

    for course in courses:
        text += course.h1.text + "\n"
        text += course.h2.text + "\n"
        text += course.header.h2.text + "\n"
        text += "\n"

    return text
