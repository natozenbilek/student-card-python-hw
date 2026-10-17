# Ödev 2 kontrolü: odev2.py'yi çalıştırır, input() sorularını görevlerde yazan değerlerle cevaplar
# ve her görevin çıktısını beklenen çıktıyla karşılaştırır. 4. ve 5. görevi öteki değerlerle de dener.
# PyCharm'da bu dosyayı açıp Run deyin. odev2.py ile aynı klasörde olmalı. Not vermez, yol gösterir.
import ast
import io
import json
import os
import pathlib
import re
import runpy
import subprocess
import sys
import tokenize

HERE = pathlib.Path(__file__).resolve().parent
ODEV = HERE / "odev2.py"

# Görevlerin "Çalıştırınca şunları yazın" satırlarındaki değerler.
ANSWERS = {
    "1. Öğrenci kartı": ["Mehmet", "BBM"],
    "3. Ağırlıklı puan": ["  fiz127", "3", "2,75"],
    "4. Tek ve çift": ["2026"],
    "5. Geçti mi": ["90", "45"],
    "Meraklısına": ["taş", "makas"],
}
EXPECTED = {
    "1. Öğrenci kartı": ["Adınız: Mehmet", "Bölümünüz: BBM", "*" * 20, "Mehmet, BBM öğrencisi", "*" * 20],
    "2. Kelime sayacı": ["Önce: 8 kelime", "Kalan çift boşluk: 1", "Kalan çift boşluk: 0",
                         "[Python ile ilk programımı yazdım]", "Sonra: 5 kelime"],
    "3. Ağırlıklı puan": ["Ders kodu:   fiz127", "Kredi: 3", "Katsayı: 2,75", "FIZ127: 8.25 puan",
                          "Geçti mi? True", "Katsayı geçerli mi? True"],
    "4. Tek ve çift": ["Bir tam sayı: 2026", "Kalan: 0", "2026 çift"],
    "5. Geçti mi": ["Vize: 90", "Final: 45", "Ortalama: 63", "Kaldı, çünkü final 50'nin altında."],
}
OPTIONAL = {"Meraklısına": ["1. oyuncu: taş", "2. oyuncu: makas", "1. oyuncu kazandı."]}
# Görevlerde yazan öteki çalıştırmalar: (görev, o görevin cevapları, beklenen çıktı).
OTHER_RUNS = [
    ("4. Tek ve çift", ["7"], ["Bir tam sayı: 7", "Kalan: 1", "7 tek"]),
    ("5. Geçti mi", ["30", "70"], ["Vize: 30", "Final: 70", "Ortalama: 54", "Geçti."]),
    ("5. Geçti mi", ["40", "55"], ["Vize: 40", "Final: 55", "Ortalama: 49",
                                   "Kaldı, çünkü ortalama 50'nin altında."]),
]


def child():
    """odev2.py'yi bu süreçte çalıştırır. input() klavyeyi beklemez: o anki görevin sıradaki cevabını
    verir ve Run penceresindeki gibi soruyla cevabı aynı satıra yazar."""
    import builtins
    answers = json.loads(sys.stdin.read())
    sizes = {title: len(values) for title, values in answers.items()}
    real = sys.stdout
    written = []

    class Screen:
        def write(self, text):
            written.append(text)
            return real.write(text)

        def __getattr__(self, name):
            return getattr(real, name)

    def answer(prompt=""):
        heads = re.findall(r"^=== (.+) ===$", "".join(written), re.M)
        title = heads[-1] if heads else "dosyanın başı"
        left = answers.get(title, [])
        if not left:
            print(prompt)
            raise EOFError(f"kontrol.py '{title}' kısmında {sizes.get(title, 0)} input() bekliyordu, "
                           "daha fazlası geldi")
        value = left.pop(0)
        print(f"{prompt}{value}")
        return value

    sys.stdout = Screen()
    builtins.input = answer
    sys.argv = [sys.argv[2]]
    runpy.run_path(sys.argv[0], run_name="__main__")


def sections(text):
    """'=== başlık ===' satırlarına göre çıktıyı böler."""
    out, cur = {}, None
    for line in text.splitlines():
        m = re.fullmatch(r"=== (.+) ===", line.strip())
        if m:
            cur = m.group(1)
            out[cur] = []
        elif cur is not None:
            out[cur].append(line.rstrip())
    return out


