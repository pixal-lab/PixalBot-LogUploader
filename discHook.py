from dhooks import Webhook, Embed
from datetime import datetime, timedelta
from collections import defaultdict
import locale
locale.setlocale(locale.LC_TIME, 'es_ES')

nombres = {
"vg": "Vale Guardian",
"gors": "Gorseval",
"sab": "Sabetha the Saboteur",
"sloth": "Slothasor",
"matt": "Matthias Gabrel",
"kc": "Keep Construct",
"xera": "Xera",
"cairn": "Cairn the Indomitable",
"mo": "Mursaat Overseer",
"sam": "Samarog",
"dei": "Deimos",
"sh": "Soulless Horror",
"dhuum": "Dhuum",
"ca": "Conjured Amalgamate",
"twins": "Twin Largos",
"qadim": "Qadim",
"adina": "Cardinal Adina",
"sabir": "Cardinal Sabir",
"qpeer": "Qadim the Peerless",
"olc": "Old Lion",
"trin": "Captain Mai Trin",
"ankka": "Ankka",
"li": "Minister Li",
"void": "Dragon Void",
"dagda": "Dagda",
"cerus": "Cerus",
"mama"  : "M A M A",
"siax"  : "Siax the Corrupted",
"enso"  : "Ensolyss of the Endless Torment",
"skor"  : "Skorvald the Shattered",
"arriv" : "Artsariiv",
"arkk"  : "Arkk",
"ai"    : "Ai",
"kana"  : "Kanaxai",
}
def get_full_name(ab):
    return nombres[ab]

def wipes_count(failures):
    count = 0
    for i in failures:
        for j in failures[i]:
            if i in nombres.values():
                count += 1
    return count

def check(codigo, success, failure):
    if get_full_name(codigo) in failure or get_full_name(codigo) in success:
        return True
    else:
        return False


def boss(codigo, success, failure):
    if check(codigo, success, failure):
        wipe = ""
        if get_full_name(codigo) in failure and len(failure[get_full_name(codigo)]) > 0:
            for f in failure[get_full_name(codigo)]:
                wipe += " [:x:](" + f.pop(0) + ")"
        y = ""
        if get_full_name(codigo) in success and len(success[get_full_name(codigo)]) > 0:
            y =" CM" if success[get_full_name(codigo)][0][4] else ""
            link = success[get_full_name(codigo)][0][0]
            success[get_full_name(codigo)].pop(0)
            cont = 0
            if codigo == "Ai" and cont == 0:
                cont += 1
                return "[Elemental" + get_full_name(codigo) + y +"](" + link + ")" + wipe
            elif codigo == "Ai" and cont == 1:
                return "[Dark" + get_full_name(codigo) + y +"](" + link + ")" + wipe

            return "[" + get_full_name(codigo) + y +"](" + link + ")" + wipe
        else:
            return get_full_name(codigo) + y + wipe
    else:
        return get_full_name(codigo)

def wing_check(bosses, success, failure):
    check_bosses = []
    for i in bosses:
        check_bosses.append(check(i, success, failure))
    if any(check_bosses):
        return True
    else:
        return False

def wing_field(wing, bosses, success, failure):
        value = ""
        for i in bosses:
            if check(i, success, failure):
                value += boss(i, success, failure) + "\n"
        value = value[:-1]
        return { 
            "name" : wing,
            "value" : value,
            "inline" : False}
    

def send(wHook, success, failure, t_runs, times0):
    wipes = wipes_count(failure)
    hook = Webhook(wHook)
    s = ' , '
    embed = Embed(
    title = f'Red Panda Logs {s.join([t.strftime("%d/%m/%y") for t in times0])}',
    color = 1694948,
    thumbnail_url = "https://img.freepik.com/premium-vector/cute-red-panda-reading-book-cartoon-icon-illustration-animal-education-icon-concept-isolated-flat-cartoon-style_138676-1295.jpg")
    

    if wing_check(["vg", "gors", "sab"],success, failure):
        embed.add_field(**wing_field("W1", ["vg", "gors", "sab"], success, failure))
    if wing_check(["sloth", "matt"],success, failure):
        embed.add_field(**wing_field("W2", ["sloth", "matt"], success, failure))
    if wing_check(["kc", "xera"],success, failure):
        embed.add_field(**wing_field("W3", ["kc", "xera"], success, failure))
    if wing_check(["cairn", "mo", "sam", "dei"],success, failure):
        embed.add_field(**wing_field("W4", ["cairn", "mo", "sam", "dei"], success, failure))
    if wing_check(["sh", "dhuum"],success, failure):
        embed.add_field(**wing_field("W5", ["sh", "dhuum"], success, failure))
    if wing_check(["ca", "twins", "qadim"],success, failure):
        embed.add_field(**wing_field("W6", ["ca", "twins", "qadim"], success, failure))
    if wing_check(["adina", "sabir", "qpeer"],success, failure):
        embed.add_field(**wing_field("W7", ["adina", "sabir", "qpeer"], success, failure))

    if wing_check(["olc", "trin", "ankka", "li", "void"],success, failure):
        embed.add_field(**wing_field("EoD Strikes", ["olc", "trin", "ankka", "li", "void"], success, failure))
        
    if wing_check(["dagda", "cerus"],success, failure):
        embed.add_field(**wing_field("SotO Strikes", ["dagda", "cerus"], success, failure))
    
    if wing_check(["mama", "siax", "enso"],success, failure):
        embed.add_field(**wing_field("Fractal 97", ["mama", "siax", "enso"], success, failure))
    if wing_check(["skor", "arriv", "arkk"],success, failure):
        embed.add_field(**wing_field("Fractal 98", ["skor", "arriv", "arkk"], success, failure))
    if wing_check(["ai"],success, failure):
        embed.add_field(**wing_field("Fractal 99", ["ai", "ai"], success, failure))
    if wing_check(["kana"],success, failure):
        embed.add_field(**wing_field("Fractal 100", ["kana"], success, failure))






    suma = timedelta(seconds=0)
    for i in range(len(t_runs)):
        if t_runs[i] > timedelta(seconds=0):
            suma += t_runs[i]
            embed.add_field(
                name = f"{times0[i].strftime('%A').capitalize()} {times0[i].strftime('%d')}: {t_runs[i].seconds // 3600:02d}h {t_runs[i].seconds % 3600 // 60:02d}m {t_runs[i].seconds % 60:02d}s",
                value = "",
                inline = False
            )
    
    embed.add_field(
        name = f"Suma: {suma.seconds // 3600:02d}h {suma.seconds % 3600 // 60:02d}m {suma.seconds % 60:02d}s",
        value = "",
        inline = False
    )
    embed.add_field(
        name = "Wipeos:   " + str(wipes) ,
        value = "",
        inline = False
    )
    embed.set_footer("Bot by Pixal_ | Pixal.2465")
    hook.send(
        embed = embed,
        username = "PixalBot",
        avatar_url = "https://img.freepik.com/vector-premium/cute-red-panda-icon-illustration-estilo-plano-dibujos-animados_138676-1212.jpg?w=826"
    )
  