# importy
import time
import datetime
import random

# počáteční hodnoty
zivoty = 10.0
maximalni_zivoty = 10.0
penize = 200
minimalni_penize = 0
inventar = {"svačina": 1}
cas = datetime.datetime.strptime("08:00", "%H:%M").time()
scena = 7
hra = True
tomkova_body = 0
jirasek_zije = True
# pocatecni hodnoty pro rvacku
rvacka = True
rvacka_zivoty_hrac = 10
rvacka_zivoty_jirasek = 10
rvacka_tah_hrac = True
rvacka_tah_jirasek = False
#pocatecni hodnoty pro obchod
pocet_bonbonu = 0
cena_bonbony = 60
cena_premium_toasty = 80
cena_zbran = 500

# definice vsech potrebnych itemu
krabicove_vino = "krabicové víno"
svacina = "svačina"
bonbony = "bonbony"
premium_toasty = "premium toasty"
zbran = "zbraň"
srdce_tomkove = "srdce paní profesorky"

# změna životů, aby nepřesáhly maximální hodnotu
def zmen_zivoty(hodnota_zivotu):
    global zivoty, maximalni_zivoty
    zivoty += hodnota_zivotu
    if zivoty <= 0:
        if srdce_tomkove in inventar:
            print("Těsně jsi unikl smrti. Naštěstí tě zachránilo srdce Tomkové, stejně jako Tomková\n" \
            "zachraňuje každou středu svou dvouhodinovkou. Nyní máš 0.5 životů.")
            zmen_item(srdce_tomkove, -1)
            zivoty = 0.5
        else:
            konec_hry()
            
    zivoty = min(zivoty, maximalni_zivoty)

# změna peněz, aby nepřesáhly minimální hodnotu
def zmen_penize(hodnota_penez):
    global penize, minimalni_penize
    penize += hodnota_penez
    penize = max(penize, minimalni_penize)

# změna itemů z listu
def zmen_item(item, zmena_itemu):
    if item in inventar:
        inventar[item] += int(zmena_itemu)
        if inventar[item] <= 0:
            del inventar[item]
    elif zmena_itemu > 0:
        inventar[item] = int(zmena_itemu)

# výčet inventáře
def vycet_inventare():
    for item, pocet in inventar.items():
                    print(str(item.capitalize()) + " (x" + str(pocet) + "), ", end="") 

# defaultní menu, včetně inputů a interakcí se staty a inventářem
def menu():
    global zivoty, penize, inventar, cas
    print("-----------------------------------------")
    print(f"Aktuálně je: {cas}\nŽivoty: {zivoty} \nPeníze: {penize}")
    if len(inventar) >= 1:
        vycet_inventare()
        print() 
    else:
        print("Inventář je prázdný")
    print("-----------------------------------------")
    print("Pokračovat v příběhu - 1.")
    print("Interakce s inventářem - 2.")
    print("Ukončit hru - 3.")
    print("-----------------------------------------")
    vstup = input(">")
    print("-----------------------------------------")
    return vstup

