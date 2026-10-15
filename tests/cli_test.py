import json
import subprocess
import sys

import pytest

from jokerai.cli import main


def test_cli_seeded_games_and_json_output(capsys):
    args = ["--games", "2", "--seed", "42"]
    main(args)
    first = capsys.readouterr().out
    main(args)
    assert capsys.readouterr().out == first
    result = json.loads(first)
    assert len(result["games"]) == 2
    assert all(game["steps"] == 144 for game in result["games"])
    assert all(len(game["scores"]) == 4 for game in result["games"])


def test_module_entry_point():
    result = subprocess.run(
        [sys.executable, "-m", "jokerai", "--games", "1"],
        capture_output=True,
        text=True,
        check=True,
    )
    assert len(json.loads(result.stdout)["games"]) == 1


@pytest.mark.parametrize("args", [["--games", "0"], ["--seed", "-1"]])
def test_cli_rejects_bad_parameters(args):
    with pytest.raises(SystemExit) as error:
        main(args)
    assert error.value.code == 2
