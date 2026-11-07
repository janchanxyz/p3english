#!/usr/bin/env python3
"""Add grammatically correct example + exampleZh; copy images from P4 overlap.

LEVEL is set per project. Templates are short, natural HK/British English for kids.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "src" / "words-data.json"
P4 = Path("/workspace/p4english/src/words-data.json")
LEVEL = "P3"

# Word-specific overrides (grammar-checked). Kept small; P4 reuse covers most overlap.
HAND = {
  "a": ("I see a bird in the tree.", "我喺樹上見到一隻鳥。"),
  "an": ("She eats an apple every day.", "佢每日食一個蘋果。"),
  "apple": ("I eat an apple after lunch.", "食完午飯我食一個蘋果。"),
  "egg": ("I boil an egg for breakfast.", "我早餐烚一個蛋。"),
  "orange": ("The orange is sweet and juicy.", "呢個橙又甜又多汁。"),
  "umbrella": ("Take an umbrella when it rains.", "落雨要帶遮。"),
  "icecream": ("I like ice cream on a hot day.", "熱天我鍾意食雪糕。"),
  "uniform": ("We wear a uniform to school.", "我哋穿校服返學。"),
  "hour": ("There is an hour left before dinner.", "距離晚飯重有一個鐘。"),
  "honest": ("An honest friend tells the truth.", "誠實嘅朋友會講真話。"),
  "insect": ("The insect is small and colourful.", "呢隻昆蟲又細又鮮艷。"),
  "octopus": ("The octopus has eight arms.", "章魚有八隻手臂。"),
  "tooth": ("My tooth hurts today.", "我今日牙痛。"),
  "mouth": ("I rinse my mouth after eating.", "食完嘢之後我會漱口。"),
  "plant": ("We water the plant every day.", "我哋每日都澆呢棵植物。"),
  "lock": ("There is a lock on the door.", "門上面有個鎖。"),
  "fast": ("He is a fast runner.", "佢係一個跑得快嘅跑手。"),
  "basketball": ("We play basketball in the park.", "我哋喺公園打籃球。"),
  "baseball": ("The team plays baseball on Sunday.", "球隊星期日打棒球。"),
  "football": ("We play football after school.", "我哋放學之後踢足球。"),
  "volleyball": ("They play volleyball on the beach.", "佢哋喺沙灘打排球。"),
  "tennis": ("She plays tennis every Saturday.", "佢逢星期六打網球。"),
  "badminton": ("We play badminton in the hall.", "我哋喺禮堂打羽毛球。"),
  "playground": ("I play in the playground.", "我喺遊樂場玩。"),
  "biscuit": ("I like to eat a biscuit with tea.", "我鍾意配茶食一塊餅乾。"),
  "onion": ("We use an onion in cooking.", "我哋煮嘢會用一個洋蔥。"),
  "carrot": ("The rabbit likes to eat a carrot.", "隻兔仔鍾意食一條紅蘿蔔。"),
  "vegetable": ("I eat a vegetable every day.", "我每日都食一樣蔬菜。"),
  "mango": ("I love eating a mango in summer.", "夏天我鍾意食一個芒果。"),
  "oven": ("We bake a cake in the oven.", "我哋用焗爐焗一個蛋糕。"),
  "rainbow": ("We see a rainbow after the rain.", "雨後我哋見到彩虹。"),
  "tiger": ("The tiger is a big animal.", "老虎係一種大型動物。"),
  "today": ("We play football today.", "我哋今日踢足球。"),
  "tomorrow": ("We go to school tomorrow.", "我哋聽日返學。"),
  "yesterday": ("Yesterday we visited the museum.", "尋日我哋參觀博物館。"),
  "ticket": ("I buy a ticket for the train.", "我買一張火車飛。"),
  "teach": ("The teacher will teach us maths.", "老師會教我哋數學。"),
  "jeans": ("My favourite clothes are jeans.", "我最鍾意嘅衫係牛仔褲。"),
  "green": ("My favourite colour is green.", "我最鍾意嘅顏色係綠色。"),
  "yellow": ("A yellow bus stopped at our school.", "黃色巴士喺學校停低。"),
  "blue": ("The sky is blue today.", "今日天空係藍色。"),
  "red": ("She wears a red dress.", "佢着住紅色連身裙。"),
  "black": ("The black cat sits on the wall.", "黑貓坐喺牆上。"),
  "white": ("A white cloud floats in the sky.", "白雲喺天空飄。"),
  "pink": ("The flower is pink and soft.", "呢朵花粉紅色又軟。"),
  "brown": ("The brown dog runs fast.", "啡色嘅狗跑得好快。"),
  "purple": ("She paints a purple butterfly.", "佢畫咗一隻紫色蝴蝶。"),
  "grey": ("The grey elephant is huge.", "灰色大象好大隻。"),
  "colour": ("What is your favourite colour?", "你最鍾意咩顏色？"),
  "cat": ("The cat sleeps on the sofa.", "隻貓喺沙發瞓覺。"),
  "dog": ("My dog likes to play ball.", "我隻狗鍾意玩波。"),
  "bird": ("A bird sings in the morning.", "雀鳥朝早唱歌。"),
  "fish": ("The fish swims in the tank.", "魚喺魚缸游水。"),
  "sun": ("The sun is bright today.", "今日太陽好猛。"),
  "moon": ("The moon is round at night.", "夜晚個月好圓。"),
  "star": ("I see a bright star.", "我見到一粒光猛嘅星。"),
  "bus": ("We go to school by bus.", "我哋搭巴士返學。"),
  "car": ("Dad drives a red car.", "爸爸揸紅色汽車。"),
  "bike": ("I ride my bike in the park.", "我喺公園踩單車。"),
  "boy": ("The boy reads a book.", "個男仔睇緊書。"),
  "girl": ("The girl draws a flower.", "個女仔畫緊一朵花。"),
  "ball": ("We kick the ball outside.", "我哋喺外面踢球。"),
  "book": ("I read a book before bed.", "瞓覺前我睇一本書。"),
  "pen": ("Please pass me a pen.", "請將支筆傳俾我。"),
  "cup": ("She drinks milk from a cup.", "佢用杯飲牛奶。"),
  "box": ("There is a toy in the box.", "盒入面有件玩具。"),
  "key": ("I open the door with a key.", "我用鎖匙開門。"),
  "map": ("We look at a map of Hong Kong.", "我哋睇香港地圖。"),
  "bag": ("My bag is blue and heavy.", "我個袋藍色又重。"),
  "bed": ("I sleep in my bed at night.", "夜晚我喺自己張床瞓。"),
  "door": ("Please close the door quietly.", "請靜靜關門。"),
  "tree": ("A bird sits in the tree.", "隻雀坐喺樹上。"),
  "flower": ("The flower smells sweet.", "呢朵花好香。"),
  "water": ("Please drink some water.", "請飲啲水。"),
  "milk": ("I drink milk every morning.", "我每個朝早飲牛奶。"),
  "rice": ("We eat rice for dinner.", "我哋晚飯食飯。"),
  "soup": ("Mum cooks hot soup for us.", "媽媽煮熱湯俾我哋。"),
  "cake": ("We share a cake at the party.", "派對上我哋分享蛋糕。"),
  "happy": ("I feel happy at school.", "我喺學校好開心。"),
  "sad": ("He looks sad after the game.", "比賽完之後佢好傷心。"),
  "big": ("The elephant is big.", "大象好大隻。"),
  "small": ("The ant is small.", "螞蟻好細。"),
  "hot": ("It is hot in summer.", "夏天好熱。"),
  "cold": ("It is cold in winter.", "冬天好冷。"),
  "run": ("We run in the playground.", "我哋喺遊樂場跑步。"),
  "walk": ("I walk to school with Mum.", "我同媽媽行路返學。"),
  "jump": ("The frog can jump high.", "青蛙跳得好高。"),
  "swim": ("Fish swim in the river.", "魚喺河入面游。"),
  "eat": ("We eat lunch at twelve.", "我哋十二點食午餐。"),
  "drink": ("Please drink your juice.", "請飲你嘅果汁。"),
  "read": ("I read a story every night.", "我每晚睇一個故事。"),
  "write": ("Please write your name clearly.", "請清楚寫低你個名。"),
  "draw": ("I draw a house with crayons.", "我用蠟筆畫間屋。"),
  "sing": ("We sing a song in music class.", "音樂堂我哋唱歌。"),
  "dance": ("The children dance happily.", "小朋友開心咁跳舞。"),
  "play": ("We play games after school.", "放學之後我哋玩遊戲。"),
  "help": ("Please help your classmate.", "請幫吓你同學。"),
  "open": ("Please open the window.", "請開窗。"),
  "close": ("Please close your books.", "請合埋書。"),
  "sleep": ("Babies sleep in the afternoon.", "BB喺晏晝瞓覺。"),
  "wash": ("I wash my hands before lunch.", "食午餐前我會洗手。"),
  "clean": ("We clean the classroom together.", "我哋一齊清潔課室。"),
  "look": ("Look at the rainbow!", "望吓條彩虹！"),
  "listen": ("Please listen to the teacher.", "請聽老師講。"),
  "talk": ("We talk softly in the library.", "圖書館入面我哋細聲傾偈。"),
  "smile": ("She gives me a big smile.", "佢對住我大笑。"),
  "laugh": ("The joke makes us laugh.", "個笑话令我哋大笑。"),
  "cry": ("The baby may cry when hungry.", "BB肚餓可能會喊。"),
  "climb": ("We climb the hill on Sunday.", "星期日我哋爬山。"),
  "throw": ("Throw the ball to your friend.", "將波拋俾你朋友。"),
  "catch": ("I can catch the ball.", "我接得住個波。"),
  "kick": ("We kick the ball when we play soccer.", "我哋踢足球嗰陣會踢球。"),
  "hold": ("Please hold my hand.", "請握住我隻手。"),
  "find": ("I find my book on the shelf.", "我喺書架上搵到我本書。"),
  "come": ("Please come to the front.", "請嚟前面。"),
  "go": ("We go home after school.", "放學之後我哋返屋企。"),
  "stop": ("Please stop at the red light.", "紅燈請停低。"),
  "start": ("We start our lesson at nine.", "我哋九點開始上課。"),
  "make": ("I make a card for Mum.", "我整張卡俾媽媽。"),
  "see": ("I see a boat on the sea.", "我喺海上見到一隻船。"),
  "sit": ("Please sit on the chair.", "請坐喺張椅度。"),
  "stand": ("Please stand in a line.", "請企成一條隊。"),
  "fly": ("Birds fly in the sky.", "雀鳥喺天空飛。"),
  "give": ("Please give me a pencil.", "請俾支鉛筆我。"),
  "take": ("Take your bag with you.", "帶埋你個袋。"),
  "family": ("My family eats dinner together.", "我哋一家人一齊食晚飯。"),
  "father": ("My father reads the newspaper.", "我爸爸睇報紙。"),
  "mother": ("My mother cooks dinner.", "我媽媽煮晚飯。"),
  "brother": ("My brother likes football.", "我弟弟鍾意足球。"),
  "sister": ("My sister draws pretty pictures.", "我妹妹畫靚圖畫。"),
  "friend": ("A good friend shares toys.", "好朋友會分享玩具。"),
  "school": ("Our school is near the park.", "我哋學校喺公園附近。"),
  "teacher": ("Our teacher is kind and funny.", "我哋老師又善良又有趣。"),
  "student": ("Every student has a desk.", "每個學生都有張書檯。"),
  "house": ("Our house has a small garden.", "我哋間屋有個小花園。"),
  "home": ("I feel safe at home.", "喺屋企我感到好安全。"),
}

VOWEL_SOUND = set("aeiou")
# words that take "an" despite consonant letter, or "a" despite vowel letter
AN_EXCEPTIONS = {"hour", "honest", "umbrella", "icecream", "egg", "apple", "orange", "onion", "elephant", "insect", "octopus", "uncle", "aunt", "airplane", "ambulance", "apartment", "adult", "exam", "envelope", "island", "oven", "artist", "actor", "eraser", "answer", "animal", "eagle", "earth", "evening", "office", "engine", "engineer"}
A_EXCEPTIONS = {"university", "uniform", "useful", "one", "European"}  # uniform starts with /ju/


def article_for(word: str) -> str:
    w = word.lower()
    if w in A_EXCEPTIONS:
        return "a"
    if w in AN_EXCEPTIONS or (w and w[0] in VOWEL_SOUND):
        return "an"
    return "a"


def kid_templates(word: str, pos: str, zh: str):
    art = article_for(word)
    if pos == "v":
        return [
            (f"We {word} every day at school.", f"我哋每日喺學校{zh}。"),
            (f"I {word} with my friends.", f"我同朋友一齊{zh}。"),
        ]
    if pos == "adj":
        return [
            (f"The puppy looks {word}.", f"隻小狗睇落好{zh}。"),
            (f"I feel {word} today.", f"我今日感到{zh}。"),
        ]
    # nouns
    return [
        (f"I can see {art} {word}.", f"我見到{zh}。"),
        (f"There is {art} {word} in the picture.", f"圖畫入面有{zh}。"),
        (f"The {word} is in our classroom.", f"呢個{zh}喺我哋課室。"),
    ]


def grammar_touchups(example: str, word: str) -> str:
    e = example.strip()
    e = e.replace("colorful", "colourful").replace("favorite", "favourite")
    e = e.replace("organize", "organise").replace("recognize", "recognise")
    e = e.replace(" math.", " maths.").replace(" math ", " maths ")
    if e and e[0].islower():
        e = e[0].upper() + e[1:]
    if e and e[-1] not in ".!?":
        e += "."
    # a/an auto around the target word when preceded by a/an
    e = re.sub(rf"\ba ({re.escape(word)})\b", lambda m: f"{article_for(word)} {m.group(1)}", e, flags=re.I)
    e = re.sub(rf"\ban ({re.escape(word)})\b", lambda m: f"{article_for(word)} {m.group(1)}", e, flags=re.I)
    if not re.search(rf"\b{re.escape(word)}\b", e, flags=re.I):
        e = f"Today we learned the word {word}."
    return e


def main():
    items = json.loads(DATA.read_text(encoding="utf-8"))
    p4_by = {}
    if P4.exists():
        for x in json.loads(P4.read_text(encoding="utf-8")):
            p4_by[x["word"]] = x

    from_hand = from_p4 = from_tmpl = 0
    for it in items:
        w = it["word"]
        pos = it.get("pos") or "n"
        zh = it.get("zh") or w

        if w in p4_by:
            src = p4_by[w]
            for k in ("imageUrl", "imageCredit", "imageUrls", "imageCredits", "thumbUrl"):
                if src.get(k) and not it.get(k):
                    it[k] = src[k]

        if w in HAND:
            ex, exzh = HAND[w]
            # Special: icecream example uses "ice cream" — ensure word token present for blanking
            if w == "icecream" and "icecream" not in ex.lower().replace(" ", ""):
                ex = "I like icecream on a hot day."
                exzh = "熱天我鍾意食雪糕。"
            from_hand += 1
        elif w in p4_by and p4_by[w].get("example"):
            ex = p4_by[w]["example"]
            exzh = p4_by[w].get("exampleZh") or f"呢個字係「{zh}」。"
            from_p4 += 1
        else:
            opts = kid_templates(w, pos, zh)
            t_en, t_zh = opts[sum(ord(c) for c in w) % len(opts)]
            ex, exzh = t_en, t_zh
            from_tmpl += 1

        it["example"] = grammar_touchups(ex, w)
        if not exzh:
            exzh = f"呢個字係「{zh}」。"
        it["exampleZh"] = exzh

        # sport collocation safety
        if w.endswith("ball") and w != "ball" and "kick" in it["example"].lower() and w != "football":
            it["example"] = f"We play {w} in the park."
            it["exampleZh"] = f"我哋喺公園玩／打{zh}。"

    # Second pass a/an polish + ensure example contains word
    fixes = []
    for it in items:
        w = it["word"]
        orig = it["example"]
        ex = orig
        ex = re.sub(r"\ba ([aeiouAEIOU]\w*)\b", lambda m: f"an {m.group(1)}" if m.group(1).lower() not in A_EXCEPTIONS else f"a {m.group(1)}", ex)
        # undo wrong an for uniform etc.
        for bad in A_EXCEPTIONS:
            ex = re.sub(rf"\ban ({bad})\b", rf"a \1", ex, flags=re.I)
        if not re.search(rf"\b{re.escape(w)}\b", ex, flags=re.I):
            ex = f"Today we learned the word {w}."
            it["exampleZh"] = f"今日我哋學咗「{it['zh']}」呢個字。"
        if ex != orig:
            fixes.append((w, orig, ex))
            it["example"] = ex

    DATA.write_text(json.dumps(items, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    with_img = sum(1 for x in items if x.get("imageUrl"))
    with_ex = sum(1 for x in items if x.get("example") and x.get("exampleZh"))
    print(f"[{LEVEL}] words={len(items)} examples={with_ex} images={with_img}")
    print(f"  hand={from_hand} p4={from_p4} tmpl={from_tmpl} auto_fixes={len(fixes)}")
    report = ROOT / "scripts" / "example-grammar-fix.md"
    lines = [
        f"# Example grammar fix report ({LEVEL})",
        "",
        f"- **Total checked:** {len(items)}",
        f"- **With example+zh:** {with_ex}",
        f"- **Images after P4 reuse:** {with_img}",
        f"- **Sources:** hand={from_hand}, P4 reuse={from_p4}, kid templates={from_tmpl}",
        f"- **Auto a/an / containment fixes:** {len(fixes)}",
        "",
        "## Focus",
        "",
        "- Short natural HK/British English for Primary kids",
        "- Articles (a/an), countable nouns, British spelling (colour/favourite/maths)",
        "- Sport collocations (play basketball, not kick)",
        "- Example sentences always contain the target word (for blanking)",
        "",
    ]
    if fixes:
        lines.append("## Auto fixes (sample)")
        lines.append("")
        for w, a, b in fixes[:40]:
            lines.append(f"- `{w}`: {a!r} → {b!r}")
        lines.append("")
    report.write_text("\n".join(lines), encoding="utf-8")
    print(f"  wrote {report}")

if __name__ == "__main__":
    main()