# obchod, který je průběžně dostupný
def obchod():
    while True:
        global penize, inventar, vstup_obchod, cena_bonbony, cena_premium_toasty, cena_zbran, pocet_bonbonu
        print("-----------------------------------------")
        print("             REFRESH BISTRO")
        print("-----------------------------------------")
        print(f"1. Premium Toast - {cena_premium_toasty} ")
        print(f"2. Bonbón - {cena_bonbony}")
        print(f"3. Zbraň - {cena_zbran}")
        print("4. Informace o předmětech")
        print("5. Zpět do hry")
        print("-----------------------------------------")
        vstup_obchod = input(">")
        print("-----------------------------------------")
        if vstup_obchod == "1":
            if penize >= cena_premium_toasty:
                zmen_penize(-cena_premium_toasty)
                zmen_item("Premium Toast" , +1)
                print("Úspěšně jsi získal Premium Toast.")
                cena_premium_toasty += 15
            else:
                print("Nemáš dostatek peněz na Premium Toast.")
        elif vstup_obchod == "2":
            if penize >= cena_bonbony and pocet_bonbonu < 3:
                zmen_penize(-cena_bonbony)
                zmen_item("Bonbóny" , +1)
                print("Úspěšně jsi získal bonbóny.")
                cena_bonbony += 40
                pocet_bonbonu += 1
            elif pocet_bonbonu >= 3 and penize >= cena_bonbony:
                    print("Nelze koupit víc bonbónů.")
            else:
                print("Nemáš dostatek peněz na bonbóny.")
        elif vstup_obchod == "3":
            if penize >= cena_zbran:
                zmen_penize(-cena_zbran)
                zmen_item("Zbraň" , +1)
                print("Úspěšně jsi získal zbraň.")
            else:
                print("Nemáš dostatek peněz na zbraň.")
        elif vstup_obchod == "4":
            print("Premium Toast - Základní potravina. Doplní 2 životy.")
            print("Bonbóny - výborné na uplácení - zvyšují všechny šance v příběhu o zhruba 10%.\n" \
            "Lze zakoupit víckrát pro ještě větší zvýšení šancí.")
            print("Standardní pistole s malorážkou. Ideální na Židáska.")
        elif vstup_obchod == "5":
            break
        else:
            print("Neplatný vstup.")

# dialog s koncem hry, druh konce asi podle boolean
def konec_hry():
    global hra
    print("teď to fakt psát nebudu")
    hra = False

# generování šancí
def sance(sance_zakladni):
    global pocet_bonbonu
    return random.random() <= sance_zakladni + pocet_bonbonu * 0.1


# úvodní scéna s krátkým tutoriálem mimo hlavní smyčku
print()
print()
print("         SKORO PĚT NOCÍ S TOMKOVOU, ANEB VÝLET DO ÚSTÍ")
print()
print("Pokud jsi zapnul tento simulátor existenční krize v podobě")
print("textové adventure hry, rozhodně nebudeš zklamaný. Čeká tě")
print("pět dnů a čtyři noci pekla s jediným cílem - PŘEŽIJ. ")
print()
print("Pod sebou vidíš primitivní herní menu, které uvidíš mezi")
print("každou scénou. Na tomto menu můžeš vidět tři jednoduché")
print("sekce - životy, peníze a inventář. Pamatuj, že 10 je ")
print("maximální hodnota tvých životů a jakékoliv životy navíc")
print("se smažou. S některými předměty v tvém inventáři můžeš reagovat,")
print("ale jen mezi scénami. Na začátek jsi od maminky")
print("dostal svačinu, která ti přidá 2.5 životů. Během hry se ti")
print("také bude nepravidelně zobrazovat obchod, ve kterém se převážně")
print("kvůli Fialovi postupně zvyšují ceny.")
print("-----------------------------------------")
print("                    HODNĚ ŠTĚSTÍ")

