def course_formatter(courses):
    courses_texts = []
    courses_texts.append('List of all courses this sem\n')
    for course in courses:
        courses_texts.append(course)
    return courses_texts