from config import settings

def test_one():
    bot_name = "BlueLockBot"
    assert bot_name == settings["bot"]