from typing import Callable, List

# From Jonathan Feinberg's answer on Stackoverflow
# https://stackoverflow.com/a/1701229
def index_of_first(l: List, predicate: Callable):
  for i, v in enumerate(l):
      if predicate(v):
          return i

  return None

def index_of_first_not(l: List, predicate:Callable):
  for i, v in enumerate(l):
      if not predicate(v):
          return i

  return None

def reversed_index_of_first_not(l: List, predicate: Callable) -> int:
  return (len(l)-1) - index_of_first_not(reversed(l), predicate)

def reversed_index_of_first(l: List, predicate: Callable) -> int:
  return (len(l)-1) - index_of_first(reversed(l), predicate)
