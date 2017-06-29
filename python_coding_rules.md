Python Coding Rules
===================

*Objective rules*: these are mechanically enforceable, hence should be followed absolutely with no argument.

*Subjective rules*: these are all important rules to follow, but their conformance/violation may not be totally objective.

When evolving this document, keep the number of rules under, say, 20.


Objective Rules
---------------

1. Python version: use the second-latest major version of Python 3.
   For example, if the current latest Python release is 3.6.x, then use the latest 3.5.y.

2. Code formatting: pick a code formatter (`yapf` might be a good one) and run it
   either in an automatic mechanism or manually from time to time.
   In the latter case, committed code may not *always* be in good format.
   Understanding that formatter will be run from time to time,
   turn attention away from unpleasant formatting in code reviews.

3. Naming: `module_name`, `package_name`, `ClassName`, `method_name, ExceptionName`,
   `function_name`, `GLOBAL_CONSTANT_NAME`, `global_var_name`, `instance_var_name`,
   `function_parameter_name`, `local_var_name`.

4. Do not use `import *` (not even in test modules).

5. At the top of a module, group imports in this order and separate groups by single blank lines:
   standard library, third-party packages, same team's other packages, same package.


Subjective Rules
----------------

1. Encourage frequent, small refactoring and incremental improvements.
   "It works now!" is not sufficient reason to resist code improvement,
   provided it is agreed that the proposed change is an improvement.

2. Naming: use descriptive names that indicate the role of the object.
   Spend time thinking up good names.

3. Follow the **Principle of Single Reponsibility**:
   one function (or method) should be concerned with a single level of abstraction.

4. In OOP code, consider following the **Law of Demeter**.

5. The third time you repeat a chunk of code is the right time to consider
   extracting it into its own function (or method).

6. Length of a function (or method) that sets off alarm and warrants discussion:
   30-50 code lines, not counting blank lines, comments, and inner functions;
   apply the same rule to inner functions recursively.


Annotations
-----------

1. The *Law of Demeter* states that a module should not have knowledge on
   the inner details of the objects it manipulates.
   One interpretation of it in simple terms is
   "call methods only of objects that are directly visible to you",
   where a "directly visible object" is one that is a member of the same class,
   or a parameter passed in, or a global, or is created locally in the same method.

   For example, if in method `C`, object `A` is directly visible, then you can call
   `A.method()`, but should not call `A.field_B.method()`, because the former
   uses `A`'s API whereas the latter uses `A`'s internal structure (i.e. implementation detail).
   In this example, `field_B` is a member of object `A`.
   If, on the other hand, `A.make_B()` creates and returns an object `B`, then
   `A.make_B().method()` will be fine because this calls a method of the object `B`,
   which is created in the current scope and is directly visible upon creation.
   This law may be relaxed if `field_B` of object `A` is designed and meant to be
   publicly accessed and freely used.

   In essence, this law is against getters and direct attribute access from outside.
   It asks you to design your code (e.g. class) in such a way
   that you do not *need* to access internal objects.
   The law's application in Python does have confusing cases,
   but its spirit of encapsulation and decoupling is absolutely critical.


