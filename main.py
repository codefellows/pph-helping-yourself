import asyncio
import os
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from playwright.async_api import async_playwright

load_dotenv()  # take environment variables from .env.


async def main(course_key=None):
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()

        page_content = await get_page_content(page)

        parsed_content = parse_content(page_content)

        output(parsed_content)

        await browser.close()


async def get_page_content(page):
    await page.goto(os.getenv("URL"))

    return await page.content()


def parse_content(content):

    soup = BeautifulSoup(content, "html.parser")

    courses = soup.select(".course-calender-year-list .calendar-event")

    text = "Code Fellows Courses\n\n"

    for course in courses:
        text += course.h1.text + "\n"
        text += course.h2.text + "\n"
        text += course.header.h2.text + "\n"
        text += "\n"

    return text


def output(content):
    with open("./cf-courses.txt", "w") as f:
        f.write(content)


if __name__ == "__main__":
    asyncio.run(main())
