import os
import shutil
import argparse
from playwright.sync_api import sync_playwright
from google import genai
from typing import List, Tuple


# for next time things we need to do 
"""
modularize the code so its not just in main

actually make the tailor function call like gemini or some llm

add logic to handle the either copying starter code to the worktree OR 
writing to the file the tailored version to the file for both resume and cv 

surely light work
"""

STARTER_RESUME = os.path.expanduser(f"~/Desktop/personal/rwt/starter/Aiden-Lee-Resume.tex")
STARTER_COVER_LETTER = os.path.expanduser(f"~/Desktop/personal/rwt/starter/base-cover-letter.tex")


def tailor(link: str) -> str | None:
    # something something tailor stuff
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(link)
        job_desc = page.content()
        browser.close()

    client = genai.Client()

    
    with open(STARTER_RESUME) as f:
        resume_content = f.read()

    response = client.models.generate_content(
        model="gemini-2.5-flash", contents=f"""
            Please tailor the resume that is passed here note the latex template
            and tailor it to this job description that you should
            parse the html for that i am passing to you  and give me back the
            same format of the latex template so i can write it to a file and keep all
            formatting just with tailored bullet points. so to recap, first read the
            resume, second read the job description html and parse the actual job
            description, finally tailor the resume (with the bullets going no longer than
            like 13 words so they fit on one line).

            DO NOT MAKE UP INFORMATION ABOUT MY SKILLSET OR PROJECTS OR ANYTHING ONLY GO OFF THE STUFF I GAVE YOU

            BASE RESUME: 
                {resume_content} 

            JOB DESCRIPTION: 
                {job_desc}
            """)

    return response.text

def create_files(company_name: str, create_cv: bool, resume_content: str | None) -> None:
    base = os.path.expanduser(f"~/Desktop/personal/rwt/{company_name}/")
    resume_path = os.path.join(base, "resume/")
    os.makedirs(resume_path, exist_ok=True)
    resume_name = os.path.join(resume_path, "Aiden-Lee-Resume.tex")

    cover_letter_path = os.path.join(base, "cover-letter/")
    cover_letter_name = os.path.join(cover_letter_path, f"{company_name}-CV.tex")

    if create_cv:
        os.makedirs(cover_letter_path, exist_ok=True)
    
    if not resume_content:
        pairs = [(STARTER_RESUME, resume_name)]
        if create_cv:
            pairs.append((STARTER_COVER_LETTER, cover_letter_name))

        write_base_files(pairs)
    else:
        write_new_files(resume_content, resume_name)


def write_new_files(resume_content: str, resume_name: str) -> None:
    try:
        with open(resume_name, "w") as f:
            f.write(resume_content)
    except:
        print("uh oh")

def write_base_files(pairs: List[Tuple[str, str]]) -> None:
    try:
        for source, dest in pairs:
            shutil.copy(source, dest)
    except FileNotFoundError:
        print("le file was not found lil bro")
    except Exception as e:
        print(f" error {e}")


# just a v1 with hardcoded vals to test
def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("company_name")
    # default to false for now, maybe change if i find myself wanting cvs more than not
    parser.add_argument("-cv", action="store_true")
    parser.add_argument("-tailor", dest="link", help="just pass the link to the job description")

    args = parser.parse_args()

    # entering tailoring pathway
    resume_content = ""
    if args.link:
        resume_content = tailor(args.link)

    create_files(args.company_name, args.cv, resume_content)


if __name__ == "__main__":
    main()
