#les from
from urllib.parse import quote_plus
from webbrowser import open_new_tab


def demander_date(question):
    date = input(question)
    while date and (len(date.split("/")) != 3 or not date.replace("/", "").isdigit()):
        date = input("Invalide. (FORMAT: DD/MM/YYYY, Entree pour passer)")

    if date:
        d = date.split("/")
        date = d[2] + "-" + d[1] + "-" + d[0]

    return date



moteurs = ["google", "duckduckgo", "yandex", "twitter", "reddit"]

while True:


    moteur = input("Sur quel moteur? (google / duckduckgo / yandex / twitter / reddit / tous, q pour quitter)").lower()
    while moteur not in moteurs and moteur != "tous" and moteur != "q":
        moteur = input("Invalide. Quel moteur? (google / duckduckgo / yandex / twitter / reddit / tous, q pour quitter)").lower()

    if moteur == "q":
        break

    if moteur == "tous":
        choisis = moteurs
    else:
        choisis = [moteur]

    # les Q communes a tous les moteurs
    mots = input("Quel mot veut tu chercher?")
    variante = input("Une variante? (cherche l'un OU l'autre, Entree pour passer)")
    termeexact = input("Cette liste de caractère précisément? O/N")
    exclure = input("Des mots a exclure? (separes par des espaces)")

    site = ""
    filetype = ""
    intitle = ""
    inurl = ""
    compte = ""
    subreddit = ""
    dated = ""
    datef = ""

    if moteur in ["google", "duckduckgo", "yandex", "tous"]:
        site = input("Un site en particulier?")
        filetype = input("Un type de fichier? pdf, docx, xlsx...")
        intitle = input("Un mot dans le titre de la page?")
        inurl = input("Un mot dans l'adresse de la page?")

    if moteur in ["twitter", "reddit", "tous"]:
        compte = input("Un compte en particulier? (sans @ ni u/, twitter et reddit)")

    if moteur in ["reddit", "tous"]:
        subreddit = input("Un subreddit en particulier? (sans r/)")

    if moteur in ["google", "twitter", "tous"]:
        dated = demander_date("A partir de quelle date? (format DD/MM/YYYY)")
        datef = demander_date("Jusqu'a quelle date? (format DD/MM/YYYY)")

    if termeexact.upper() == "O":
        mots = '"' + mots + '"'
        if variante:
            variante = '"' + variante + '"'

    if variante:
        mots = mots + " OR " + variante

    if exclure:
        exclure = "-" + exclure.replace(" ", " -")

    if site:
        site = "site:" + site

    # yandex n'utilise pas les memes mots que google, on prepare les deux
    mime = ""
    if filetype:
        mime = "mime:" + filetype
        filetype = "filetype:" + filetype

    title = ""
    if intitle:
        title = "title:" + intitle
        intitle = "intitle:" + intitle

    if inurl:
        inurl = "inurl:" + inurl

    # meme compte, mais twitter dit from: et reddit dit author:
    auteur = ""
    if compte:
        auteur = "author:" + compte
        compte = "from:" + compte

    if subreddit:
        subreddit = "subreddit:" + subreddit



    after = ""
    since = ""
    if dated:
        after = "after:" + dated
        since = "since:" + dated

    before = ""
    until = ""
    if datef:
        before = "before:" + datef
        until = "until:" + datef

    # on fait une URL pour chaque moteur de la liste
    for m in choisis:

        if m == "google":
            url = "https://www.google.com/search?q=" + quote_plus(mots + " " + exclure + " " + site + " " + filetype + " " + intitle + " " + inurl + " " + after + " " + before)

        if m == "duckduckgo":
            url = "https://duckduckgo.com/?q=" + quote_plus(mots + " " + exclure + " " + site + " " + filetype + " " + intitle + " " + inurl)

        if m == "yandex":
            # yandex ecrit OR avec une barre |
            url = "https://yandex.com/search/?text=" + quote_plus(mots.replace(" OR ", " | ") + " " + exclure + " " + site + " " + mime + " " + title + " " + inurl)

        if m == "twitter":
            url = "https://x.com/search?q=" + quote_plus(mots + " " + exclure + " " + compte + " " + since + " " + until) + "&f=live"

        if m == "reddit":
            url = "https://www.reddit.com/search/?q=" + quote_plus(mots + " " + auteur + " " + subreddit)

        print(url)
        open_new_tab(url)

    print()