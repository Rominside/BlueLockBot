from config import settings
import os

def test_one():
    bot_name = "BlueLockBot"
    assert bot_name == os.environ.get('BOTNAME')