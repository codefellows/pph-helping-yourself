import asyncio
import os
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import fire
from playwright.async_api import async_playwright

load_dotenv()  # take environment variables from .env.


async def main(course_key=None):
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()

        courses = {
            "java": "Code 401: Java",
            "javascript": "Code 401: JavaScript",
            ".net": "Code 401: ASP.NET",
            "python": "Code 401: Python",
            "cybersecurity": "Ops 401: Cybersecurity",
        }

        page_content = await get_page_content(page, course_key, courses)

        parsed_content = parse_content(page_content, courses.get(course_key))

        output(parsed_content)

        await browser.close()


async def get_page_content(page, course_key, courses):
    await page.goto(os.getenv("URL"))

    await page.click("//label[text()='400: Advanced']")

    if course_key and course_key not in courses:
        print(f"Course {course_key} not found.")
        print(f"Enter one of {[key for key in courses.keys()]}")
        return

    # all course families are selected by default
    # so let's de-select all but desired one

    for course in courses:
        if course_key and course != course_key:
            await page.click(f"//label[text()='{courses[course]}']")

    return await page.content()


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


def output(content):
    with open("./courses.txt", "w") as f:
        f.write(content)


def run(course_key=None):
    return asyncio.run(main(course_key))


if __name__ == "__main__":
    fire.Fire(run)
