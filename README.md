<h1>CTF-VEEBIRAKENDUS<h1>

<h3>Kuidas käivitada<h3>

1. Tõmba see source code alla
2. Installi Python ja Node
3. Tee Client directoryst uus build (npm run build)
4. Installi vajalikud python moodulid (pip install requirements.txt)
5. Jooksuta app (python ./server.py)

<h3>Vulnid<h3>

<h1>Hetke seisuga olemas 5/7 vulni<h1>


<h1>Olemas vulnid:<h1>

1. User regristration vormis on võimalik enumerateda päris palju username ja siis nende logini brute-forceda (meil ainuke bruteforcetav on mingi "banned for weak password" account sest teistel on actually normid paroolid)
   <span style="color: red;">VULN OLEMAS - VAJA AINULT EXPLOITIDA</span>

2. idor abil võimalik lugeda kõikide teiste userite infot (nt mingeid invoice või full-on kontot vahetada)
   <span style="color: red;">VULN OLEMAS</span>

3. JWT token bypass et enableda experimental features (kui oled juba sisse loginud)
   <span style="color: red;">VULN OLEMAS, vaja ainult exploidi peale teha midagi</span>

4. Offerite buyimiseks vajaliku raha valideerimist saab client-sides muuta sest back-end ei kontrolli kui paju raha sul on.
   <span style="color: red;">VULN OLEMAS?</span>

5. Mingis php(?) failis labi get argide teha lfi et lugeda pmst koiki faile mis os-is on (akki teeks seda /private all?)
   VULN ON CONFIRMITUD, ainult vaja teha viis kuidagi user saaks sellest actually teada (scripti prglt muuta ise ei saa)


<h1>Hetkel tulemas vulnid:<h1>

6. XSS vuln offerite rewiedes et saade teiste kasutajate credentiale/muud infot (nt sisselogimiseks mingisse "verified accounti" sest by default pole uutel kontodel voimalik palju teha)
   <span style="color: red;">VULN SEMI-TÖÖTAB AGA EXECUTION POLE SIIAMAANI SUUTNUD</span>




<h1>Mittetehtud vulnid:<h1>

7. SQL injection marketplace offerite VÕI oma purchasite searchimisel

8. /private aladirectory kuhu saab AINULT ligi läbi ssrf vulni (lykkab mingi et lehte ei saa avada sest vale ip). Läbi avatar selection screeni (mille saab läbi jwt vulni) saab bypassida.

*(9 ja 10 personally natuke sus aga pohh)*
9. secret developer panel koos loginiga (mille credentialid on lih indexi htmlis commentina) (paneli saab üles leida kui minna robots.txt)
10. developer portalis võimalik mingeid api keyisi saada või api calle teha mida niisama ei saa?
Või teha siia mingi sql-i kasutav search propmt (search for usernames) aga labi selle voimalik teha vulni nr 2?

11. Võimalik saada code execution (ja läbi selle reverse shell), kui olla sisse logitud ja teha uus marketplace offer, kus pildi asemel laed exetuable scripti ja executid selle
12. (BONUS): pärast reverse shelli on võimalik privescida rootiks