TIMEOUT = "odev2.py 20 saniyede bitmedi."


def run(answers):
    """odev2.py'yi verilen cevaplarla çalıştırır: (görevlere bölünmüş çıktı, hata satırı ya da None)."""
    env = dict(os.environ, PYTHONIOENCODING="utf-8", PYTHONUTF8="1")
    try:
        done = subprocess.run([sys.executable, str(pathlib.Path(__file__).resolve()), "--run", str(ODEV)],
                              input=json.dumps(answers), capture_output=True, text=True, encoding="utf-8",
                              errors="replace", timeout=20, cwd=HERE, env=env)
    except subprocess.TimeoutExpired:
        return {}, TIMEOUT
    error = None
    if done.returncode != 0:
        last = [ln for ln in done.stderr.splitlines() if ln.strip()]
        error = last[-1] if last else "(boş)"
    return sections(done.stdout), error


def compare(want, have):
    """İlk farklı satırı anlatan bir not; çıktı aynıysa None."""
    if have == want:
        return None
    for i, w in enumerate(want):
        h = have[i] if i < len(have) else "(satır yok)"
        if h != w:
            return f"{i + 1}. satır beklenen: {w!r}, sizinki: {h!r}"
    return f"beklenenden fazla satır var: {have[len(want)]!r}"


def parts(src):
    """odev2.py'yi görev başlıklarına göre böler. Her görev için: ast düğümleri, koddaki kelimeler
    (if, and, True gibi), comment'ler ve kod satırlarının numaraları."""
    heads = []
    for i, line in enumerate(src.splitlines(), 1):
        m = re.match(r"""\s*print\(\s*["']=== (.+) ===["']\s*\)""", line)
        if m:
            heads.append((m.group(1), i))
    try:
        tree = ast.parse(src)
        tokens = list(tokenize.generate_tokens(io.StringIO(src).readline))
    except (SyntaxError, tokenize.TokenError):
        return {}
    skip = (tokenize.COMMENT, tokenize.NL, tokenize.NEWLINE, tokenize.INDENT, tokenize.DEDENT)
    out = {}
    for k, (title, start) in enumerate(heads):
        end = heads[k + 1][1] - 1 if k + 1 < len(heads) else len(src.splitlines())
        inside = range(start + 1, end + 1)
        out[title] = {
            "nodes": [n for n in ast.walk(tree) if getattr(n, "lineno", 0) in inside],
            "words": {t.string for t in tokens if t.type == tokenize.NAME and t.start[0] in inside},
            "comments": [(t.start[0], t.string) for t in tokens
                         if t.type == tokenize.COMMENT and t.start[0] in inside],
            "rows": sorted({t.start[0] for t in tokens if t.type not in skip and t.start[0] in inside}),
        }
    return out


def name_of(func):
    """f() için 'f', x.f() için 'f'."""
    if isinstance(func, ast.Name):
        return func.id
    if isinstance(func, ast.Attribute):
        return func.attr
    return None


def calls(nodes, name):
    """name() ya da .name() çağrıları."""
    return [n for n in nodes if isinstance(n, ast.Call) and name_of(n.func) == name]


def args_are(call, *values):
    """Çağrının argümanları tam olarak bu sabitler mi?"""
    return [a.value if isinstance(a, ast.Constant) else None for a in call.args] == list(values)


def assigned(nodes, var, func):
    """var = ... func(...) ... biçiminde bir assignment var mı? (int(input()) gibi iç içe de olur.)"""
    for n in nodes:
        if isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id == var for t in n.targets):
            if any(isinstance(c, ast.Call) and name_of(c.func) == func for c in ast.walk(n.value)):
                return True
    return False


def uses(node, var):
    return any(isinstance(n, ast.Name) and n.id == var for n in ast.walk(node))


def const(node):
    return node.value if isinstance(node, ast.Constant) else None


