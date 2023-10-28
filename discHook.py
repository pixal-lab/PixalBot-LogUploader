from dhooks import Webhook, Embed
from datetime import datetime, timedelta
from collections import defaultdict
import locale
locale.setlocale(locale.LC_TIME, 'es_ES')

nombres = {
    "vg": "Vale Guardian",
    "gors": "Gorseval",
    "sab": "Sabetha",
    "sloth": "Slothason",
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
}

def lunes():
    hoy = datetime.today()
    lunes = hoy - timedelta(days=hoy.weekday())
    return lunes.strftime('%d/%m/%y')

def boss(codigo, success, failure):
    if nombres[codigo] in failure or nombres[codigo] in success:
        wipe = ""
        if nombres[codigo] in failure:
            for f in failure[nombres[codigo]]:
                wipe += " [:x:](" + f[0] + ")"
        y = ""
        if nombres[codigo] in success:
            y =" CM" if success[nombres[codigo]][0][4] else ""
            return "[" + nombres[codigo] + y +"](" + success[nombres[codigo]][0][0] + ")" + wipe
        else:
            return nombres[codigo] + y + wipe
    else:
        return nombres[codigo]

def send(wHook, success, failure, t_runs, times0):
    hook = Webhook(wHook)
    s = ' , '
    embed = Embed(
    title = f'Blue Panda Logs {s.join([t.strftime("%d/%m/%y") for t in times0])}',
    color = 1694948,
    thumbnail_url = "https://img.freepik.com/premium-vector/cute-red-panda-reading-book-cartoon-icon-illustration-animal-education-icon-concept-isolated-flat-cartoon-style_138676-1295.jpg")
    
    
    embed.add_field(
        name = "W1:",
        value = boss("vg") + "\n" + boss("gors") + "\n" + boss("sab"),
        inline = False
    )
    embed.add_field(
        name = "W2:",
        value = boss("sloth") + "\n" + boss("matt"),
        inline = False
    )
    embed.add_field(
        name = "W3:",
        value = boss("kc") + "\n" + boss("xera"),
        inline = False
    )
    embed.add_field(
        name = "W4:",
        value = boss("cairn") + "\n" + boss("mo") + "\n" + boss("sam") + "\n" + boss("dei"),
        inline = False
    )
    embed.add_field(
        name = "W5:",
        value = boss("sh") + "\n" + boss("dhuum"),
        inline = False
    )
    embed.add_field(
        name = "W6:",
        value = boss("ca") + "\n" + boss("twins") + "\n" + boss("qadim"),
        inline = False
    )
    embed.add_field(
        name = "W7:",
        value = boss("adina") + "\n" + boss("sabir") + "\n" + boss("qpeer"),
        inline = False
    )


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
        name = "Wipeos:   " + str(len(failure)) ,
        value = "",
        inline = False
    )
    hook.send(
        embed = embed,
        username = "PixalBot",
        avatar_url = "https://img.freepik.com/vector-premium/cute-red-panda-icon-illustration-estilo-plano-dibujos-animados_138676-1212.jpg?w=826"
    )



    pass



    # Convertir la diferencia de tiempo en formato hhmmss
  