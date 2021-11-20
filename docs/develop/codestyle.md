## Python Style Guide

In project to write code in python [PEP 8](https://www.python.org/dev/peps/pep-0008/) is used, 
so we strongly encourage to read it.

Basic requirements for writing code:

* Use 4 spaces per indentation level;
* Spaces are the preferred indentation method;
* Avoid trailing whitespace anywhere;
* Limit all lines to a maximum of 79 characters;
* Surround top-level function and class definitions with two blank lines;
* Imports should usually be on separate lines;
* Trailing commas are usually optional, except they are mandatory when making a tuple of one element;
* Conventions for writing good documentation strings (a.k.a. "docstrings") are immortalized in PEP 257;
* Comments that contradict the code are worse than no comments. Comments should be complete sentences;
* Don't use spaces around the = sign when used to indicate a keyword argument;
* If operators with different priorities are used, consider adding whitespace around the operators with 
the lowest priority(ies);
* Function annotations should use the normal rules for colons and always have spaces around 
the -> arrow if present and etc.

## Formatting example

```python
# Module name in snake case
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State

# Space between third party and custom libraries
from bot.loggers import LogInstaller
from bot.modules.handlers_chain import HandlersChain
from bot.modules.handlers_registrar import HandlersRegistrar as Registrar


# Class name in camel case
class GreetingsStates(StatesGroup):
    # Vars in snake case
    hello = State()
    bye = State()

# Space before class definition
class GreetingsHandlersChain(HandlersChain):
    _logger = LogInstaller.get_default_logger(__name__, LogInstaller.DEBUG)

    @staticmethod
    @Registrar.message_handler(text_contains="привет")
    async def bye_handler(message: types.Message):
        GreetingsHandlersChain._logger.debug(f"Start greetings conversation state")
        await GreetingsStates.hello.set()

        await Registrar.bot.send_message(message.from_user.id, "Привет.")

    # Space between methods in class
    @staticmethod
    @Registrar.message_handler(text_contains="пока")
    async def bye_handler(message: types.Message, state: FSMContext):
        GreetingsHandlersChain._logger.debug(f"Finish greetings conversation state")
        await GreetingsStates.bye.set()

        await state.finish()
        await Registrar.bot.send_message(message.from_user.id, "Пока.")

# Space after double dash. And full sentences in comments.
```

**To check bot sources code style on Linux:**

```shell
./check_code_style.sh
```