def texts(nodes):
    """Koddaki str sabitleri; f-string'lerde {} içindeki :.2f gibi biçim kısmı hariç."""
    spec = {id(x) for n in nodes if isinstance(n, ast.FormattedValue) and n.format_spec
            for x in ast.walk(n.format_spec)}
    return [n.value for n in nodes if isinstance(n, ast.Constant) and isinstance(n.value, str)
            and id(n) not in spec]


def numbers(nodes):
    return [n.value for n in nodes if isinstance(n, ast.Constant) and type(n.value) in (int, float)]


def own_comments(part, title, given):
    """Öğrencinin kendi kodundan (hazır verilen ilk `given` kod satırından) sonra yazdığı comment'ler."""
    rows = part["rows"][given:]
    if not rows:
        return ""
    ready = {"#", "# TODO", "# Beklenen çıktı:"} | {"# " + line for line in EXPECTED[title]}
    return " ".join(text.lstrip("#").strip() for row, text in part["comments"]
                    if row >= rows[0] and text.strip() not in ready)


def check_1(p, n):
    notes = []
    if not (assigned(n, "name", "input") and assigned(n, "department", "input")):
        notes.append("adı ve bölümü input() ile sorup name ve department variable'larına koyun")
    if any("Mehmet" in t or "BBM" in t for t in texts(n)):
        notes.append("Mehmet'i ve BBM'yi koda yazmayın, ekrana name ve department'tan gelsin")
    if not any(isinstance(b, ast.BinOp) and isinstance(b.op, ast.Add)
               and (uses(b, "name") or uses(b, "department")) for b in n):
        notes.append("ortadaki satırı + ile birleştirin")
    stars = any(isinstance(b, ast.BinOp) and isinstance(b.op, ast.Mult)
                and {const(b.left), const(b.right)} == {"*", 20} for b in n)
    if not stars or any("**" in t for t in texts(n)):
        notes.append('üst ve alt çizgiyi "*" * 20 ile yazdırın, yıldızları tek tek yazmayın')
    return notes


def check_2(p, n):
    notes = []
    if not assigned(n, "text", "strip"):
        notes.append("a) text'i strip() ile temizleyip sonucu yine text'e atayın")
    if not (any(args_are(c, "  ", " ") for c in calls(n, "replace")) and assigned(n, "text", "replace")):
        notes.append('b) çift boşlukları replace("  ", " ") ile tek boşluğa çevirip sonucu yine text\'e atayın')
    spaces = [c for c in calls(n, "count") if args_are(c, " ")]
    doubles = [c for c in calls(n, "count") if args_are(c, "  ")]
    if len(spaces) < 2 or not doubles:
        notes.append('kelimeleri iki seferde de count(" ") ile, kalan çift boşlukları count("  ") ile sayın')
    if any(re.search(r"\d", t) for t in texts(n)):
        notes.append("sayıları elle yazmayın, count() bulsun")
    if len(own_comments(p, "2. Kelime sayacı", given=1)) < 10:
        notes.append("d) tek bir replace()'in neden yetmediğini kodun altına bir comment olarak yazın")
    return notes


def check_3(p, n):
    notes = []
    if not (calls(n, "strip") and calls(n, "upper")):
        notes.append("ders kodunu strip() ve upper() ile temizleyin")
    if not calls(n, "int"):
        notes.append("krediyi int() ile alın")
    if not any(args_are(c, ",", ".") for c in calls(n, "replace")):
        notes.append('katsayıdaki virgülü replace(",", ".") ile noktaya çevirin')
    if not assigned(n, "coefficient", "float"):
        notes.append("katsayıyı float() ile sayıya çevirip coefficient'a koyun")
    if not any(".2f" in t for x in n if isinstance(x, ast.FormattedValue) and x.format_spec
               for t in texts(list(ast.walk(x.format_spec)))):
        notes.append("ağırlıklı puanı bir f-string içinde :.2f ile yazın")
    if not any(isinstance(x, ast.Compare) and 1.75 in numbers(list(ast.walk(x))) for x in n):
        notes.append("dersin geçilip geçilmediğini coefficient'ı 1.75 ile kıyaslayarak bulun")
    if "and" not in p["words"]:
        notes.append("katsayının 0 ile 4 arasında olup olmadığını and ile sınayın")
    if ({"True", "False"} & p["words"] or 8.25 in numbers(n)
            or any(w in t for t in texts(n) for w in ("FIZ127", "8.25", "True"))):
        notes.append("sonuçları elle yazmayın: FIZ127'yi upper(), 8.25'i çarpma, True'ları kıyaslama bulsun")
    return notes