# hlavní smyčka
while hra:
    # definice vstupu
    vstup = menu()

    # prohrávající conditions
    if vstup == "3":
      hra = False

    # interakce s inventářem
    elif vstup == "2":
        if len(inventar) < 1:
            print("Tvůj inventář je prázdný.")
        else:
            print("Se kterým z těchto předmětů si přeješ interagovat?")
            print("-----------------------------------------")
            inventar_list = list(inventar.keys())
            for index, item in enumerate(inventar_list, start=1):
                print(f"{index} - {item.capitalize()} (x{inventar[item]})")
            print("-----------------------------------------")
            vstup_item = input(">")
            print("-----------------------------------------")

            if vstup_item.isdigit():
                index = int(vstup_item)
                if index in range(1, len(inventar_list) + 1):
                    zvoleny_item = inventar_list[index - 1]
                    if zvoleny_item in inventar:
                        if zvoleny_item == "svačina":
                            print("Chcete zkonzumovat svoji svačinu a přidat si 2.5 životů? y/n")
                            print("-----------------------------------------")
                            rozhodnuti_svacina = input(">")
                            print("-----------------------------------------")
                            if rozhodnuti_svacina == "y":
                                zmen_zivoty(2.5)
                                zmen_item(svacina, -1)
                                print(f"Úspěšně jste snědli svoji svačinu. Nyní máte {zivoty} životů.")
                            elif rozhodnuti_svacina == "n":
                                print(f"Rozhodli jste nesníst svoji svačinu a ponechat si svých {zivoty} životů.")
                        elif zvoleny_item == "krabicové víno":
                            print("S vínem prozatím nelze interagovat. Jeho čas ovšem přijde.")
                else:
                    print("-----------------------------------------")
                    print("Daný předmět se ve vašem inventáři nenachází.")

    # scény
    elif vstup == "1":
        if scena == 0:
            print("Je pondělí, osm hodin ráno. Přicházíš na slavné parkoviště\n" \
            "před školou, ale zjistil jsi nečekanou novinku. Všem, kromě tebe se\n" \
            "porařilo z výletu nějak vymluvit. František je na Šumavě, Matouš s\n" \
            "ním a dokonce i Štěpán má něco lepšího na práci. Ale teď už je pozdě.\n" \
            "Na výlet se musíš vydat pouze ty, Tomková, Burgetová, ale naštěstí i \n" \
            "Slačík, který je mimochodem zase zlitej pod obraz. Snad nebude řídit.\n" \
            "Tomková svým obřím zadkem zabrala všechna volná místa v autobuse, takže\n" \
            "si musíš sednout vedle někoho.")
            print("-----------------------------------------")
            print("Posadit se vedle Slačíka - 1.")
            print("Posadit se vedle Tomkový - 2.")
            print("Posadit se vedle Burgetový - 3.")
            print("-----------------------------------------")
            rozhodnuti_0 = input(">")
            print("-----------------------------------------")
            if rozhodnuti_0 == "1":
                print("Slačík s tebou soucítí a proto ti předal jeho cenné krabicové\n"
                "víno poznání, má ho totiž ještě do zásoby spoustu. Tímto vínem se dokážeš\n"
                "opít tak efektivně, že když se tě někdo bude dožadovat nějaké znalostní otázky,\n"
                " budeš vždycky vědět správnou odpověď. Taky ti dal dvacku ze své peněženky.\n")
                zmen_item(krabicove_vino, +1)
                zmen_penize(20)
            elif rozhodnuti_0 == "2":
                if "svačina" in inventar:
                   print("Co sis jako kurva myslel? Máš štěstí, že jsi u sebe pořád měl\n" \
                   "tu svačinu, kterou jsi mohl Tomkovou uplatit, jinak by tě asi rozsedla.")
                   zmen_item(svacina, -1)
                else:
                    print("Tak to byl hodně dementní nápad. Protože jsi svoji svačinu už snědl,\n" \
                    "Tomková se nasrala, že pro ni nic nemáš a sedla si na tebe. Přicházíš o 4 životy.")
                    zmen_zivoty(-4)
            elif rozhodnuti_0 == "3":
                print("Ze všech možností si vybereš tuhle? Na to bych se ani já necejtil... \n" \
                "A Burgetová se taky necejtí. Přicházíš o dva životy.")
                zmen_zivoty(-2)
            else:
                print("Neplatný vstup.")
            scena += 1
        elif scena == 1:
            print("Tvojí záchranou bylo, že vzhledem k tomu, že škola zarezervovala pokoje pro třicet\n" \
            "lidí (a jednu Tomkovou), bylo místa dost a nejen, že spíš sám, ale také dostatečně daleko od Burgetové.")
            scena += 1
        elif scena == 2:
            print("Z pokoje už jsi do večera radši nevyšel. Nechtěl jsi riskovat interakce s místními obyvateli.\n" \
            "Spalo se ti skvěle, když v tom najednou, někdo začal klepat na tvé zamčené dveře\n" \
            "se slovy: 'Bububu, mám rád malé děti!'. Co to mohlo být? Byla to Tomková, která\n" \
            "zrovna jen projevovala svoje chutě, nebo snad Slačík, který to myslel naprosto vážně?")
            print("-----------------------------------------")
            print("Nechat to být - 1.")
            print("Nahlédnout za dveře - 2.")
            print("-----------------------------------------")
            while True:
                rozhodnuti_2 = input(">")
                print("-----------------------------------------")
                if rozhodnuti_2 == "1":
                    print("Pokusil jsi se usnout, ale jednoduše to nejde. Klepání pokračuje.")
                    print("-----------------------------------------")
                    print("Nechat to být - 1.")
                    print("Nahlédnout za dveře - 2.")
                    print("-----------------------------------------")
                    continue
                elif rozhodnuti_2 == "2":
                    print("Nahlédl jsi za dveře a záhada se okamžitě vyřešila. 'Mohl bys\n" \
                    "toho nechat?' ozvalo se. Ten zasranej zeměpisář se nasere fakt všude.\n" \
                    "Vůbec nevíš proč, ale očividně mu vadí nějaký tvůj hluk. Nejspíš jsi chrápal.\n" \
                    "Každopádně se ho potřebuješ zbavit.")
                    print("-----------------------------------------")
                    print("Mile mu vzkázat, ať se odebere ke spánku - 1.")
                    print("Začít ho finančně vydírat - 2.")
                    print("-----------------------------------------")
                    rozhodnuti_zidasek = input(">")
                    print("-----------------------------------------")
                    if rozhodnuti_zidasek == "1":
                        if sance(0.3):
                            print("Z nějakýho důvodu tohle zafungovalo. Utekl tak rychle, že mu z kapsy\n" \
                            "ještě vypadla dvacetikorunovka. Snad bude víc...")
                            zmen_penize(+20)
                        else:
                            print("To bylo hodně naivní. Po krátké a nepřehledné hádce jsi zjistil, že\n" \
                            "Židásek sice odešel, z peněženky ti ale zmizelo 20 korun. V Ústí je tohle\n" \
                            "na denním i nočním pořádku.")
                            zmen_penize(-20)
                    elif rozhodnuti_zidasek == "2":
                        print("To nebyl zas tak hloupý nápad. Je to přece žid, peněz na to, aby tě\n" \
                        "uplatil, musí mít logicky dost, to je jasný. Má pro tebe nabídku - 100 korun\n" \
                        "za to, že se budeš do rána snažit bejt zticha.")
                        print("-----------------------------------------")
                        print("Přijmout nabídku - 1.")
                        print("Říct si o víc - 2.")
                        print("-----------------------------------------")
                        rozhodnuti_zidasek_vydirani = input(">")
                        if rozhodnuti_zidasek_vydirani == "1": 
                            zmen_penize(+100)
                            print("Přijmul jsi Jiráskovu nabídku a získal jsi 100 korun.\n" \
                            "Docela jednoduše vydělané peníze.")
                        elif rozhodnuti_zidasek_vydirani == "2":
                            zidasek_vydirani_random = random.randint(1,2)
                            if zidasek_vydirani_random == 1:
                                print("On má opravdu peněz na rozdávání. Povedlo se ti vyhádat\n" \
                                "200 korun.")
                                zmen_penize(+200)
                            else:
                                print("To bylo hodně naivní. Po krátké a nepřehledné hádce jsi zjistil, že\n" \
                            "Židásek sice odešel, z peněženky ti ale zmizelo 20 korun a dohoda s Jiráskem nikde. V Ústí je tohle ale\n" \
                            "na denním i nočním pořádku.")
                                zmen_penize(-20)
                        else:
                            print("Neplatný vstup.")
                    else:
                        print("Neplatný vstup.")
                else:
                    print("Neplatný vstup.")
                break
            scena +=1

        elif scena == 3:
            print("Po nočním útoku na soukromé vlastnictví jsi v pořádku přežil\n" \
            "zbytek noci, ale ráno toho možná začínáš litovat. Venku lije jak Slačík po ránu\n" \
            "a tak to vypadá, že budeš celý den zaseklý na ubytovně s našimi Třemi mušketýry.\n" \
            "S nekonečným nic-neděláním má Tomková bohaté zkušenosti, tudíž se programu na dnešek\n" \
            "ujala ona.")
            print()
            print("Krátce po přestávce na ranní hygienu ale začíná docházet na nejhorší.\n" \
            "Tomková dostala hlad. Výjimečně jsi se od ní ovšem dozvěděl, co máš udělat,\n" \
            " žádná hitparáda to ale nebude. Poslala tě pro snídani z místní benzínky, kterou\n" \
            "kupodivu ještě nerozkradli.")
            obchod()
            scena += 1
        elif scena == 4:
            if svacina in inventar or premium_toasty in inventar:
                if premium_toasty in inventar:
                    zmen_item(premium_toasty, -1)
                    print("Výborně. Tomková byla nadšená z toastů a jako odměnu ti ještě něco přispěla zpátky.")
                    zmen_penize(110)
                    zmen_zivoty(0.7)
                else:
                    print("To bylo těsné, ještě že jsi pořád měl tu svačinu z Prahy a mohl jsi jí ji podstrčit.\n" \
                    "Možná by přece jenom bylo chytřejší něco koupit.")
                    zmen_item(svacina, -1)
            else:
                print("Proč jsi jí kurva něco nekoupil? Teď bude sakra těžký s ní přežít. Ještě jsi ji musel uplatit,\n" \
                "aby tě přímo nezabila.")
                zmen_zivoty(-3)
                zmen_penize(-60)
        elif scena == 5:
            print("Odpoledne se situace moc neposunula. Pořád a pořád pršelo, Slačík dává už šestou zelenou\n" \
            "a Tomková zase začala vymýšlet. Bohužel má ale připravenou závěrečný přepadový test jen pro tercii,\n" \
            "jelikož s vaší třídou ji to prostě nebaví a tak budeš muset vymyslet krátký test. První si ale\n" \
            "Tomková prověří tvoje hluboké znalosti.")
            print("-----------------------------------------")
            print("Pověz mi, v jakém roce zavedla Marie Terezie povinnou školní docházku?")
            print("1. - 1774 ")
            print("2. - 1775")
            print("3. - 1780")
            print("-----------------------------------------")
            tomkova_terezie = input(">")
            print("-----------------------------------------")
            if tomkova_terezie == ("1"):
                tomkova_body +=1
            print("-----------------------------------------")
            print("Pověz mi, v jakém roce byla zrušena nevolnictví?")
            print("1. - 1786 ")
            print("2. - 1781")
            print("3. - 1780")
            print("-----------------------------------------")
            tomkova_nevolnictvi = input(">")
            print("-----------------------------------------")
            if tomkova_nevolnictvi == ("2"):
                tomkova_body +=1
            print("Pověz mi, v jakém roce zemřela Marie Terezie?")
            print("1. - 1780 ")
            print("2. - 1787")
            print("3. - 1786")
            print("-----------------------------------------")
            tomkova_terezie_zemrela = input(">")
            print("-----------------------------------------")
            if tomkova_terezie_zemrela == ("1"):
                tomkova_body +=1
            if tomkova_body == 0:
                print("Tomková byla zklamaná, že jsi se vůbec nepřipravil. Přicházíš o 4 životy.")
                zivoty -= 4
            elif tomkova_body == 1:
                print("Tomková byla zklamaná a v Praze tě hned pošle do zadní lavice. Přicházíš o 2 životy.")
                zivoty -= 2
            elif tomkova_body == 2:
                print("Solidní výkon, Tomková byla spokojená a nechala tě vytvořit test pro terciány.\
                      Ten jsi jim následně přeprodal a vydělal jsi si 135 peněz.")
                zmen_penize(135)
            elif tomkova_body ==3:
                print("Tomková je naprosto unešená. Bohužel jen obrazně. Nechala tě vytvořit\n" \
                "test pro terciány a jako pochvalu za tento úchvatný výkon ti dala dar. Nedala ti\n" \
                "nic jiného, než její srdce, které už nechtěla mít na správném místě. Toto srdce ti slouží\n" \
                "jako záložní život, který, pokud dojde na nejhorší a měl by jsi umřít tě zachrání a tvoje\n" \
                "životy se místo hodnoty 0 zastaví na hodnotě 0.5.")
                zmen_item(srdce_tomkove, +1)
            scena += 1
        elif scena == 6:
            print("Aktivita kvízu zabrala celé odpoledne a tak už jsi se neodvážel nic udělat. Pokojně\n" \
            "usínáš a doufáš, že přes noc přestane pršet, protože další takto intimní den s Tomkovou\n" \
            "by jsi nepřežil. ")
            scena += 1
        elif scena == 7:
            print("Probudil tě nepříliž výrazný zvuk kroků z chodby. Na tom by nebylo nic zvláštního, ale\n" \
            "všiml sis, že jsou otevřené dveře tvého pokoje. To je sice zvláštní, ale zkusil jsi to ignorovat\n" \
            "a dveře jsi zavřel. Když najednou, po prudkém zabouchnutí dveří, se ozvalo: 'Můžeš přestat mlátit\n" \
            "těma dveřma? Ty zvuky jsou nepříjemné!'. No jasně, že tě to nenapadlo. Ten žid se tě pokusil okrást\n" \
            "znova! Tentokrát už si to ale líbit nenecháš. Je třeba tomu hajzlovi domluvit, že tě má v noci nechat. ")
            print("-----------------------------------------")
            rvacka = True 
            rvacka_zivoty_hrac = 10
            rvacka_zivoty_jirasek = 10
            rvacka_tah_hrac = True
            rvacka_tah_jirasek = False
            odlakano_special_outcome = False
            while rvacka:
                    if rvacka_tah_hrac:
                        print("            RVAČKA S JIRÁSKEM")
                        print("-----------------------------------------")
                        print(f"Tvoje životy - {rvacka_zivoty_hrac}")
                        print(f"Jiráskovy životy - {rvacka_zivoty_jirasek}")
                        print("-----------------------------------------")
                        print("                Útočíš!")
                        print("-----------------------------------------")
                        print("1. Hodit po Jiráskovi ředkvičku")
                        print("2. Přiškrtit Jiráska drátovou myší")
                        print("3. Odlákat Jiráska desetikorunou")
                        print("-----------------------------------------")
                        rvacka_vstup = input(">")
                        print("-----------------------------------------")
                        if rvacka_vstup == "1":
                            if sance(0.65):
                                print("Výborná práce. Jirásek nestihl uhnout a dostal 3 poškození.")
                                rvacka_zivoty_jirasek -= 3
                            else:
                                print("To se moc nepovedlo. Netrefil jsi se, asi nemáš mušku z bridže.")
                            rvacka_tah_hrac = False
                            rvacka_tah_jirasek = True
                        elif rvacka_vstup == "2":
                            if sance(0.3):
                                print("Tohle byla skvělá technika. Jirásek se dusí a ztrácí 6 životů.\n" \
                                "Ještě k tomu můžeš útočit znovu.")
                                rvacka_zivoty_jirasek -= 6
                            else:
                                print("To se moc nepovedlo. Jirásek tě chytil za ruku a uštědřil ti 4 poškození.")
                                rvacka_zivoty_hrac -= 4
                                rvacka_tah_hrac = False
                                rvacka_tah_jirasek = True
                        elif rvacka_vstup == "3":
                            if penize >=10:
                                zmen_penize(-10)
                                if sance(0.2):
                                    odlakano_special_outcome = True
                                    rvacka = False
                                else:
                                    print("Tohle bylo úplně k ničemu. Pod vlivem adrenalinu asi Židáska\n" \
                                    "peníze tolik nezajímají.")
                                    rvacka_tah_hrac = False
                                    rvacka_tah_jirasek = True
                            else:
                                print("Ještě, kdyby jsi tu desetikorunu měl. Takhle ho sotva odlákáš.")
                                rvacka_tah_hrac = False 
                                rvacka_tah_jirasek = True
                        else:
                            print("Neplatný vstup.")
                            continue 

                        if rvacka_zivoty_jirasek <= 0 or rvacka_zivoty_hrac <= 0:
                            rvacka = False 
                        
                        if not rvacka: 
                            continue 
                    if rvacka_tah_jirasek:
                        print("             RVAČKA S JIRÁSKEM")
                        print("-----------------------------------------")
                        print(f"Tvoje životy - {rvacka_zivoty_hrac}")
                        print(f"Jiráskovy životy - {rvacka_zivoty_jirasek}")
                        print("-----------------------------------------")
                        print("             Útočí Jirásek!     ")
                        print("-----------------------------------------")
                        
                        if sance(0.5): 
                            print("Jirásek vytáhl svoji píšťalku! Zacpal si uši a je připraven k písknutí!")
                            print("-----------------------------------------")
                            print("1. Taky si zacpat uši a doufat")
                            print("2. Spustit Šalom Chaverim a pokusit se ho překřičet")
                            print("-----------------------------------------")
                            jirasek_utok_pistalka_vstup = input(">")
                            print("-----------------------------------------")
                            if jirasek_utok_pistalka_vstup == "1":
                                if sance(0.5):
                                    print("Perfektní. Útok jsi úplně odrazil.")
                                else:
                                    print("Doufal jsi zbytečně. Jiráska lze těžko přemoct v zacpávání uší.\n" \
                                    "Přicházíš o tři životy.")
                                    rvacka_zivoty_hrac -= 3
                            elif jirasek_utok_pistalka_vstup == "2":
                                if sance(0.25):
                                    print("Fantastický nápad. Z ničeho nic se zjevila postava připomínající\n" \
                                    "svou siluetou Sebastiana Skopového a po Židáskovi se málem slehla zem.\n" \
                                    "Záhadná postava ti také za tvůj výkon přispěla 100 penězi.")
                                    rvacka_zivoty_jirasek -= 7
                                    zmen_penize(100)
                                else:
                                    print("To byl hodně stupidní nápad. Co sis myslel? Že se Židásek lekne?\n" \
                                    "Přicházíš o 3 životy.")
                                    rvacka_zivoty_hrac -= 3
                            else:
                                print("Neplatný vstup.") 
                        else:
                            print("Židásek se rozhodl, že zavolá Burgetovou, ať se na to přijde podívat.\n" \
                            "Únik před jejím smradem byl nevyhnutelný. Přicházíš o 2 životy." )
                            rvacka_zivoty_hrac -= 2                       
                        rvacka_tah_jirasek = False
                        rvacka_tah_hrac = True
                        if rvacka_zivoty_jirasek <= 0 or rvacka_zivoty_hrac <= 0:
                            rvacka = False           
            if odlakano_special_outcome:
                print("Skvělá taktika. Židásek ti perfektně skočil na lep a po zbytek noci tě přestal\n" \
                      "otravovat. Zbytek noci se ti spalo perfektně.")
                scena += 1
            elif rvacka_zivoty_hrac <=0:
                print("Celou bitvu s Jiráskem jsi prohrál. Sice tě nechal až do rána spát,\n" \
                "nemohl jsi ovšem nic dělat s tím, že ti při jeho noční akci ukradl z pěněžěnky\n" \
                "200 peněz.")
                zmen_penize(-200)
                scena += 1
            elif rvacka_zivoty_jirasek <=0: 
                print("Po tomto epickém souboji se ti podařilo Jiráskův útok odrazit. Odešel\n" \
                "naprosto zdrcený a ještě ti zaplatil 200 za cenu toho, že ho už mlátit\n" \
                "nebudeš. Následně jsi celou noc spal v pořádku.")
                zmen_penize(200)
                scena += 1
                       
        elif scena == 8:
            print("osma scena")

    else:
        print("Neplatný vstup.")
