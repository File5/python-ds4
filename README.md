# python-ds4
Python script to emulate mouse and keyboard with DualShock 4 gamepad

## Idea

The project is "Proof of Concept" of a new input method only with the help of DualShock 4 gamepad.

Goals:

- both mouse and keyboard input with 1 gamepad
- easy to learn input method
- touch typing (blind typing)
- type faster than the default input method in the PlayStation interface

## Concept

The script prints key mapping so it's easy to understand the principle.

```
             ,---,                                           ,---,
             |SCR|                                           |SCR|
             |OLL|                                           |OLL|
             '---'                                           '---'
           ,-----,                                           ,-----,
           | LMB |                                           | RMB |
        ,--'-----'--------,-------------------------,--------'-----'--,
       /    ,---,     ,--,|                         |,--,     ,---,    \
      /     |   |     |  ||      [  Mouse   ]       ||  |    (Ctrl )    \
     / ,---. \ / .---,'--'|        Keyboard         |'--',---,'---',---, \
    |  |    >   <    |    |                         |   ( Cmd )   ( Opt ) |
    |  '---` / \ `---'    '-------------------------'    '---',---,'---'  |
    |       |   |       .-"""-.      ,---,      .-"""-.      (     )      |
    |       '---'      /       \    (     )    /       \      '---'       |
   /                  (  Slow   )    '---'    (  Fast   )                  \
  /                  ,-\       /---------------\       /-,                  \
 /                  /   '-...-'                 '-...-'   \                  \
|                  /                                       \                  |
|                 /       | |                     |⏎|       \                 |
 \               |                                           |               /
  \             /                                             \             /
   '---_____---'                                               '---_____---'

             ,---,                                           ,---,
             |   |                                           |   |
             | ^ |                                           | ^ |
             '---'                                           '---'
           ,-----,                                           ,-----,
           |Space|                                           |  <- |
        ,--'-----'--------,-------------------------,--------'-----'--,
       /    ,---,     ,--,|                         |,--,     ,---,    \
      /     |   |     |  ||         Mouse           ||  |    (Ctrl )    \
     / ,---. \ / .---,'--'|      [ Keyboard ]       |'--',---,'---',---, \
    |  |    >   <    |    |                         |   ( Cmd )   ( Opt ) |
    |  '---` / \ `---'    '-------------------------'    '---',---,'---'  |
    |       |   |       .-"""-.      ,---,      .-"""-.      (     )      |
    |       '---'      / qwert \    (     )    / yuiop \      '---'       |
   /                  (  asdfg  )    '---'    (  hjkl;  )                  \
  /                  ,-\ zxcvb /---------------\ nm,./ /-,                  \
 /                  /   '-...-'                 '-...-'   \                  \
|                  /                                       \                  |
|                 /       | |                     |⏎|       \                 |
 \               |                                           |               /
  \             /                                             \             /
   '---_____---'                                               '---_____---'

             ,---,                                           ,---,
             |   |                                           |   |
             | ^ |                                           | ^ |
             '---'                                           '---'
           ,-----,                                           ,-----,
           |Space|                                           |  <- |
        ,--'-----'--------,-------------------------,--------'-----'--,
       /    ,---,     ,--,|                         |,--,     ,---,    \
      /     |   |     |  ||         Mouse           ||  |    (Ctrl )    \
     / ,---. \ / .---,'--'|      [ Keyboard ]       |'--',---,'---',---, \
    |  |    >   <    |    |                         |   ( Cmd )   ( Opt ) |
,---,---,---,---,---,---,---,---,---,---,---,---,---,-------,',---,'---'  |
| § | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 0 | - | = |  <-   |(     )      |
'---'-,-'-,-'-,-'-,-'-,-'-,-'-,-'-,-'-,-'-,-'-,-'-,-'-,-----| '---'       |
| ->| | q | w | e | r | t | y | u | i | o | p | [ | ] |     |              \
'-----',--',--',--',--',--',--',--',--',--',--',--',--'     |               \
| Caps | a | s | d | f | g | h | j |<k>| l | ; | ' |   ⏎    |                \
'------',--',--',--',--',--',--',--',--',--',--',--'--------|                 |
| ^     | z | x |[c]| v | b | n | m | , | . | / |         ^ |                 |
'------,'---',--'--,'---'---'---'---'---'---'---'-----,-----||               /
| Ctrl | Alt | Cmd |                            | Cmd | Alt | \             /
'------'-----'-----'----------------------------'-----'-----'  '---_____---'
```

## Support

Numbers and `[` (`{`), `]` (`}`), `'` (`"`) keys are not implemented yet.

| Platform | Support                                                      |
|----------|--------------------------------------------------------------|
| macOS    | All features                                                 |
| Windows  | Issues with L2, R2 triggers, issues with Ctrl, Alt, Win keys |
| Linux    | Untested                                                     |

## How to use

Connect the gamepad before starting any scripts.

### Generating config.py

The provided config.py works on macOS Mojave with DualShock 4 connected via Bluetooth.

You may need to generate config.py on Windows to properly setup button numbers:
```
python3 configure.py
```
and then follow on screen instructions.

### Using

```
python3 main.py
```
Help on key mapping is printed in the terminal.
