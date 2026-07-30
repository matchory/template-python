from matchory_template import greeting


def test_greeting_uses_the_given_name() -> None:
    assert greeting("Matchory") == "Hello, Matchory!"
