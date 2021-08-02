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

Just a couple of words on typing. The main concept is that there are 8 directions of analog sticks and 2 degrees of tilt: small and large tilt. The central (resting) position is used to separate keystrokes.
Having that in mind let's take a look at the following scheme.
```
                         ,---,   ,---,   ,---,
                         | q |   | e |   | t |
,---,---,---,---,---,    '---|---|---|---|---'
| q | w | e | r | t |        | w | d | r |
|---|---|---|---|---|    ,---|---|---|---|---,
| a | s |<d>| f | g |    | a | s |< >| f | g |
|---|---|---|---|---|    '---|---|---|---|---'
| z | x | c | v | b |        | x | d | v |
'---'---'---'---'---'    ,---|---|---|---|---,
                         | z |   | c |   | b |
                         '---'   '---'   '---'
Part of keyboard view    Analog stick position
```

Note that `<d>` is in the `<` and `>` signs which are pointing to the left and right.
This indicate that the key `d` is not selected (so, no key is selected on the left side)
but small movement to the left or right will select `s` or `f` respectively.

Actually, there is no empty space between keys, so e. g. the position between `q` and `e` will
definitely belong to the closest key, but it's much easier to get either all the way up to `e`
or diagonally to `q`, hence, it doesn't introduce any issues.

So if you remember how the keyboard layout looks like then you can type without
looking on the helping keyboard view:
1. Move the analog stick in the chosen direction either slightly or to the end.
This will select the key but the keystroke is not done yet.
2. Let the analog stick return into resting position - this will register a keystroke.

You can move left and right sticks independently and whatever stick returned to the
resting position first will register a keystroke first.

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
