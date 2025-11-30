
# "Splash","Title","Action","Rebind","GameOver","Elevator","Config", "Story"
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 960
STARTING_STATE = 'Splash' # default Splash
STARTING_FLOOR = 15 # default 1 # bosses: 5, 8, 13, 15
NUMBER_OF_ENEMIES_TO_SPAWN = 0 #3
LOOT_CHANCE = 0.15

INPUT_MAPS = {
    "xbox": {"SHOOT_DOWN": 0, "SHOOT_RIGHT": 1, "SHOOT_LEFT": 2, "SHOOT_UP": 3, "START": 7},
    "playstation": {"SHOOT_DOWN": 0, "SHOOT_RIGHT": 1, "SHOOT_LEFT": 2, "SHOOT_UP": 3, "START": 7},
    "switch": {"SHOOT_DOWN": 0, "SHOOT_RIGHT": 1, "SHOOT_LEFT": 3, "SHOOT_UP": 2, "START": 10},
}

POPUP_TEXTS = {

    "INTRO": [
        "Project W.A.V.E.S...",
        "Behind that name lies a mysterious string of disappearances we came here to investigate.",
        "",
        "The folks in town were helpful enough to point us to a large building standing ominously",
        "atop the highest hill.",
        "",
        "They say this is \"Where All Victims End Silently\".",
        "",
        "Armed only with our trusty M9s, we entered. What we found there... astonished us."
    ],

    "BEFORE_FINAL_BOSS": [
        "This is it. The last floor.",
        "",
        "Ready your guns and confront the mastermind!",
        "",
        "It's time to end this sordid affair once and for all."
    ],

    "AFTER_FINAL_BOSS": [
        "The signal is dead. The mastermind's big dish-head-thing has finally cracked.",
        "",
        "The villagers blink and stretch, vaguely wondering why they're wearing matching cloaks,",
        "and what exactly was so great about The Great Frequency they were chanting about",
        "mere seconds ago.",
        "",
        "You've silenced the waves and saved the village. And you didn't even need a tin foil hat.",
        "",
        "Thank you for playing!"
    ],

    "TIP1": [
        "Welcome to Project W.A.V.E.S!",
        "",
        "Use arrow keys to move and W/A/S/D to shoot up/left/down/right",
        "",
        "Or use a gamepad (d-pad or left stick to move, A/B/X/Y to shoot)",
        "",
        "If your keyboard uses the AZERTY layout, fear not!",
        "Just press the F1 key to switch to ZQSD"
    ],

    "TIP2": [
        "There are communication towers scattered on this floor and others.",
        "It seems they are sending brainwashing waves that force the cultists", 
        "to attack you on sight.",
        "",
        "Until you destroy them, they will keep shooting harmful waves at you from afar.",
        "Destroy all towers on a floor to unlock the elevator."
    ]

}