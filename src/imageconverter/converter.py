import typing as _
import tomllib
from argparse import Namespace, ArgumentParser
from dataclasses import dataclass, field
from os import environ
from pathlib import Path

from PIL import Image


@dataclass
class Config:
    convert_to: str = '.png'
    watchdog: bool = False
    dry_run: bool = False
    inbox: Path = field(default_factory=Path)
    outbox: Path = field(default_factory=Path)

    def load_object(self, obj: _.Any) -> _.NoReturn:
        if (val := obj.get('IMG_CONVERT_TO')) is not None:
            self.convert_to = val

        if (val := obj.get('IMG_WATCHDOG')) is not None:
            self.watchdog = bool(val)

        if (val := obj.get('IMG_INBOX')) is not None:
            self.inbox = Path(val)

        if (val := obj.get('IMG_OUTBOX')) is not None:
            self.outbox = Path(val)

        if (val := obj.get('IMG_DRYRUN')) is not None:
            self.dry_run = bool(val)

    def load_env(self) -> _.NoReturn:
        self.load_object(environ)

    def load_file(self, file_name: str | Path) -> _.NoReturn:
        with Path(file_name).open('rb') as f:
            toml = tomllib.load(f)

        self.load_object(toml)

    def load_args(self, args: Namespace) -> _.NoReturn:
        if args.extension is not None:
            self.convert_to = args.extension
        if args.outbox is not None:
            self.outbox = Path(args.outbox)
        if args.inbox is not None:
            self.inbox = Path(args.inbox)
        if args.watchdog is not None:
            self.watchdog = args.watchdog
        if args.dry_run is not None:
            self.dry_run = args.dry_run


def build_arg_parser() -> ArgumentParser:
    parser = ArgumentParser()
    parser.add_argument('-cfg', '--config', help='Caminho para o arquivo de configuração.', type=str)
    parser.add_argument('-i', '--inbox', help='Diretório de entrada de arquivos.', type=str)
    parser.add_argument('-o', '--outbox', help='Diretório de saída de arquivos.', type=str)
    parser.add_argument('-w', '--watchdog', help='Hábilitar watchdog.', type=bool)
    parser.add_argument('-e', '--extension', help='Extensão para o arquivo final', type=str)
    parser.add_argument('--dry-run', help='Apenas gera as mensagens, sem converter nenhum arquivo', type=bool)

    return parser


def convert(config):
    print(f'Inbox:  {config.inbox.absolute()!s}')
    print(f'Outbox: {config.outbox.absolute()!s}')

    for fname in config.inbox.glob('**/*.*'):
        print(f'  Arquivo: {fname.relative_to(config.inbox)!s}')

        relative_name = fname.relative_to(config.inbox)
        new_name = config.outbox.joinpath(relative_name).with_suffix(config.convert_to)

        if not (new_dir := new_name.parent).exists():
            new_dir.mkdir(parents=True, exist_ok=True)

        if not config.dry_run:
            with Image.open(fname) as img:
                img.save(new_name)

        print(f'         > {new_name.relative_to(config.outbox)!s}')
