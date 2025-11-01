# Automated Reports

## Coverage Report
```text
Name                      Stmts   Miss  Cover   Missing
-------------------------------------------------------
UI/__init__.py                0      0   100%
cli/__init__.py               0      0   100%
cli/main.py                 282     16    94%   88, 273-274, 314-324, 362, 384
core/__init__.py              0      0   100%
core/backgammon_game.py     245     34    86%   185, 197, 215-231, 250, 252, 393-407, 487-489, 494
core/board.py               231     15    94%   194-198, 200-204, 224-226, 234-239, 268, 294-299, 382, 384, 391
core/checker.py               9      0   100%
core/dice.py                 11      0   100%
core/excepciones.py          10      0   100%
core/player.py               23      0   100%
core/validaciones.py         15      0   100%
-------------------------------------------------------
TOTAL                       826     65    92%

```

## Pylint Report
```text
************* Module core.backgammon_game
core/backgammon_game.py:183:19: E1136: Value 'resultado' is unsubscriptable (unsubscriptable-object)
core/backgammon_game.py:188:26: E1136: Value 'resultado' is unsubscriptable (unsubscriptable-object)
core/backgammon_game.py:192:46: E1136: Value 'resultado' is unsubscriptable (unsubscriptable-object)

-----------------------------------
Your code has been rated at 9.92/10


```
