import sys
import os
import shutil

# just a v1 with hardcoded vals to test
def main():
    if len(sys.argv) < 2:
        print("needed a name at least as arg -- ex rwt openai")
        return

    print(sys.argv[1])

    company_name = sys.argv[1]

    base = os.path.expanduser(f"~/Desktop/personal/rwt/{company_name}/")

    resume_path = os.path.join(base, "resume/")
    cover_letter_path = os.path.join(base, "cover-letter/")

    os.makedirs(resume_path, exist_ok=True)
    os.makedirs(cover_letter_path, exist_ok=True)

    resume_name = os.path.join(resume_path, "Aiden-Lee-Resume.tex")
    cover_letter_name = os.path.join(cover_letter_path, f"{company_name}-CV.tex")

    starter_resume = os.path.expanduser(f"~/Desktop/personal/rwt/starter/Aiden-Lee-Resume.tex")
    starter_cover_letter = os.path.expanduser(f"~/Desktop/personal/rwt/starter/base-cover-letter.tex")

    pairs = [(starter_resume, resume_name), (starter_cover_letter, cover_letter_name)]

    try:
        for source, dest in pairs:
            print(source, dest)
            shutil.copy(source, dest)
            print(f"File '{source}' copied to '{dest}' successfully.")
    except FileNotFoundError:
        print("le file was not found lil bro")
    except Exception as e:
        print(f" error {e}")


if __name__ == "__main__":
    main()
