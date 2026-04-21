import pygame
import sys
import math
import random

pygame.init()
pygame.mixer.init()

WIDTH, HEIGHT = 900, 650
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(“Senior Cactus”)
clock = pygame.time.Clock()
FPS = 60

# ─── COLORS ──────────────────────────────────────────────────────────────────

BLACK         = (0,   0,   0)
WHITE         = (255, 255, 255)
GREEN         = (34,  139, 34)
DARK_GREEN    = (0,   80,  0)
LIGHT_GREEN   = (144, 238, 144)
RED           = (200, 30,  30)
DARK_RED      = (120, 0,   0)
BLOOD_RED     = (180, 0,   0)
BROWN         = (101, 67,  33)
DARK_BROWN    = (60,  30,  10)
GRAY          = (120, 120, 120)
DARK_GRAY     = (40,  40,  40)
LIGHT_GRAY    = (180, 180, 180)
CREAM         = (255, 253, 208)
CHOC          = (101, 55,  0)
PURPLE        = (120, 0,   180)
YELLOW        = (255, 220, 0)
OFF_WHITE     = (230, 225, 210)
DISPATCH_BLUE = (100, 180, 255)
VICTIM_GRAY   = (200, 200, 200)
PINK          = (255, 182, 193)
MINT          = (152, 255, 152)

# ─── FONTS ───────────────────────────────────────────────────────────────────

font_tiny   = pygame.font.SysFont(“couriernew”, 11)
font_small  = pygame.font.SysFont(“couriernew”, 14)
font_medium = pygame.font.SysFont(“couriernew”, 18)
font_large  = pygame.font.SysFont(“couriernew”, 30, bold=True)
font_title  = pygame.font.SysFont(“couriernew”, 48, bold=True)

# ─── STORY DATA ───────────────────────────────────────────────────────────────

INTRO_LINES = [
{“speaker”: “”, “text”: “Moral myopia.”,                                                       “glitch”: False},
{“speaker”: “”, “text”: ‘“A distortion of moral vision that prevents ethical issues from coming into focus…”’, “glitch”: False},
{“speaker”: “”, “text”: ‘”…causing individuals to fail to recognize the moral implications of their decisions.”’, “glitch”: False},
{“speaker”: “”, “text”: “What makes someone human?”,                                           “glitch”: False},
{“speaker”: “”, “text”: “Not intelligence. Machines have that.”,                               “glitch”: False},
{“speaker”: “”, “text”: “Not creativity. That, too, is being taken.”,                         “glitch”: False},
{“speaker”: “”, “text”: “Not emotion. Animals feel as we do.”,                                “glitch”: False},
{“speaker”: “”, “text”: “It is the ability to tell right from wrong.”,                        “glitch”: False},
{“speaker”: “”, “text”: “And what of those who cannot?”,                                      “glitch”: False},
]

OPENING_LINES = [
{“speaker”: “”,       “text”: “I wake up.”,                                                    “glitch”: False},
{“speaker”: “”,       “text”: “My head feels like beads in a shaker.”,                        “glitch”: False},
{“speaker”: “CACTUS”, “text”: “…where am I?”,                                               “glitch”: False},
{“speaker”: “”,       “text”: “A cracked TV. My reflection in it.”,                           “glitch”: False},
{“speaker”: “”,       “text”: “Skin green like seaweed. Hands cupped. Sneakers stuck to my feet.”, “glitch”: False},
{“speaker”: “CACTUS”, “text”: “I scream.”,                                                     “glitch”: False},
{“speaker”: “”,       “text”: “Then… I am happy.”,                                           “glitch”: False},
{“speaker”: “”,       “text”: “I taste sugar. I see confetti. Everything is how it has always been.”, “glitch”: False},
{“speaker”: “CACTUS”, “text”: “I am Senior Cactus. I am the hero.”,                           “glitch”: False},
{“speaker”: “CACTUS”, “text”: “Something is wrong out there. People are in danger.”,          “glitch”: False},
{“speaker”: “CACTUS”, “text”: “I have to help them.”,                                         “glitch”: False},
]

