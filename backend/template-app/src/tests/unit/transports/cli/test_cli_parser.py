from template_app.transports.cli.parser import build_cli_parser


def test_cli_parser_builds() -> None:
    parser = build_cli_parser()

    args = parser.parse_args([])

    assert args is not None
