import os
import shutil
import argparse
from playwright.sync_api import sync_playwright


# for next time things we need to do 
"""
modularize the code so its not just in main

actually make the tailor function call like gemini or some llm

add logic to handle the either copying starter code to the worktree OR 
writing to the file the tailored version to the file for both resume and cv 

sure light work
"""


def tailor(job_desc: str, tailoring: str) -> None:
    # something something tailor stuff
    pass

    if args.tailor[1]:
        match args.tailor[1]:
            # something something make a llm request with job data 
            case "resume":
                print("tailoring resume...")
            case "cv":
                print("tailoring cv...")
            case "all":
                print("tailoring both...")
            case _:
                print("unknown var passed for what to tailor")

# just a v1 with hardcoded vals to test
def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("company_name")
    # default to false for now, maybe change if i find myself wanting cvs more than not
    parser.add_argument("-cv", action="store_true")
    parser.add_argument("-tailor", nargs=2, metavar=("link", "ai"), help="first pass the link, then pass what you want tailored from ['resume', 'cv', 'all']")

    args = parser.parse_args()


    job_desc = ""
    if args.tailor[0]:
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            page.goto(args.tailor[0])
            job_desc = page.content()
            browser.close()



    base = os.path.expanduser(f"~/Desktop/personal/rwt/{args.company_name}/")

    resume_path = os.path.join(base, "resume/")
    os.makedirs(resume_path, exist_ok=True)
    resume_name = os.path.join(resume_path, "Aiden-Lee-Resume.tex")
    starter_resume = os.path.expanduser(f"~/Desktop/personal/rwt/starter/Aiden-Lee-Resume.tex")

    pairs = [(starter_resume, resume_name)] 
    if args.cv:
        cover_letter_path = os.path.join(base, "cover-letter/")
        os.makedirs(cover_letter_path, exist_ok=True)
        cover_letter_name = os.path.join(cover_letter_path, f"{args.company_name}-CV.tex")
        starter_cover_letter = os.path.expanduser(f"~/Desktop/personal/rwt/starter/base-cover-letter.tex")

        pairs.append((starter_cover_letter, cover_letter_name))

    try:
        for source, dest in pairs:
            shutil.copy(source, dest)
    except FileNotFoundError:
        print("le file was not found lil bro")
    except Exception as e:
        print(f" error {e}")


if __name__ == "__main__":
    main()