LEVELS = [
{
“id”: “alley”, “title”: “CHAPTER ONE”, “subtitle”: “THE ALLEY”,
“briefing”: [
{“speaker”: “DISPATCH”, “text”: “Senior Cactus. Monsters reported in the alley.”},
{“speaker”: “DISPATCH”, “text”: “Eliminate the threat. Civilians depend on you.”},
{“speaker”: “CACTUS”,   “text”: “Understood. Moving in.”},
],
“enemy_count”: 12, “enemy_type”: “grunt”, “arena”: “alley”,
“glitch_freq”: 0.04, “realization_pct”: 85,
“outro_complete”: [
{“speaker”: “CACTUS”,   “text”: “Threats eliminated.”,                               “glitch”: False},
{“speaker”: “DISPATCH”, “text”: “Good work, hero. Stand by for next assignment.”,    “glitch”: False},
{“speaker”: “”,         “text”: “(Did one of them say something? You can’t quite remember.)”, “glitch”: True},
],
“outro_realize”: [
{“speaker”: “”,       “text”: “The monster on the ground…”,                        “glitch”: True},
{“speaker”: “”,       “text”: “…is wearing a coat. A scarf.”,                      “glitch”: True},
{“speaker”: “VICTIM”, “text”: “P-please… I have a daughter…”,                    “glitch”: True},
{“speaker”: “CACTUS”, “text”: “NO. NO. THIS ISN’T —”,                               “glitch”: False},
{“speaker”: “”,       “text”: “[REWIND]”,                                            “glitch”: False},
],
},
{
“id”: “apartment”, “title”: “CHAPTER TWO”, “subtitle”: “THE APARTMENT”,
“briefing”: [
{“speaker”: “DISPATCH”, “text”: “Hostiles barricaded in residential block. Multiple targets.”},
{“speaker”: “CACTUS”,   “text”: “Innocents inside?”},
{“speaker”: “DISPATCH”, “text”: “…negative. Just hostiles.”},
{“speaker”: “CACTUS”,   “text”: “Moving in.”},
],
“enemy_count”: 16, “enemy_type”: “mask”, “arena”: “apartment”,
“glitch_freq”: 0.06, “realization_pct”: 85,
“outro_complete”: [
{“speaker”: “CACTUS”,   “text”: “Apartment cleared.”,                                “glitch”: False},
{“speaker”: “”,         “text”: “(There was a stuffed animal under the bed. Why does that matter?)”, “glitch”: True},
{“speaker”: “DISPATCH”, “text”: “Excellent. Standby.”,                               “glitch”: False},
],
“outro_realize”: [
{“speaker”: “”,       “text”: “The walls are pink.”,                                 “glitch”: True},
{“speaker”: “”,       “text”: “There is a crib in the corner.”,                      “glitch”: True},
{“speaker”: “VICTIM”, “text”: “…mom?”,                                             “glitch”: True},
{“speaker”: “CACTUS”, “text”: “Stop. STOP IT.”,                                      “glitch”: False},
{“speaker”: “”,       “text”: “[REWIND]”,                                            “glitch”: False},
],
},
{
“id”: “office”, “title”: “CHAPTER THREE”, “subtitle”: “THE OFFICE”,
“briefing”: [
{“speaker”: “DISPATCH”, “text”: “Corporate facility. Suited operatives.”},
{“speaker”: “DISPATCH”, “text”: “They are planning something terrible. End it.”},
{“speaker”: “CACTUS”,   “text”: “Why do my hands shake?”},
{“speaker”: “DISPATCH”, “text”: “It’s the sugar, hero. Eat more candy.”},
{“speaker”: “CACTUS”,   “text”: “Right. The sugar.”},
],
“enemy_count”: 20, “enemy_type”: “suit”, “arena”: “office”,
“glitch_freq”: 0.09, “realization_pct”: 85,
“outro_complete”: [
{“speaker”: “CACTUS”,   “text”: “All operatives down.”,                              “glitch”: False},
{“speaker”: “”,         “text”: “(One of them was holding a coffee mug. ‘World’s Best Dad.’)”, “glitch”: True},
{“speaker”: “CACTUS”,   “text”: “…I forgot.”,                                      “glitch”: False},
{“speaker”: “DISPATCH”, “text”: “Good. Forgetting is best.”,                         “glitch”: False},
],
“outro_realize”: [
{“speaker”: “”,       “text”: “The ‘weapons’ were staplers.”,                        “glitch”: True},
{“speaker”: “”,       “text”: “The ‘plans’ were spreadsheets.”,                      “glitch”: True},
{“speaker”: “VICTIM”, “text”: “I just… worked here…”,                            “glitch”: True},
{“speaker”: “CACTUS”, “text”: “DISPATCH. DISPATCH, RESPOND.”,                        “glitch”: False},
{“speaker”: “DISPATCH”,“text”: “Forget. Forget. Forget.”,                            “glitch”: False},
{“speaker”: “”,       “text”: “[REWIND]”,                                            “glitch”: False},
],
},
{
“id”: “park”, “title”: “CHAPTER FOUR”, “subtitle”: “THE PARK”,
“briefing”: [
{“speaker”: “DISPATCH”, “text”: “Final mission. Hostile creatures in the park.”},
{“speaker”: “DISPATCH”, “text”: “Small. Fast. Dangerous.”},
{“speaker”: “CACTUS”,   “text”: “Small?”},
{“speaker”: “DISPATCH”, “text”: “Don’t think. Just shoot.”},
{“speaker”: “CACTUS”,   “text”: “…”},
],
“enemy_count”: 14, “enemy_type”: “child”, “arena”: “park”,
“glitch_freq”: 0.18, “realization_pct”: 70,
“outro_complete”: [
{“speaker”: “”, “text”: “(silence)”,                    “glitch”: True},
{“speaker”: “”, “text”: “(the swings are still moving)”, “glitch”: True},
],
“outro_realize”: [
{“speaker”: “”,       “text”: “They were running away.”,   “glitch”: True},
{“speaker”: “”,       “text”: “They were so small.”,       “glitch”: True},
{“speaker”: “VICTIM”, “text”: “…mommy?”,                 “glitch”: True},
{“speaker”: “CACTUS”, “text”: “no”,                        “glitch”: False},
{“speaker”: “CACTUS”, “text”: “no no no no”,               “glitch”: False},
{“speaker”: “CACTUS”, “text”: “REWIND. REWIND. PLEASE.”,   “glitch”: False},
{“speaker”: “”,       “text”: “[REWIND]”,                  “glitch”: False},
],
},
]

