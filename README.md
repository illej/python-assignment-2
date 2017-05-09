# python-assignment-2
Refactoring python assignment 1 (Interpreter)

Bad Smells
1. Switch Statement: controller.display()
2. Feature Envy: controller.display()
3. Large Class: Controller
4. Speculative Generality: View

 refactoring process for each individual bad smell identified and a discussion on how well you remove the bad smells
  (e.g., has the bad smells successfully been removed at the end?
  Did you bring new bad smells into the program? 
  How well is your program now in terms of software quality?) 

Smell 1: Switch Statement
  package:  Interpreter
  file:     controller.py
  class:    Controller
  method:   display()
  lines:    26 - 33
  steps:
    1. Extract Method:
    2. Move Method:
    3. Consolidate Conditional Expression:
  result:
    switch is gone, no new smells, class is now more easily extensible, though improvements can still be made (example?)
    
Smell 2: Feature Envy
  package:  Interpreter
  file:     controller.py
  class:    Controller
  method:   display()
  lines:    17, 18
  steps:
    1. Extract Method:
    2. Extract Method:
    3. Move Method:
    4. Move Method:
  result:
    It didn't really clean up controller.display() method, but the Validator/Visualiser classes now have their privacy more intact.
    Could clean up further with assertions, but that would be beyond the scope of the smell.
    I also now realise there are more glaring flaws in my design, but again, they are outside the scope of this smell.
    
Smell 3: Large Class
  package:  Interpreter
  file:     controller.py
  class:    Controller
  method:   serialize()
  lines:    76
  steps:
    1. Extract Class:
  result:
    Controller is now cleaner and abides more to the Single Responsibility Principle.
    The serialization functionality is now encapsulated, making it easier to inspect or clean up in the future.
    
Smell 4: Speculative Generality
  package:  Interpreter
  file:     view.py
            fileview.py
            databaseview.py
            cmdview.py
  class:    View
            FileView
            DatabaseView
            CmdView
  method:   get(), set()
  lines:    fileview.py -> line: 44, line: ??
            databaseview.py -> line: ??, line: ??
            cmdview.py -> line: 92, line: ??
  steps:
    1. Collapse Hierarchy:
      a.
      b.
    2. Rename Method:
      a.
      b.
      c.
      d.
    3. Rename Class:
      a.
      b.
    result:
      With the inept inheritance hierarchy gone, the overall design is more straight forward.
      Renaming the affected methods and class clears up a lot of the previous ambiguity, and better describes the functionality
        and purpose of each class / method.
        
Overall, refactoring these smells has improved my code a decent amount, but the real value has been the discovery of subtler issues
that I might be otherwise unaware of.
