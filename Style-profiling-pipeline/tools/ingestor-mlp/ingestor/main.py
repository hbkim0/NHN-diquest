import typer
import logging

# import pyfiglet
# print(pyfiglet.Figlet(font="speed", width=120).renderText("AI-Dev Ingestor"))
_LOGO = '''_______________    ________                 ________                          _____
___    |___  _/    ___  __ \_______   __    ____  _/_____________ ______________  /______________
__  /| |__  /________  / / /  _ \_ | / /     __  / __  __ \_  __ `/  _ \_  ___/  __/  __ \_  ___/
_  ___ |_/ /_/_____/  /_/ //  __/_ |/ /     __/ /  _  / / /  /_/ //  __/(__  )/ /_ / /_/ /  /
/_/  |_/___/       /_____/ \___/_____/      /___/  /_/ /_/_\__, / \___//____/ \__/ \____//_/
                                                          /____/
'''

#
app = typer.Typer(name="ingestor", help="Data ingestor for built-in dataset")


def main():
    #
    logging.basicConfig(
        format='%(asctime)s:%(name)s:%(levelname)s:%(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        level=logging.WARNING
    )

    typer.echo(_LOGO)
    app()
