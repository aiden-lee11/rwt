import os
import shutil
import argparse
import requests
from bs4 import BeautifulSoup

# just a v1 with hardcoded vals to test
def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("company_name")
    # default to false for now, maybe change if i find myself wanting cvs more than not
    parser.add_argument("-cv", action="store_true")
    parser.add_argument("-l", dest="link", help="link to the site to pull the job description from")
    parser.add_argument("-ai", choices=['resume', 'cv', 'all'], help="have ai tailor your resume")

    args = parser.parse_args()

    job_desc = ""
    if args.link:
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/118.0 Safari/537.36"
            ),
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9",
        }
        print(f"Pulling job description from: {args.link}")
        r = requests.get(args.link, headers=headers)

        if r.status_code == 200:
            soup = BeautifulSoup(r.text, "html.parser")
            job_desc = soup.get_text(separator="\n", strip=True)
            print(job_desc)


    if args.ai:
        match args.ai:
            case "resume":
                print("tailoring resume...")
            case "cv":
                print("tailoring cv...")
            case "all":
                print("tailoring both...")

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