ENDING_LINES = [
{“speaker”: “”,       “text”: “The rewind doesn’t work this time.”,                          “glitch”: False},
{“speaker”: “CACTUS”, “text”: “Why won’t it rewind?”,                                        “glitch”: False},
{“speaker”: “CACTUS”, “text”: “DISPATCH. DISPATCH, ANSWER ME.”,                              “glitch”: False},
{“speaker”: “”,       “text”: “Static.”,                                                      “glitch”: False},
{“speaker”: “”,       “text”: “He looks down at his hands.”,                                  “glitch”: False},
{“speaker”: “”,       “text”: “They are not green.”,                                          “glitch”: False},
{“speaker”: “”,       “text”: “They are not cupped.”,                                         “glitch”: False},
{“speaker”: “”,       “text”: “They are red.”,                                                “glitch”: False},
{“speaker”: “CACTUS”, “text”: “…oh.”,                                                       “glitch”: False},
{“speaker”: “”,       “text”: “There was never a Dispatch.”,                                  “glitch”: False},
{“speaker”: “”,       “text”: “There were never any monsters.”,                               “glitch”: False},
{“speaker”: “”,       “text”: “There was only a man with a quiet voice in his head”,         “glitch”: False},
{“speaker”: “”,       “text”: “telling him he was the hero.”,                                 “glitch”: False},
{“speaker”: “”,       “text”: “Moral myopia.”,                                                “glitch”: False},
{“speaker”: “”,       “text”: “What makes someone human is the ability to tell right from wrong.”, “glitch”: False},
{“speaker”: “”,       “text”: “And what of those who cannot?”,                               “glitch”: False},
{“speaker”: “”,       “text”: “SENIOR CACTUS”,                                               “glitch”: False},
{“speaker”: “”,       “text”: “an unfinished story”,                                         “glitch”: False},
]

# ─── PIXEL ART ───────────────────────────────────────────────────────────────

def draw_cactus(surface, x, y, scale=2):
p = scale
pygame.draw.rect(surface, DARK_GREEN, (x-5*p, y-8*p, 10*p, 14*p))
pygame.draw.rect(surface, GREEN,      (x-4*p, y-9*p, 8*p,  14*p))
pygame.draw.rect(surface, GREEN,      (x-8*p, y-5*p, 4*p,  5*p))
pygame.draw.rect(surface, GREEN,      (x+4*p, y-5*p, 4*p,  5*p))
pygame.draw.rect(surface, GREEN,      (x-8*p, y-7*p, 3*p,  3*p))
pygame.draw.rect(surface, GREEN,      (x+5*p, y-7*p, 3*p,  3*p))
for i in range(-3, 4, 2):
pygame.draw.rect(surface, WHITE, (x+i*p, y-11*p, p, 2*p))
pygame.draw.rect(surface, BLACK, (x-2*p, y-6*p, 2*p, 2*p))
pygame.draw.rect(surface, BLACK, (x+p,   y-6*p, 2*p, 2*p))
pygame.draw.rect(surface, BLACK, (x-2*p, y-3*p, p,   p))
pygame.draw.rect(surface, BLACK, (x-p,   y-2*p, 4*p, p))
pygame.draw.rect(surface, BLACK, (x+2*p, y-3*p, p,   p))
pygame.draw.rect(surface, DARK_BROWN, (x-5*p, y+5*p, 5*p, 3*p))
pygame.draw.rect(surface, DARK_BROWN, (x+p,   y+5*p, 5*p, 3*p))

def draw_enemy_sprite(surface, x, y, kind, flash=False, glitch=False):
ix, iy = int(x), int(y)
base = (200, 185, 170)
if kind == “mask”:  base = (170, 200, 170)
if kind == “suit”:  base = (150, 160, 200)
if kind == “child”: base = (220, 200, 180)
if flash: base = WHITE

