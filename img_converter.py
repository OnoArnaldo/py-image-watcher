import typing as _
import tomllib
from argparse import Namespace, ArgumentParser
from dataclasses import dataclass
from os import environ
from pathlib import Path
from shutil import move

from PIL import Image
from pillow_heif import register_heif_opener

register_heif_opener()


@dataclass
class Config:
    convert_to: str = '.png'
    watchdog: bool = False
    dry_run: bool = False
    inbox: Path = None
    outbox: Path = None

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

    def assert_config(self) -> _.NoReturn:
        if self.inbox is None or not self.inbox.exists():
            raise Exception(f"Valor '{self.inbox!s}' em 'inbox' não é válido.")

        if self.outbox is None or not self.outbox.exists():
            raise Exception(f"Valor '{self.outbox!s}' em 'outbox' não é válido.")

        if self.inbox == self.outbox:
            raise Exception(f"'inbox' e 'outbox' devem ter valores diferentes.")


def build_arg_parser() -> ArgumentParser:
    parser = ArgumentParser()
    parser.add_argument('-cfg', '--config', help='Caminho para o arquivo de configuração.', type=str)
    parser.add_argument('-i', '--inbox', help='Diretório de entrada de arquivos.', type=str)
    parser.add_argument('-o', '--outbox', help='Diretório de saída de arquivos.', type=str)
    parser.add_argument('-e', '--extension', help='Extensão para o arquivo final', type=str)
    parser.add_argument('-w', '--watchdog', help='Hábilitar watchdog.', action='store_true')
    parser.add_argument('--dry-run', help='Apenas gera as mensagens, sem converter nenhum arquivo', action='store_true')

    return parser


def build_file_name(fname: Path, suffix: str = None) -> Path:
    result = Path(fname).with_suffix(suffix) if suffix is not None else Path(fname)

    i = 1
    name = result.stem
    while result.exists():
        result = result.with_stem(f'{name} ({i})')
        i += 1

    return result


def convert(config):
    print(f'Inbox:  {config.inbox.absolute()!s}')
    print(f'Outbox: {config.outbox.absolute()!s}')
    if config.dry_run:
        print('Dry Run')

    move_original_to = config.outbox.joinpath('_original')
    save_to = config.outbox

    for fname in config.inbox.glob('**/*.*'):
        print(f'  Arquivo: {fname.relative_to(config.inbox)!s}')

        relative_name = fname.relative_to(config.inbox)
        new_name = build_file_name(save_to.joinpath(relative_name), suffix=config.convert_to)
        orig_name = build_file_name(move_original_to.joinpath(relative_name))

        if not config.dry_run:
            if not (new_dir := new_name.parent).exists():
                new_dir.mkdir(parents=True, exist_ok=True)

            if not (new_dir := orig_name.parent).exists():
                new_dir.mkdir(parents=True, exist_ok=True)

            try:
                with Image.open(fname) as img:
                    img.save(new_name)
                    move(fname, orig_name)
                    print(f'         > {new_name.relative_to(config.outbox)!s}')

            except Exception as ex:
                print(f'         > [FAILED] {ex}')

        else:
            print(f'         > {new_name.relative_to(config.outbox)!s}')


if __name__ == '__main__':
    parser = build_arg_parser()
    args = parser.parse_args()

    try:
        config = Config()
        config.load_env()

        if args.config:
            config.load_file(args.config)
        else:
            config.load_args(args)

        config.assert_config()

        convert(config)

    except Exception as ex:
        print(f'[ERROR] {ex}')
        print("Use --help para ajuda.")