def check_4(p, n):
    notes = []
    if not assigned(n, "number", "int"):
        notes.append("sayıyı input() ile isteyip int() ile number'a koyun")
    if not any(isinstance(b, ast.BinOp) and isinstance(b.op, ast.Mod) and const(b.right) == 2 for b in n):
        notes.append("2'ye bölümünden kalanı % ile bulun")
    if not {"if", "else"} <= p["words"]:
        notes.append("çift mi tek mi olduğuna if ve else ile karar verin")
    return notes


def check_5(p, n):
    notes = []
    if not (assigned(n, "midterm", "int") and assigned(n, "final", "int")):
        notes.append("vize ve final puanlarını int() ile midterm ve final variable'larına koyun")
    if not assigned(n, "average", "round"):
        notes.append("ortalamayı round() ile yuvarlayıp average'a koyun")
    if not {"if", "elif", "else"} <= p["words"]:
        notes.append("üç yoldan birini if, elif ve else ile seçin")
    return notes


CHECKS = {"1. Öğrenci kartı": check_1, "2. Kelime sayacı": check_2, "3. Ağırlıklı puan": check_3,
          "4. Tek ve çift": check_4, "5. Geçti mi": check_5}


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(errors="replace")
    if not ODEV.exists():
        print("odev2.py bulunamadı. kontrol.py ile aynı klasöre koyun.")
        return
    got, error = run(ANSWERS)
    if error == TIMEOUT:
        print(TIMEOUT, "Dosyayı Run ile çalıştırıp nerede takıldığına bakın.")
        return
    if error:
        where = f", '{list(got)[-1]}' görevinde" if got else ""
        print(f"odev2.py çalışırken hata verdi{where}. Error message'ın son satırı:")
        print("   ", error)
        if "kontrol.py" in error:
            print("Her görevin input() satırları kendi başlığının altında olmalı. Görevde yazandan fazla")
            print("input() kullanmayın ve başlıkları yazdıran print() satırlarını silmeyin.")
        print("Önce bu hatayı düzeltin, sonra kontrolü tekrar çalıştırın.")
        return
    others = {}
    for title, values, want in OTHER_RUNS:
        out, err = run({**ANSWERS, title: values})
        others.setdefault(title, []).append((values, want, out.get(title, []), err))
    found = parts(ODEV.read_text(encoding="utf-8"))
    passed = 0
    for title, want in EXPECTED.items():
        have = got.get(title)
        if have is None:
            print(f"✗ {title}: başlık satırı çıktıda yok. Başlığı yazdıran print() satırını silmeyin, "
                  "comment yaptıysanız geri açın.")
            continue
        if not have:
            print(f"✗ {title}: henüz çıktı yok. TODO satırının yerine kodunuzu yazın.")
            continue
        notes = []
        diff = compare(want, have)
        if diff:
            notes.append(diff)
        for values, other_want, other_have, err in others.get(title, []):
            label = " ve ".join(values) + " yazınca"
            if err == TIMEOUT:
                notes.append(f"{label} dosya 20 saniyede bitmedi")
            elif err:
                notes.append(f"{label} hata verdi: {err}")
            elif compare(other_want, other_have):
                notes.append(f"{label}: {compare(other_want, other_have)}")
        part = found.get(title)
        if part:
            notes += CHECKS[title](part, part["nodes"])
            if {"while", "for"} & part["words"]:
                notes.append("while ve for Ders 3'te geliyor, bu ödevde kullanmayın")
        if notes:
            print(f"✗ {title}")
            for note in notes:
                print("    " + note)
        else:
            print(f"✓ {title}")
            passed += 1
    for title, want in OPTIONAL.items():
        have = got.get(title, [])
        if have:
            print(("✓ " if have == want else "· ") + title + " (zorunlu değil)")
    print(f"\n{passed} / {len(EXPECTED)} görev geçti.")


if len(sys.argv) > 2 and sys.argv[1] == "--run":
    child()
else:
    main()
