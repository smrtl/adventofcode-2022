import os
from importlib import import_module
from pathlib import Path

import click
import requests
from dotenv import load_dotenv


def day_path(day: int) -> Path:
    return Path(__file__).parent.parent.joinpath(f'day{day:02d}')


@click.group()
def main() -> None:
    pass


@main.command()
@click.argument('day', type=int)
def create(day: int) -> None:
    """Scaffold the day folder and fetch the input"""
    load_dotenv()

    click.echo(f'scaffolding day {day} ...')
    day_dir = day_path(day)
    day_dir.mkdir(exist_ok=True)
    init_file = day_dir.joinpath('__init__.py')
    if not init_file.exists():
        init_file.write_text('from pathlib import Path\n\n\n'
                             'def main(input_file: Path) -> None:\n'
                             f'    print(\'day {day}\')\n')

    click.echo('fetching input ...')
    url = f'https://adventofcode.com/2022/day/{day}/input'
    cookies = {'session': os.environ.get('SESSION_COOKIE', '')}
    input_file = day_dir.joinpath('input')
    input_file.unlink(missing_ok=True)

    with requests.get(url, cookies=cookies, stream=True) as r:
        r.raise_for_status()

        with open(input_file, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)

    click.echo('done')


@main.command()
@click.argument('day', type=int)
def run(day: int) -> None:
    """Run the code of a day"""
    mod = import_module(f'aoc2022.day{day:02d}')
    mod.main(day_path(day).joinpath('input'))
