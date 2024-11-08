from pathlib import Path

from diagram_as_code import GitLab

folder = Path("diagrams")


def main():
    folder.mkdir(exist_ok=True, parents=True)

    GitLab(folder / "gitlab")


if __name__ == "__main__":
    main()
