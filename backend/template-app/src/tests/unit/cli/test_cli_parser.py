from template_app.runtime.transports.cli.parser import build_cli_parser


def test_cli_parser_created() -> None:

    parser = build_cli_parser()

    assert parser is not None


def test_cli_parser_supports_version_flag() -> None:

    parser = build_cli_parser()

    args = parser.parse_args(
        ["--version"],
    )

    assert args.version is True
