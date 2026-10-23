from argparse import ArgumentParser, Namespace

from .app import App
from .factory import Projects


def main() -> None:
    parser: ArgumentParser = ArgumentParser()
    parser.add_argument(
        "--project",
        type=lambda x: Projects(int(x)),
        choices=list(Projects),
        default=Projects.FLYWEIGHT,
        help=", ".join([f"{project.name}={project.value}" for project in Projects]),
    )
    args: Namespace = parser.parse_args()

    app: App = App(args.project)
    app.run()


main()
