# Conversor de imagens

## Instalação:

### Instalar Python:

Siga as instruções no site https://www.python.org/downloads/.


## Uso:

### Básico:

```shell
python img_converter.py --inbox "/diretorio/inbox" --outbox "/diretorio/outbox" --extension ".png"
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
python img_converter.py --config "caminho/arquivo/converter.cfg"
```


### Com variáveis de ambiente:

Defina as variáveis com mesmas chaves disponíveis no arquivo `.cfg`.

Commando:
```shell
python img_converter.py
```


## No futuro:

* Implementar o watchdog