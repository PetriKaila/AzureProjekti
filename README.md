Azure IoT harjoitustehtävä

Rakensimme iot hubin, jonne saimme dataa rasberry piltä. Rasberryn ohjelma hakee OpenWeatherMap palvelusta Kalajoen lämpötiloja ja tietyin välein niitä putkahtelee sieltä Azureen. Azuren pipeline lähettää tavarat databaseen talteen.

Tehtävämme alkoi ideoinnista, mitä ihmettä me voisimme tehdä. Päädyimme tutkailemaan erilaisia tapoja saada lämpötiladataa, sillä meitä nyt sattuu Kalajoen sää kiinnostamaan. Tämän jälkeen huomasimme myös opettajamme käsittelevän lämpötiladataa, mikä hivenen auttoi meitä eteenpäin rakentamaan pipelineamme.

Tehtävää tehdessämme monet kerrat olemme nettiä selailleet apuja etsien. Eihän meillä heti alkuun ollut edes tiedossa, kuinka saamme dataa edes kerättyä. Kokeilimme alkuun jopa puhelinta käyttää mittalaitteena, mutta kun se ei onnistunutkaan, päädyimme käyttämään OpenWeatherMapin tarjoamaa API palvelua. Siellä voi rakentaa APIn joka tarjoaa projektiin tarvittavat datat. Me valitsimme lämpötilan.

Vaikka olemme tietotekniikan opiskelijoita, ei meillä ole vielä ollenkaan ollut Python-koodausta, mutta tässä APIn kanssa Python-ohjelma tuntui olevan paras vaihtoehto kerätä dataa. Näin tuli opittua vähän lisää uudesta ja kurssin ulkopuolisesta asiasta.

Netistä saaduilla ohjeilla ja tiedosto rungoilla saimme tehtyä toimivan python koodin, millä saamme OpenWeatherMapista kerättyä dataa rasberrylle. OpenWeatherMap tarjoaa tähän tarkoitukseen sopivan APIn. Sieltä pystyimme valitsemaan paikaksi Kalajoen, joten nyt saamme Kalajoen lämpötiladataa.

![Kuva1](F:\petri\Pictures\Kuva1.png)

Tarvittiin kyllä paljon verta hikeä ja kyyneliä, jotta saimme Python ohjelman toimimaan haluamallamme tavalla.

Rasberryä käytämme välissä siksi, koska se kuluttaa vähemmän sähköä verrattuna oikeaan tietokoneeseen, eikä sido tietokoneen omia resursseja. Rasberry toimii IoT laitteena. Näin myös ohjelma pysyy toiminnassa tietokoneen tilasta huolimatta. OpenWeatherMap tarjoaa kyllä myös paljon muutakin tietoa, mutta tähän meidän tarkoitukseen ajattelimme lämpötiladatan riittävän.

![Kuva2](F:\petri\Pictures\Kuva2.png)

Python ohjelman kokosimme yhdistelemällä erilaisia valmiita malleja netistä. Koodimme koostuu usean lähteen johdosta eri osioista, mutta raakasti olemme muokanneet kaikkia koodeja. Enää ei ole meidän lopullisessa ohjelmassamme montaa riviä alkuperäisiä netistä löydettyjä python-skriptejä.

![Kuva3](F:\petri\Pictures\Kuva3.png)

Vaikeata oli saada alunperin data hyppäämään rasberrystä Azureen. Datan muoto myös oli ongelmallinen, sillä Azure ei oikein ymmärrä Base64 Muotoa. Tähän meitä auttoi löytämämme koodi rivi, jolla datan saa muutettua Azuren paremmin tukemaan Json muotoon.

![Kuva4](F:\petri\Pictures\Kuva4.png)

Datan saatuamme tulemaan Azureen mietimme, mitä me sillä datalla nyt tekisimmekään. Tutkimme erilaisia vaihtoehtoja ja opettajan esimerkin innoittamana päätimme rakentaa Datafactoryn ja pipelinen. Pipeline louhii tietoa eräkerroksen masterdatasta ja vie sitä tarjoilukerroksen NoSql databaseen, joka toteutettiin CosmosDB:llä. Tarjoilukerroksesta datan voi ladata csv-tiedostona ja avata Excelillä.

![Kuva5](F:\petri\Pictures\Kuva5.png)

Meidän rakentamamme systeemi on Cold Path, eli masterdatasta louhitaan agregaattorilla näkymiä tarjoilukerrokseen, josta dataa voi siirtää vaikka sovelluksille, verkkosivuille tai mihin tahansa muuhun käyttöön. Tämän tekniikan taustalla on Lambda arkkitehtuuri.

Ei sekään kuitenkaan aivan ajatuksen voimalla sujunut. Saimmepa opettajankin ihmettelemään pitkän aikaa meidän datan käyttäytymistä. Datalle oli vaikeaa mennä pipelinen läpi sinkiin. Tämän ongelman saimme ratkaistua opettajan kanssa tunnilla tuumittuamme. Tunnillakin kuitenkin mielenkiintoisesti alkuun kaikki data oli hukassa, toisin kuin aiemmin olimme dataa Azuressa nähneet. Onneksi tämäkin saatiin selvitettyä ja näin saimme työmme tehtyä loppuun asti.

Jatkokehitysideoita miettiessämme meillä heräsi ajatus siitä, että haluaisimme tehdä jotakin tällä kaikella tiedolla, mitä me Azureen nyt saamme ja siellä käsittelemme. Erityisesti keskuudestamme nousi idea nettisivusta, tai sovelluksesta, joka näyttäisi joko tämänhetken tai historia tietoa lämpötilasta. Päivän suurin lämpötila-arvo voisi myös olla kätevä saada eroteltua ja ilmoitettua. Tätä tutkiessamme huomasimme, että Azuresta suoraan saa zip tiedostona arvoja Json muodossa, mutta se ei tssä oikein auta, sillä erityisesti kiiinnostaisi muuten käyttää dataa, kuin kerran ladata. Löysimme Power BIn. Ajattelimme, että se olisi hyödyllinen tapa saada dataa ulos. Olemme myös kuulleet, että yritykset käyttävät sitä omiin tarkoituksiinsa. Alkuun vähän sitä kokeilimme, mutta sekään ei helpolla sujunut. Monia error-koodeja sekin lykkäsi.

![Kuva6](F:\petri\Pictures\Kuva6.png)

Työn tekemistä edes auttoi paljon, että löysimme Azuresta IAM ominaisuuden, millä pystyimme jakamaan Azuressa tehtäviä juttuja keskenänmme. Näin saimme kaikki yhtäläisesn pääsyn esimerkiksi IoT-hubiimme.

Oppimiskokemuksena tämä työ on ollut laajasti silmiä avaava. Olemme oppineet paljon Iot laitteista ja datan käsittelystä. Erityisesti datan ominaisuudet ja käyttäytminen ovat opettaneet meitä paljon ymmärtämään, miten suuret datamäärät toimivat. Tuleivaisuudessa uskomme tämän harjoituksen oppien tulevan oikeasti käyttöönkin, sillä nämä samat toiminta tavat nimittäin toimivat myös erittäinkin isoillekin datamäärille. Meidän mielestämme opiskelijuiden parasta hyötyä ovat juuri nämä tuleivaisuuden kannalta merkitykselliset rakennelmat.
