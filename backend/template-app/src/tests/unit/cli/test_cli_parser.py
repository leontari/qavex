from template_app.cli import build_parser


def test_cli_parser_created() -> None:
    parser = build_parser()

    assert parser is not None
