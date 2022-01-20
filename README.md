PyVjudge
--------
A python client to interact with https://vjudge.net. This project was born to make vjudge's data
(standing, contest data) easily accessible to generate various kinds of thing such as a custom standing. As Vjudge
doesn't provide apis, it would help to build scripts based on this widely used online judge.

## Features

| Feature     | Working | Test    |
|-------------|---------|---------|
| Contest     | Yes     | Passing |
| Problem Set | Yes     | Passing |
| Submissions | Yes     | Passing |
| Standing    | Yes     | Passing |

## Development

Starting development is easy!

Get `pipenv` installed by `pip install --user pipenv`

Now follow the commands:

```commandline
git clone https://github.com/joynahid/pyvjudge.git
cd pyvjudge
pipenv shell
pipenv sync
pip install -e .
```

You need another task to make it ready to use. Add your vjudge credentials to your systems environment variable.

In Ubuntu/Linux:

```commandline
export VJUDGE_USERNAME=yourvjudgeusername
export VJUDGE_PASSWORD=yourvjudgepassword
```

After executing the last command, pyjudge will be accessible to any module under that pipenv shell. So you can import it
as `from pyvjudge import PyVjudge` to play around.

### Testing

For testing, simply run `pytest` :)

## Usage

Using this package is easy! After installing, you can simply write the following piece of code to fetch everything from
about a vjudge contest with python serialized!

```python
from pyvjudge import PyVjudge

pv = PyVjudge()

# Replace with a valid vjudge contest id
pv.get_standing(contest_id=12345)
```

## Upcoming

- Problem Set/ Description scraper
- Code Submission and Watcher
- CLI for easy access
- `pyvjudge` will be available to PyPI for convenient installation.

## Why PyVjudge?

This package was born, because I needed it in a project where I did combine standing from multiple contests of multiple
online judges. Vjudge was included too. I'll switch to this package when it gets the first release.