# Installation
1. Install dependencies
2. Copy `config-sample.py` to `config.py`
3. Open `config.py` and change the required settings

## Dependencies
- discord.py
- pytimeparse
- pytz
- transaction
- APScheduler
- python-dateutil

You can install these via `pip install -r requirements.txt`

# Usage
To start, run `python3 bot.py`.

To stop, hit `CTRL+C`.

# Command info

All info about a command can be found in the docs of the relative function.
All commands have one or more aliases. Check the relative function docs for them.
The prefix of the examples is the standard one. You can change it in `config-sample.py`

### Help command
```
^help [command_name]
```
Give the name of the command for which help is needed. An alias works too.
If no name is given (or the given command is not found), the standard help message (found in `config.py`) gets sent.

### Create giveaway command
```
^giveaway [duration] [winners]w [prize]( >[description])
```
Used to start a giveaway. Insert the prize, the amount of winners and the duration 
of the giveaway. Everything inside the round brackets is optional (description included).

The duration can have different formats:
- **+xy** Examples: `+4h`, `+2h 30m`, `+1d 6h 24m`
- **M/D/Y T** Examples: `06/28/20 6pm`, `12/03/21 7:25 am`

### Close giveaway command
```
^close [id]
```
Used to close a giveaway. Insert the id of the giveaway message to be closed.

### Re-roll giveaway winners command
```
^reroll [id] [winners]
```
Used to re-roll an amount of winners of a giveaway.
Insert the id of the giveaway message of which one or more winners need to be re-rolled and the amount of winners to re-roll.