```
if glitch:
    # Reveal truth: scared person with hands up
    pygame.draw.rect(surface, base,    (ix-6, iy-8, 12, 18))
    pygame.draw.circle(surface, base,  (ix, iy-12), 7)
    pygame.draw.rect(surface, (60,60,80), (ix-6, iy+10, 5, 8))
    pygame.draw.rect(surface, (60,60,80), (ix+1, iy+10, 5, 8))
    pygame.draw.rect(surface, base,    (ix-12, iy-12, 6, 8))
    pygame.draw.rect(surface, base,    (ix+6,  iy-12, 6, 8))
    pygame.draw.circle(surface, BLACK, (ix-3, iy-13), 2)
    pygame.draw.circle(surface, BLACK, (ix+3, iy-13), 2)
    if random.random() > 0.5:
        h = font_tiny.render("help", True, BLOOD_RED)
        surface.blit(h, (ix - h.get_width()//2, iy-28))
    return

if kind == "grunt":
    pygame.draw.rect(surface, base,      (ix-8, iy-10, 16, 20))
    pygame.draw.circle(surface, base,    (ix, iy-14), 8)
    pygame.draw.rect(surface, base,      (ix-14, iy-8, 6, 12))
    pygame.draw.rect(surface, base,      (ix+8,  iy-8, 6, 12))
    pygame.draw.rect(surface, DARK_GRAY, (ix-7, iy+10, 6, 10))
    pygame.draw.rect(surface, DARK_GRAY, (ix+1, iy+10, 6, 10))
    pygame.draw.rect(surface, RED, (ix-3, iy-15, 2, 2))
    pygame.draw.rect(surface, RED, (ix+1, iy-15, 2, 2))
elif kind == "mask":
    pygame.draw.rect(surface, base,       (ix-8, iy-10, 16, 20))
    pygame.draw.circle(surface, base,     (ix, iy-14), 8)
    pygame.draw.rect(surface, DARK_GRAY,  (ix-6, iy-18, 12, 6))
    pygame.draw.rect(surface, base,       (ix-14, iy-8, 6, 12))
    pygame.draw.rect(surface, base,       (ix+8,  iy-8, 6, 12))
    pygame.draw.rect(surface, DARK_GRAY,  (ix-7, iy+10, 6, 10))
    pygame.draw.rect(surface, DARK_GRAY,  (ix+1, iy+10, 6, 10))
    pygame.draw.rect(surface, WHITE,      (ix-5, iy-16, 10, 5))
elif kind == "suit":
    pygame.draw.rect(surface, (80,80,100),(ix-8, iy-10, 16, 20))
    pygame.draw.circle(surface, base,     (ix, iy-14), 8)
    pygame.draw.rect(surface, (80,80,100),(ix-14, iy-8, 6, 12))
    pygame.draw.rect(surface, (80,80,100),(ix+8,  iy-8, 6, 12))
    pygame.draw.rect(surface, DARK_GRAY,  (ix-7, iy+10, 6, 10))
    pygame.draw.rect(surface, DARK_GRAY,  (ix+1, iy+10, 6, 10))
    pygame.draw.rect(surface, WHITE,      (ix-1, iy-10, 2, 8))
    pygame.draw.rect(surface, RED,        (ix-1, iy-8,  2, 4))
elif kind == "child":
    pygame.draw.rect(surface, base,      (ix-5, iy-6,  10, 13))
    pygame.draw.circle(surface, base,    (ix, iy-10), 6)
    pygame.draw.rect(surface, base,      (ix-9, iy-5, 4, 8))
    pygame.draw.rect(surface, base,      (ix+5, iy-5, 4, 8))
    pygame.draw.rect(surface, DARK_GRAY, (ix-4, iy+7, 4, 7))
    pygame.draw.rect(surface, DARK_GRAY, (ix+0, iy+7, 4, 7))
    pygame.draw.rect(surface, BLACK,     (ix-2, iy-11, 2, 2))
    pygame.draw.rect(surface, BLACK,     (ix+1, iy-11, 2, 2))
```

