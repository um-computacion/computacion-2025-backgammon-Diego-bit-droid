# Automated Reports
## Coverage Report
```text
Name                            Stmts   Miss  Cover   Missing
-------------------------------------------------------------
core/__init__.py                    0      0   100%
core/clases/__init__.py             0      0   100%
core/clases/backgammonGame.py     102     32    69%   17-18, 21-25, 45, 49-51, 60, 81-84, 116-121, 125, 129, 133-134, 138-139, 143-144, 148-149
core/clases/board.py              133     20    85%   153, 187, 193-215
core/clases/checker.py              9      0   100%
core/clases/dice.py                 9      0   100%
core/clases/player.py              20      0   100%
-------------------------------------------------------------
TOTAL                             273     52    81%

```
## Pylint Report
```text
************* Module core.clases.checker
core/clases/checker.py:30:0: C0304: Final newline missing (missing-final-newline)
core/clases/checker.py:1:0: C0114: Missing module docstring (missing-module-docstring)
core/clases/checker.py:1:0: C0115: Missing class docstring (missing-class-docstring)
************* Module core.clases.board
core/clases/board.py:51:0: C0301: Line too long (103/100) (line-too-long)
core/clases/board.py:58:0: C0301: Line too long (129/100) (line-too-long)
core/clases/board.py:64:0: C0301: Line too long (133/100) (line-too-long)
core/clases/board.py:68:0: C0301: Line too long (109/100) (line-too-long)
core/clases/board.py:97:0: C0301: Line too long (107/100) (line-too-long)
core/clases/board.py:114:0: C0301: Line too long (102/100) (line-too-long)
core/clases/board.py:117:0: C0301: Line too long (105/100) (line-too-long)
core/clases/board.py:244:0: C0304: Final newline missing (missing-final-newline)
core/clases/board.py:1:0: C0114: Missing module docstring (missing-module-docstring)
core/clases/board.py:3:0: C0115: Missing class docstring (missing-class-docstring)
core/clases/board.py:144:40: W0613: Unused argument 'hasta' (unused-argument)
core/clases/board.py:192:4: C0116: Missing function or method docstring (missing-function-docstring)
core/clases/board.py:192:34: C0103: Argument name "Player" doesn't conform to snake_case naming style (invalid-name)
core/clases/board.py:203:19: E1101: Instance of 'Board' has no 'es_destino_valido' member (no-member)
core/clases/board.py:212:43: E1101: Instance of 'Board' has no 'es_destino_valido' member (no-member)
************* Module core.clases.player
core/clases/player.py:31:0: C0301: Line too long (103/100) (line-too-long)
core/clases/player.py:72:0: C0304: Final newline missing (missing-final-newline)
core/clases/player.py:1:0: C0114: Missing module docstring (missing-module-docstring)
core/clases/player.py:1:0: C0115: Missing class docstring (missing-class-docstring)
core/clases/player.py:33:28: C0104: Disallowed name "bar" (disallowed-name)
core/clases/player.py:51:41: C0104: Disallowed name "bar" (disallowed-name)
************* Module core.clases.dice
core/clases/dice.py:1:13: C0303: Trailing whitespace (trailing-whitespace)
core/clases/dice.py:7:0: C0303: Trailing whitespace (trailing-whitespace)
core/clases/dice.py:17:0: C0304: Final newline missing (missing-final-newline)
core/clases/dice.py:1:0: C0114: Missing module docstring (missing-module-docstring)
core/clases/dice.py:3:0: C0115: Missing class docstring (missing-class-docstring)
core/clases/dice.py:3:0: R0903: Too few public methods (1/2) (too-few-public-methods)
************* Module core.clases.backgammonGame
core/clases/backgammonGame.py:11:27: C0303: Trailing whitespace (trailing-whitespace)
core/clases/backgammonGame.py:11:0: W0311: Bad indentation. Found 9 spaces, expected 8 (bad-indentation)
core/clases/backgammonGame.py:13:0: W0311: Bad indentation. Found 9 spaces, expected 8 (bad-indentation)
core/clases/backgammonGame.py:16:0: C0303: Trailing whitespace (trailing-whitespace)
core/clases/backgammonGame.py:19:0: C0303: Trailing whitespace (trailing-whitespace)
core/clases/backgammonGame.py:66:0: C0301: Line too long (103/100) (line-too-long)
core/clases/backgammonGame.py:73:0: C0301: Line too long (139/100) (line-too-long)
core/clases/backgammonGame.py:83:0: C0301: Line too long (116/100) (line-too-long)
core/clases/backgammonGame.py:94:0: C0301: Line too long (102/100) (line-too-long)
core/clases/backgammonGame.py:99:0: C0301: Line too long (123/100) (line-too-long)
core/clases/backgammonGame.py:102:0: C0301: Line too long (117/100) (line-too-long)
core/clases/backgammonGame.py:158:0: C0304: Final newline missing (missing-final-newline)
core/clases/backgammonGame.py:1:0: C0114: Missing module docstring (missing-module-docstring)
core/clases/backgammonGame.py:1:0: C0103: Module name "backgammonGame" doesn't conform to snake_case naming style (invalid-name)
core/clases/backgammonGame.py:2:0: C0115: Missing class docstring (missing-class-docstring)
************* Module core.test.test_BackgammonGame
core/test/test_BackgammonGame.py:29:8: C0103: Attribute name "_BackgammonGame__turno__" doesn't conform to snake_case naming style (invalid-name)
core/clases/backgammonGame.py:10:4: C0116: Missing function or method docstring (missing-function-docstring)
core/clases/backgammonGame.py:11:9: R1705: Unnecessary "else" after "return", remove the "else" and de-indent the code inside it (no-else-return)
core/clases/backgammonGame.py:15:4: C0116: Missing function or method docstring (missing-function-docstring)
core/clases/backgammonGame.py:20:4: C0116: Missing function or method docstring (missing-function-docstring)
core/clases/backgammonGame.py:21:8: R1705: Unnecessary "elif" after "return", remove the leading "el" from "elif" (no-else-return)
core/clases/backgammonGame.py:27:4: C0116: Missing function or method docstring (missing-function-docstring)
core/clases/backgammonGame.py:36:12: R1705: Unnecessary "elif" after "return", remove the leading "el" from "elif" (no-else-return)
core/clases/backgammonGame.py:47:4: C0116: Missing function or method docstring (missing-function-docstring)
core/clases/backgammonGame.py:53:4: C0116: Missing function or method docstring (missing-function-docstring)
core/clases/backgammonGame.py:55:8: R1705: Unnecessary "elif" after "return", remove the leading "el" from "elif" (no-else-return)
core/clases/backgammonGame.py:62:4: C0116: Missing function or method docstring (missing-function-docstring)
core/clases/backgammonGame.py:69:4: C0116: Missing function or method docstring (missing-function-docstring)
core/clases/backgammonGame.py:75:4: C0116: Missing function or method docstring (missing-function-docstring)
core/clases/backgammonGame.py:88:28: W1309: Using an f-string that does not have any interpolated variables (f-string-without-interpolation)
core/clases/backgammonGame.py:99:28: W1309: Using an f-string that does not have any interpolated variables (f-string-without-interpolation)
core/clases/backgammonGame.py:75:4: R1710: Either all return statements in a function should return an expression, or none of them should. (inconsistent-return-statements)
core/clases/backgammonGame.py:92:12: W0612: Unused variable 'desde' (unused-variable)
core/clases/backgammonGame.py:114:4: C0116: Missing function or method docstring (missing-function-docstring)
core/clases/backgammonGame.py:123:4: C0116: Missing function or method docstring (missing-function-docstring)
core/clases/backgammonGame.py:127:4: C0116: Missing function or method docstring (missing-function-docstring)
core/clases/backgammonGame.py:127:4: E0102: method already defined line 20 (function-redefined)
core/clases/backgammonGame.py:129:15: E1101: Instance of 'BackgammonGame' has no '__jugadores__' member (no-member)
core/clases/backgammonGame.py:131:4: C0116: Missing function or method docstring (missing-function-docstring)
core/clases/backgammonGame.py:136:4: C0116: Missing function or method docstring (missing-function-docstring)
core/clases/backgammonGame.py:138:8: C0104: Disallowed name "bar" (disallowed-name)
core/clases/backgammonGame.py:141:4: C0116: Missing function or method docstring (missing-function-docstring)
core/clases/backgammonGame.py:146:4: C0116: Missing function or method docstring (missing-function-docstring)
************* Module core.test.test_checker
core/test/test_checker.py:25:0: C0304: Final newline missing (missing-final-newline)
core/test/test_checker.py:1:0: C0114: Missing module docstring (missing-module-docstring)
core/test/test_checker.py:4:0: C0115: Missing class docstring (missing-class-docstring)
core/test/test_checker.py:6:4: C0116: Missing function or method docstring (missing-function-docstring)
core/test/test_checker.py:12:4: C0116: Missing function or method docstring (missing-function-docstring)
core/test/test_checker.py:18:4: C0116: Missing function or method docstring (missing-function-docstring)
core/test/test_BackgammonGame.py:43:0: C0303: Trailing whitespace (trailing-whitespace)
core/test/test_BackgammonGame.py:1:0: C0114: Missing module docstring (missing-module-docstring)
core/test/test_BackgammonGame.py:1:0: C0103: Module name "test_BackgammonGame" doesn't conform to snake_case naming style (invalid-name)
core/test/test_BackgammonGame.py:8:0: C0115: Missing class docstring (missing-class-docstring)
core/test/test_BackgammonGame.py:16:4: C0116: Missing function or method docstring (missing-function-docstring)
core/test/test_BackgammonGame.py:20:4: C0116: Missing function or method docstring (missing-function-docstring)
core/test/test_BackgammonGame.py:24:4: C0116: Missing function or method docstring (missing-function-docstring)
core/test/test_BackgammonGame.py:28:4: C0116: Missing function or method docstring (missing-function-docstring)
core/test/test_BackgammonGame.py:29:8: W0212: Access to a protected member _BackgammonGame__turno__ of a client class (protected-access)
core/test/test_BackgammonGame.py:36:4: C0116: Missing function or method docstring (missing-function-docstring)
core/test/test_BackgammonGame.py:37:8: W0212: Access to a protected member _BackgammonGame__turno__ of a client class (protected-access)
core/test/test_BackgammonGame.py:5:0: W0611: Unused Checker imported from core.clases.checker (unused-import)
************* Module core.test.test_Board
core/test/test_Board.py:80:0: C0304: Final newline missing (missing-final-newline)
core/test/test_Board.py:1:0: C0114: Missing module docstring (missing-module-docstring)
core/test/test_Board.py:1:0: C0103: Module name "test_Board" doesn't conform to snake_case naming style (invalid-name)
core/test/test_Board.py:6:0: C0115: Missing class docstring (missing-class-docstring)
core/test/test_Board.py:12:4: C0116: Missing function or method docstring (missing-function-docstring)
core/test/test_Board.py:23:4: C0116: Missing function or method docstring (missing-function-docstring)
core/test/test_Board.py:26:15: W0718: Catching too general exception Exception (broad-exception-caught)
core/test/test_Board.py:29:4: C0116: Missing function or method docstring (missing-function-docstring)
core/test/test_Board.py:37:4: C0116: Missing function or method docstring (missing-function-docstring)
core/test/test_Board.py:47:4: C0116: Missing function or method docstring (missing-function-docstring)
core/test/test_Board.py:55:4: C0116: Missing function or method docstring (missing-function-docstring)
core/test/test_Board.py:63:4: C0116: Missing function or method docstring (missing-function-docstring)
core/test/test_Board.py:71:4: C0116: Missing function or method docstring (missing-function-docstring)
************* Module core.test.test_Dice
core/test/test_Dice.py:2:33: C0303: Trailing whitespace (trailing-whitespace)
core/test/test_Dice.py:8:28: C0303: Trailing whitespace (trailing-whitespace)
core/test/test_Dice.py:11:0: C0304: Final newline missing (missing-final-newline)
core/test/test_Dice.py:1:0: C0114: Missing module docstring (missing-module-docstring)
core/test/test_Dice.py:1:0: C0103: Module name "test_Dice" doesn't conform to snake_case naming style (invalid-name)
core/test/test_Dice.py:4:0: C0115: Missing class docstring (missing-class-docstring)
core/test/test_Dice.py:6:4: C0116: Missing function or method docstring (missing-function-docstring)
************* Module core.test.test_Player
core/test/test_Player.py:60:0: C0304: Final newline missing (missing-final-newline)
core/test/test_Player.py:1:0: C0114: Missing module docstring (missing-module-docstring)
core/test/test_Player.py:1:0: C0103: Module name "test_Player" doesn't conform to snake_case naming style (invalid-name)
core/test/test_Player.py:5:0: C0115: Missing class docstring (missing-class-docstring)
core/test/test_Player.py:18:8: C0104: Disallowed name "bar" (disallowed-name)
core/test/test_Player.py:21:4: C0116: Missing function or method docstring (missing-function-docstring)
core/test/test_Player.py:25:4: C0116: Missing function or method docstring (missing-function-docstring)
core/test/test_Player.py:29:4: C0116: Missing function or method docstring (missing-function-docstring)
core/test/test_Player.py:33:4: C0116: Missing function or method docstring (missing-function-docstring)
core/test/test_Player.py:37:4: C0116: Missing function or method docstring (missing-function-docstring)
core/test/test_Player.py:41:4: C0116: Missing function or method docstring (missing-function-docstring)
core/test/test_Player.py:3:0: C0411: standard import "unittest" should be placed before first party imports "core.clases.player.Player", "core.clases.checker.Checker"  (wrong-import-order)

-----------------------------------
Your code has been rated at 6.95/10


```
