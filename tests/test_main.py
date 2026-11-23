from mailroom import main


def test_main_prints_greeting(capsys):
    main()
    assert "mailroom" in capsys.readouterr().out
