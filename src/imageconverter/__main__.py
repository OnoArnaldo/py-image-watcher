from imageconverter.converter import convert, Config, build_arg_parser

config = Config()
config.load_env()

parser = build_arg_parser()
args = parser.parse_args()

if args.config:
    config.load_file(args.config)
else:
    config.load_args(args)

convert(config)
