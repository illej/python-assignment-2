# python-assignment-2
Refactoring python assignment 1 (Interpreter)

Bad Smells
==========
1. Switch Statement: `controller.display()`
2. Feature Envy: `controller.display()`
3. Large Class: `Controller`
4. Speculative Generality: `View`

 *refactoring process for each individual bad smell identified and a discussion on how well you remove the bad smells
  (e.g., has the bad smells successfully been removed at the end?
  Did you bring new bad smells into the program? 
  How well is your program now in terms of software quality?)*

Smell 1: Switch Statement
-------------------------
Package:  `Interpreter`

File:     `controller.py`

Class:    `Controller`

Method:   `display()`

Lines:    `26 - 33`

Steps:
1. Extract Method:

  desctipions
  
2. Move Method:

  desctipions
  
3. Consolidate Conditional Expression:

  desctipions

Result:

switch is gone

no new smells

class is now more easily extensible, though improvements can still be made (example?)
    
Smell 2: Feature Envy
---------------------
Package:  `Interpreter`

File:     `controller.py`

Class:    `Controller`

Method:   `display()`

Lines:    `17, 18`

Steps:
1. Extract Method:

  desctipions
  
2. Extract Method:

  desctipions
  
3. Move Method:

  desctipions
  
4. Move Method:

  desctipions

Result:

It didn't really clean up controller.display() method, but the Validator/Visualiser classes now have their privacy more intact.

Could clean up further with assertions, but that would be beyond the scope of the smell.

I also now realise there are more glaring flaws in my design, but again, they are outside the scope of this smell.
    
Smell 3: Large Class
--------------------
Package:  `Interpreter`

File:     `controller.py`

Class:    `Controller`

Method:   `serialize()`

Lines:    `76`

Steps:
1. Extract Class:

Result:

Controller is now cleaner and abides more to the Single Responsibility Principle.

The serialization functionality is now encapsulated, making it easier to inspect or clean up in the future.
    
Smell 4: Speculative Generality
-------------------------------
Package:  `Interpreter`

File:     `view.py`, `fileview.py`, `databaseview.py`, `cmdview.py`
          
Class:    `View`, `FileView`, `DatabaseView`, `CmdView`
          
Method:   `get()`, `set()`

Lines:    
```
fileview.py -> line: 44, line: ??

databaseview.py -> line: ??, line: ??
          
cmdview.py -> line: 92, line: ??
```
          
Steps:
1. Collapse Hierarchy:

  1.  xx
  
  2.  xx
  
2. Rename Method:

  1.  xx
  2.  xx
  3.  xx
  4.  xx
3. Rename Class:
  1.  xx
  
  2.  xx
    
Result:

With the inept inheritance hierarchy gone, the overall design is more straight forward.

Renaming the affected methods and class clears up a lot of the previous ambiguity, and better describes the functionality and purpose of each class / method.

*Overall, refactoring these smells has improved my code a decent amount, but the real value has been the discovery of subtler issues
that I might be otherwise unaware of.*