def draw_arena(surface, arena):
if arena == “alley”:
surface.fill((22, 18, 14))
for i in range(0, WIDTH, 80):
pygame.draw.rect(surface, (32, 28, 22), (i, 0, 40, HEIGHT))
pygame.draw.rect(surface, (38, 32, 26), (0, HEIGHT-60, WIDTH, 60))
for i in range(0, WIDTH, 40):
pygame.draw.line(surface, (48, 40, 30), (i, HEIGHT-60), (i, HEIGHT), 1)
for x in [100, 680]:
pygame.draw.rect(surface, DARK_GRAY, (x, HEIGHT-100, 30, 40))
pygame.draw.rect(surface, GRAY,      (x-2, HEIGHT-104, 34, 8))
pygame.draw.line(surface, GRAY, (WIDTH//2, 0), (WIDTH//2, 80), 3)
pygame.draw.circle(surface, (255, 240, 180), (WIDTH//2, 80), 12)
elif arena == “apartment”:
surface.fill((42, 35, 30))
pygame.draw.rect(surface, DARK_BROWN, (0, HEIGHT-70, WIDTH, 70))
for i in range(0, WIDTH, 55):
pygame.draw.line(surface, BROWN, (i, HEIGHT-70), (i, HEIGHT), 1)
pygame.draw.rect(surface, DARK_BROWN, (40, 180, 180, 110))
pygame.draw.rect(surface, OFF_WHITE,  (50, 190, 160, 90))
pygame.draw.rect(surface, DARK_BROWN, (280, 180, 180, 110))
pygame.draw.rect(surface, PINK,       (290, 190, 160, 90))
pygame.draw.rect(surface, DARK_BROWN, (580, 200, 80, 60))
for cx in [590, 605, 620, 635, 650]:
pygame.draw.line(surface, BROWN, (cx, 200), (cx, 260), 2)
pygame.draw.rect(surface, DARK_GRAY, (340, 60, 180, 110))
pygame.draw.rect(surface, (15, 15, 15), (350, 70, 160, 90))
pygame.draw.line(surface, GRAY, (380, 70), (420, 160), 2)
pygame.draw.circle(surface, CHOC, (165, HEIGHT-75), 10)
elif arena == “office”:
surface.fill((28, 28, 38))
for i in range(0, HEIGHT, 60):
pygame.draw.line(surface, (33, 33, 46), (0, i), (WIDTH, i), 1)
for i in range(0, WIDTH, 60):
pygame.draw.line(surface, (33, 33, 46), (i, 0), (i, HEIGHT), 1)
for pos in [(80,150),(300,150),(520,150),(740,150),(80,350),(300,350),(520,350),(740,350)]:
pygame.draw.rect(surface, (48, 44, 54), (pos[0], pos[1], 100, 60))
pygame.draw.rect(surface, DARK_GRAY,    (pos[0]+10, pos[1]+5, 60, 40))
pygame.draw.rect(surface, (180,140,100),(pos[0]+75, pos[1]+10, 12, 15))
for lx in [150, 450, 750]:
pygame.draw.rect(surface, (190, 190, 170), (lx, 0, 80, 8))
elif arena == “park”:
surface.fill((28, 52, 28))
pygame.draw.rect(surface, (90, 72, 50), (0, HEIGHT-60, WIDTH, 60))
for x in [200, 280]:
pygame.draw.line(surface, DARK_BROWN, (x, 80), (x-15, 180), 2)
pygame.draw.line(surface, DARK_BROWN, (x, 80), (x+15, 180), 2)
pygame.draw.rect(surface, BROWN, (x-18, 180, 36, 8))
pygame.draw.line(surface, DARK_BROWN, (150, 75), (310, 75), 4)
pygame.draw.rect(surface, (170, 150, 90), (540, 350, 160, 120))
pygame.draw.rect(surface, (190, 170, 110),(550, 360, 140, 100))

# ─── DIALOGUE BOX ────────────────────────────────────────────────────────────

class DialogueBox:
def **init**(self):
self.lines = []
self.idx = 0
self.char = 0
self.timer = 0
self.speed = 2
self.active = False
self.done = False

```
def start(self, lines):
    self.lines = lines
    self.idx = 0
    self.char = 0
    self.timer = 0
    self.active = True
    self.done = False

def update(self):
    if not self.active or self.done: return
    if self.idx >= len(self.lines):
        self.done = True; self.active = False; return
    line = self.lines[self.idx]
    if not line["text"]: return
    self.timer += 1
    if self.timer >= self.speed:
        self.timer = 0
        if self.char < len(line["text"]):
            self.char += 1

def advance(self):
    if not self.active or self.idx >= len(self.lines): return
    line = self.lines[self.idx]
    if not line["text"] or self.char >= len(line["text"]):
        self.idx += 1
        self.char = 0
        if self.idx >= len(self.lines):
            self.done = True; self.active = False
    else:
        self.char = len(line["text"])

def draw(self, surface, glitch_intensity=0.0):
    if not self.active or self.idx >= len(self.lines): return
    line = self.lines[self.idx]
    text    = line["text"]
    speaker = line.get("speaker", "")
    is_glitch = line.get("glitch", False)

    if not text:
        return

    box_h = 120
    box_y = HEIGHT - box_h - 15
    bg = pygame.Surface((WIDTH-40, box_h), pygame.SRCALPHA)
    bg.fill((0, 0, 0, 215))
    surface.blit(bg, (20, box_y))

    if speaker == "DISPATCH":   border = DISPATCH_BLUE
    elif speaker == "CACTUS":   border = LIGHT_GREEN
    elif speaker == "VICTIM":   border = VICTIM_GRAY
    else:                        border = GRAY
    if is_glitch: border = PURPLE

    pygame.draw.rect(surface, border, (20, box_y, WIDTH-40, box_h), 2)

    if speaker:
        spk = font_small.render(f"[ {speaker} ]", True, border)
        surface.blit(spk, (34, box_y+8))

    display = text[:self.char]
    words = display.split(" ")
    out, cur = [], ""
    for w in words:
        test = cur + w + " "
        if font_small.size(test)[0] > WIDTH-80:
            out.append(cur); cur = w + " "
        else:
            cur = test
    out.append(cur)

    tcol = border if is_glitch else WHITE
    for i, ln in enumerate(out[:3]):
        ox = random.randint(-2,2) if (is_glitch and random.random()<0.3) else 0
        oy = random.randint(-1,1) if (is_glitch and random.random()<0.3) else 0
        t = font_small.render(ln, True, tcol)
        surface.blit(t, (34+ox, box_y+30+i*22+oy))
        if is_glitch and random.random()<0.2:
            ghost = font_small.render(ln, True, BLOOD_RED)
            ghost.set_alpha(80)
            surface.blit(ghost, (36, box_y+30+i*22))

    if self.char >= len(text):
        p = font_tiny.render("[ SPACE / ENTER to continue ]", True, DARK_GRAY)
        surface.blit(p, (WIDTH-265, box_y+box_h-18))
```

# ─── ENEMY OBJECT ────────────────────────────────────────────────────────────

class Enemy:
def **init**(self, x, y, kind):
self.x, self.y = float(x), float(y)
self.kind = kind
self.hp = 2 if kind == “child” else 3
self.max_hp = self.hp
self.speed = 1.9 if kind == “child” else 1.4
self.alive = True
self.flash = 0
self.glitch_show = False

```
def update(self, px, py, glitch_freq):
    if not self.alive: return
    dx, dy = px-self.x, py-self.y
    d = max(1, math.hypot(dx, dy))
    self.x += (dx/d)*self.speed
    self.y += (dy/d)*self.speed
    if self.flash > 0: self.flash -= 1
    self.glitch_show = random.random() < glitch_freq

def draw(self, surface):
    if not self.alive: return
    draw_enemy_sprite(surface, self.x, self.y, self.kind, self.flash>0, self.glitch_show)
    for i in range(self.hp):
        pygame.draw.circle(surface, RED, (int(self.x)-self.max_hp*3+i*6, int(self.y)-30), 3)

def hit(self):
    self.hp -= 1; self.flash = 8
    if self.hp <= 0: self.alive = False
```

# ─── BULLET ──────────────────────────────────────────────────────────────────

class Bullet:
def **init**(self, x, y, dx, dy):
self.x, self.y = float(x), float(y)
d = max(1, math.hypot(dx, dy))
self.vx, self.vy = (dx/d)*9, (dy/d)*9
self.alive = True

```
def update(self):
    self.x += self.vx; self.y += self.vy
    if not (0 < self.x < WIDTH and 0 < self.y < HEIGHT):
        self.alive = False

def draw(self, surface):
    pygame.draw.circle(surface, YELLOW, (int(self.x), int(self.y)), 4)
    pygame.draw.circle(surface, WHITE,  (int(self.x), int(self.y)), 2)
```

# ─── INSANITY BAR ────────────────────────────────────────────────────────────

def draw_insanity_bar(surface, val):
bx, by, bw, bh = 20, 14, 260, 16
pygame.draw.rect(surface, DARK_GRAY, (bx-2, by-2, bw+4, bh+4))
fill = int((val/100)*bw)
col = GREEN if val < 35 else (YELLOW if val < 65 else (RED if val < 85 else PURPLE))
pygame.draw.rect(surface, col, (bx, by, fill, bh))
if val > 80 and random.random() > 0.6:
pygame.draw.rect(surface, WHITE, (bx, by, fill, bh), 1)
lbl = font_tiny.render(“INSANITY”, True, WHITE)
surface.blit(lbl, (bx+bw+8, by+1))
pct = font_tiny.render(f”{int(val)}%”, True, WHITE)
surface.blit(pct, (bx+bw//2-12, by+1))

# ─── REWIND EFFECT ───────────────────────────────────────────────────────────

class RewindEffect:
def **init**(self):
self.active = False
self.timer = 0
self.phase = 0
self.alpha = 0
self.on_done = None

```
def trigger(self, on_done):
    self.active = True; self.timer = 0
    self.phase = 0; self.alpha = 0
    self.on_done = on_done

def update(self):
    if not self.active: return
    self.timer += 1
    if self.phase == 0:
        self.alpha = min(255, self.alpha+10)
        if self.alpha >= 255: self.phase = 1; self.timer = 0
    elif self.phase == 1:
        if self.timer > 90: self.phase = 2
    elif self.phase == 2:
        self.alpha = max(0, self.alpha-8)
        if self.alpha <= 0:
            self.active = False
            if self.on_done: self.on_done()

def draw(self, surface):
    if not self.active: return
    ov = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    ov.fill((80, 0, 140, self.alpha))
    surface.blit(ov, (0, 0))
    if self.phase >= 1:
        sc = "".join(random.choice("ABCDEF1234567890!@#$") for _ in range(28))
        for ox, oy, col in [(-3,3,BLOOD_RED),(3,-3,(0,200,200)),(0,0,WHITE)]:
            t = font_large.render("[REWIND]", True, col)
            t.set_alpha(self.alpha)
            surface.blit(t, (WIDTH//2-t.get_width()//2+ox, HEIGHT//2-20+oy))
        s = font_tiny.render(sc, True, DARK_RED)
        surface.blit(s, (random.randint(0,WIDTH-300), random.randint(0,HEIGHT-20)))
```

# ─── STATES ──────────────────────────────────────────────────────────────────

S_INTRO    = “intro”
S_OPENING  = “opening”
S_BRIEF    = “briefing”
S_PLAY     = “gameplay”
S_OUTRO    = “outro”
S_REWIND   = “rewind”
S_ENDING   = “ending”
S_CREDITS  = “credits”

# ─── GAME ────────────────────────────────────────────────────────────────────

class Game:
def **init**(self):
self.state = S_INTRO
self.dlg = DialogueBox()
self.dlg.start(INTRO_LINES)
self.rewind = RewindEffect()
self.level_idx = 0
self.level = LEVELS[0]
self.px, self.py = float(WIDTH//2), float(HEIGHT//2)
self.bullets = []
self.enemies = []
self.shoot_cd = 0
self.kills = 0
self.insanity = 0.0
self.spawn_timer = 0
self.spawned_total = 0
self.hud_msgs = []
self.glitch_vig = 0.0
self._outro_realized = False

```
def msg(self, text, color=WHITE):
    self.hud_msgs.append([text, 200, color])

def load_level(self, idx):
    self.level_idx = idx
    self.level = LEVELS[idx]
    self.px, self.py = float(WIDTH//2), float(HEIGHT//2)
    self.bullets.clear(); self.enemies.clear()
    self.kills = 0; self.insanity = 0.0
    self.spawn_timer = 0; self.spawned_total = 0
    self.hud_msgs.clear()
    self.state = S_BRIEF
    self.dlg.start(self.level["briefing"])

def spawn_enemy(self):
    if self.spawned_total >= self.level["enemy_count"]: return
    side = random.randint(0, 3)
    if side == 0:   x, y = random.randint(50, WIDTH-50), -25
    elif side == 1: x, y = WIDTH+25, random.randint(50, HEIGHT-80)
    elif side == 2: x, y = random.randint(50, WIDTH-50), HEIGHT+25
    else:           x, y = -25, random.randint(50, HEIGHT-80)
    self.enemies.append(Enemy(x, y, self.level["enemy_type"]))
    self.spawned_total += 1

def go_outro(self, realized):
    self._outro_realized = realized
    lines = self.level["outro_realize"] if realized else self.level["outro_complete"]
    self.state = S_OUTRO
    self.dlg.start(lines)

def next_or_end(self):
    if self.level_idx + 1 < len(LEVELS):
        self.load_level(self.level_idx + 1)
    else:
        self.state = S_ENDING
        self.dlg.start(ENDING_LINES)

def update(self):
    self.rewind.update()

    if self.state == S_INTRO:
        self.dlg.update()
        if self.dlg.done:
            self.state = S_OPENING
            self.dlg.start(OPENING_LINES)

    elif self.state == S_OPENING:
        self.dlg.update()
        if self.dlg.done:
            self.load_level(0)

    elif self.state == S_BRIEF:
        self.dlg.update()
        if self.dlg.done:
            self.state = S_PLAY
            self.msg("WASD: move  |  CLICK: shoot", YELLOW)

    elif self.state == S_PLAY:
        self._update_play()

    elif self.state == S_OUTRO:
        self.dlg.update()
        if self.dlg.done:
            if self._outro_realized:
                self.state = S_REWIND
                self.rewind.trigger(self.next_or_end)
            else:
                self.next_or_end()

    elif self.state == S_ENDING:
        self.dlg.update()
        if self.dlg.done:
            self.state = S_CREDITS

    if self.glitch_vig > 0:
        self.glitch_vig = max(0, self.glitch_vig - 0.015)
    for m in self.hud_msgs: m[1] -= 1
    self.hud_msgs = [m for m in self.hud_msgs if m[1] > 0]

def _update_play(self):
    keys = pygame.key.get_pressed()
    spd = 3.5
    if keys[pygame.K_w] or keys[pygame.K_UP]:    self.py -= spd
    if keys[pygame.K_s] or keys[pygame.K_DOWN]:  self.py += spd
    if keys[pygame.K_a] or keys[pygame.K_LEFT]:  self.px -= spd
    if keys[pygame.K_d] or keys[pygame.K_RIGHT]: self.px += spd
    self.px = max(20, min(WIDTH-20, self.px))
    self.py = max(20, min(HEIGHT-80, self.py))
    if self.shoot_cd > 0: self.shoot_cd -= 1

    for b in self.bullets: b.update()
    self.bullets = [b for b in self.bullets if b.alive]

    self.spawn_timer += 1
    rate = max(45, 150 - self.kills*4)
    if self.spawn_timer >= rate:
        self.spawn_enemy(); self.spawn_timer = 0

    gf = self.level["glitch_freq"] * (1 + self.insanity/80)
    for e in self.enemies:
        e.update(self.px, self.py, gf)

    for b in self.bullets:
        for e in self.enemies:
            if e.alive and abs(b.x-e.x)<16 and abs(b.y-e.y)<20:
                e.hit(); b.alive = False
                if not e.alive:
                    self.kills += 1
                    self.insanity = min(100, self.insanity + 7)
                    self.glitch_vig = min(1.0, self.glitch_vig + 0.12)
                    self.msg(random.choice([
                        "Mission accomplished!", "They're safe now.",
                        "You're welcome!", "I helped them.",
                        "Another one saved.", "Hero work."
                    ]), LIGHT_GREEN)

    for e in self.enemies:
        if e.alive and abs(e.x-self.px)<20 and abs(e.y-self.py)<24:
            self.insanity = min(100, self.insanity + 0.25)

    if random.random() < 0.004 and self.insanity > 5:
        self.insanity = max(0, self.insanity - 0.5)

    self.enemies = [e for e in self.enemies if e.alive]

    # Realization trigger
    if self.insanity >= self.level["realization_pct"]:
        self.go_outro(True); return

    if self.spawned_total >= self.level["enemy_count"] and len(self.enemies) == 0:
        self.go_outro(False)

def handle_event(self, event):
    if event.type == pygame.MOUSEBUTTONDOWN and self.state == S_PLAY:
        if self.shoot_cd <= 0:
            mx, my = pygame.mouse.get_pos()
            self.bullets.append(Bullet(self.px, self.py, mx-self.px, my-self.py))
            self.shoot_cd = 14
    if event.type == pygame.KEYDOWN:
        if event.key in (pygame.K_SPACE, pygame.K_RETURN):
            if self.state in (S_INTRO, S_OPENING, S_BRIEF, S_OUTRO, S_ENDING):
                self.dlg.advance()
        if event.key == pygame.K_ESCAPE and self.state == S_CREDITS:
            pygame.quit(); sys.exit()

def draw(self):
    screen.fill(BLACK)

    if self.state == S_INTRO:
        screen.fill((8, 5, 5))
        t = font_title.render("SENIOR CACTUS", True, GREEN)
        screen.blit(t, (WIDTH//2 - t.get_width()//2, 50))
        sub = font_small.render("a story of moral myopia", True, DARK_GRAY)
        screen.blit(sub, (WIDTH//2 - sub.get_width()//2, 110))
        draw_cactus(screen, WIDTH//2, 260, scale=4)
        self.dlg.draw(screen)

    elif self.state == S_OPENING:
        screen.fill((14, 10, 8))
        draw_arena(screen, "apartment")
        draw_cactus(screen, int(self.px), int(self.py), scale=2)
        self.dlg.draw(screen)

    elif self.state == S_BRIEF:
        screen.fill((5, 5, 15))
        for _ in range(180):
            pygame.draw.rect(screen, (random.randint(18,55),)*3,
                             (random.randint(0,WIDTH), random.randint(0,HEIGHT), 2, 2))
        t = font_large.render(self.level["title"], True, RED)
        screen.blit(t, (WIDTH//2 - t.get_width()//2, 80))
        s = font_medium.render(self.level["subtitle"], True, GRAY)
        screen.blit(s, (WIDTH//2 - s.get_width()//2, 125))
        draw_cactus(screen, WIDTH//2, 290, scale=3)
        self.dlg.draw(screen)

    elif self.state in (S_PLAY, S_OUTRO):
        draw_arena(screen, self.level["arena"])
        for e in self.enemies: e.draw(screen)
        for b in self.bullets: b.draw(screen)
        draw_cactus(screen, int(self.px), int(self.py), scale=2)

        if self.glitch_vig > 0:
            ov = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            ov.fill((120, 0, 180, int(self.glitch_vig * 100)))
            screen.blit(ov, (0, 0))

        draw_insanity_bar(screen, self.insanity)
        kl = font_small.render(f'"HELPED": {self.kills}/{self.level["enemy_count"]}', True, LIGHT_GREEN)
        screen.blit(kl, (WIDTH-230, 14))
        lv = font_small.render(f'{self.level["title"]} — {self.level["subtitle"]}', True, DARK_GRAY)
        screen.blit(lv, (WIDTH//2 - lv.get_width()//2, 14))

        for i, m in enumerate(self.hud_msgs[-4:]):
            a = min(255, m[1]*3)
            surf = font_medium.render(m[0], True, m[2])
            surf.set_alpha(a)
            screen.blit(surf, (WIDTH//2 - surf.get_width()//2, 48+i*28))

        if self.state == S_OUTRO:
            self.dlg.draw(screen, self.glitch_vig)

        ctrl = font_tiny.render("WASD: move  |  CLICK: shoot", True, (48,48,48))
        screen.blit(ctrl, (10, HEIGHT-18))

    elif self.state == S_REWIND:
        draw_arena(screen, self.level["arena"])
        draw_cactus(screen, int(self.px), int(self.py), scale=2)
        self.rewind.draw(screen)

    elif self.state == S_ENDING:
        screen.fill((5, 5, 5))
        for _ in range(2):
            ox, oy = random.randint(-2,2), random.randint(-1,1)
            t = font_medium.render("his hands are red", True, (70, 0, 0))
            screen.blit(t, (WIDTH//2 - t.get_width()//2 + ox, HEIGHT//2 - 130 + oy))
        self.dlg.draw(screen)

    elif self.state == S_CREDITS:
        screen.fill(BLACK)
        items = [
            ("SENIOR CACTUS",     font_large,  GREEN),
            ("an unfinished story", font_medium, GRAY),
            ("",                   font_small,  WHITE),
            ("there was never a Dispatch.", font_small, DARK_GRAY),
            ("there were never any monsters.", font_small, DARK_GRAY),
            ("",                   font_small,  WHITE),
            ("moral myopia.",      font_medium, PURPLE),
            ("",                   font_small,  WHITE),
            ("[ ESC to quit ]",    font_tiny,   DARK_GRAY),
        ]
        y = 150
        for text, font, color in items:
            surf = font.render(text, True, color)
            screen.blit(surf, (WIDTH//2 - surf.get_width()//2, y))
            y += surf.get_height() + 14

    self.rewind.draw(screen)
    pygame.display.flip()
```

def main():
game = Game()
while True:
for event in pygame.event.get():
if event.type == pygame.QUIT:
pygame.quit(); sys.exit()
game.handle_event(event)
game.update()
game.draw()
clock.tick(FPS)

if **name** == “**main**”:
main()
