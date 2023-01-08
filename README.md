# Conversor de imagens

## Instalação:

### Instalar Python:

Siga as instruções no site https://www.python.org/downloads/.


### Instalar Image Converter

```shell
python3.11 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install git+https://github.com/OnoArnaldo/py-image-watcher.git
```

**No windows**
```shell
python3.11 -m venv venv
source venv\script\activate.bat
pip install --upgrade pip
pip install git+https://github.com/OnoArnaldo/py-image-watcher.git
```


## Uso:

### Básico:

```shell
python -m imageconverter --inbox "/diretorio/inbox" --outbox "/diretorio/outbox" --extension ".png"
```


### Com arquivo de configuração:

Arquivo: `converter.cfg`
```toml
IMG_CONVERT_TO = ".PNG"
IMG_WATCHDOG = "FALSE"

IMG_INBOX = "/inbox"
IMG_OUTBOX = "/outbox"
```

Commando:
```shell
python -m imageconverter --config "caminho/arquivo/converter.cfg"
```


### Com variáveis de ambiente:

Defina as variáveis com mesmas chaves disponíveis no arquivo `.cfg`.

Commando:
```shell
python -m imageconverter
```


## No futuro:

* Implementar o watchdog