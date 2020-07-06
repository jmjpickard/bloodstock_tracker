# Carnall Farrar Coding Guidelines

- Follow [PEP8](https://www.python.org/dev/peps/pep-0008/)
- Use type hinting and docstrings as much as possible
- `TODO` tags are used for hacks and issues

## Example 

```python
"""This is the example module.
This module loves birthdays
"""
__version__ = '0.1'
__author__ = 'Bilbo Baggins'
RANDOM_CONSTANT = "mu"
import datetime
class BirthdayMessager(object):
    """ This class holds birthdays and messages
    appropriately"""
    __slots__ = ['_dob', '_name']
    def __init__(self, date: datetime.datetime, name: str):
        self._dob = date
        self._name = name
    @property
    def dob(self) -> datetime.datetime:
        """provides access to attribute date"""
        return self._dob
    @property
    def name(self) -> str:
        """provides access to attribute name"""
        return self._name
    def birthdaychecker(self) -> bool:
        """This function checks to see if today is the birthday"""
        today = datetime.datetime.today()
        ismonth : bool = self.dob.month == today.month 
        isday : bool = self.dob.day == today.day
        return isday and ismonth
    def birthdaymessager(self) -> str:
        """This function prints a birthday message""
        if self.birthdaychecker():
            print("Happy birthday {}!".format(self.name))
        else:
            print("Sorry {}. Today is not your birthday".format(self.name))
if __name__ == "__main__":
    john_name = "John"
    john_dob = datetime.datetime.today() - datetime.timedelta(10)
    dave_name = "Dave"
    dave_dob = datetime.datetime.today()
    john = BirthdayMessager(john_dob,john_name)
    dave = BirthdayMessager(dave_dob,dave_name)
    john.birthdaymessager()
    dave.birthdaymessager()
```

## Zen

When in doubt follow the zen of python:

```
[Yesterday 15:19] Will Browne
    
 Beautiful is better than ugly.
    Explicit is better than implicit.
    Simple is better than complex.
    Complex is better than complicated.
    Flat is better than nested.
    Sparse is better than dense.
    Readability counts.
    Special cases aren't special enough to break the rules.
    Although practicality beats purity.
    Errors should never pass silently.
    Unless explicitly silenced.
    In the face of ambiguity, refuse the temptation to guess.
    There should be one-- and preferably only one --obvious way to do it.
    Although that way may not be obvious at first unless you're Dutch.
    Now is better than never.
    Although never is often better than right now.
    If the implementation is hard to explain, it's a bad idea.
    If the implementation is easy to explain, it may be a good idea.
    Namespaces are one honking great idea -- let's do more of those!
    --Tim Peters
```

## Style tool

In order to check the style of your code use the following scripts:

```
./run-checks.sh <dir>
```

If this script won't run it is likely that the script will need to be made executable:

```
chmod +x run-checker.sh 
```