# Azure IoT harjoitustehtävä 

## Petri Kaila, Piia Virrankoski, Jere Jämsä


Rakensimme IoT hubin, jonne saimme dataa Raspberry PI:ltä. Raspberryn ohjelma hakee OpenWeather palvelusta Kalajoen lämpötilaa ja tunnin välein lähettää sen Azureen.

Tehtävämme alkoi ideoinnista, mitä ihmettä me voisimme tehdä. Päädyimme tutkailemaan erilaisia tapoja saada lämpötiladataa. Tämän jälkeen huomasimme myös opettajamme käsittelevän lämpötiladataa, mikä hivenen auttoi meitä eteenpäin rakentamaan pipelineamme.

Tehtävää tehdessämme monet kerrat olemme nettiä selailleet apuja etsien. Eihän meillä heti alkuun ollut edes tiedossa, kuinka saamme dataa edes kerättyä. Kokeilimme alkuun jopa puhelinta käyttää mittalaitteena, mutta kun se ei onnistunutkaan, päädyimme käyttämään OpenWeatherin tarjoamaa APIa. Siellä voi rakentaa APIn joka tarjoaa projektiin tarvittavan datan. Me valitsimme lämpötilan.

Vaikka olemme tietotekniikan opiskelijoita, ei meillä ole vielä ollenkaan ollut Python-koodausta, mutta tässä APIn kanssa Python-ohjelma tuntui olevan tässä vaiheessa paras vaihtoehto kerätä dataa, kun tarpeeksi googlailtuemme löysimme pari Python koodia, toinen keräsi dataa OpenWeatherista ja toinen lähetti dataa IoT Hubiin. Näin tuli opittua vähän lisää uudesta ja kurssin ulkopuolisesta asiasta.

Näistä kahdesta koodista saimme aikaiseksi toimivan [Python](https://github.com/PetriKaila/AzureProjekti/blob/main/saa.py) koodin, millä saamme OpenWeatherista kerättyä dataa Raspberryn kautta IoT Hubiin. Koodiin kovakoodattiin Kalajoki, koska Petri halusi seurata paikkakuntansa lämpötilaa.

![projekti](https://user-images.githubusercontent.com/102190520/234664634-7f8825e3-f99c-4530-80c3-5265a70104c7.png)

Tarvittiin kyllä paljon verta hikeä ja kyyneliä, että saimme Python koodit yhdistettyä ja toimimaan haluamallamme tavalla.

![](https://user-images.githubusercontent.com/102190520/234664854-c09af45d-d8e1-4f3c-8652-ce958af43c1b.png)

Raspberrya käytämme välissä siksi, koska se kuluttaa vähemmän sähköä verrattuna oikeaan tietokoneeseen, eikä sido tietokoneen omia resursseja. Raspberry toimii IoT laitteena. Näin myös ohjelma pysyy toiminnassa tietokoneen tilasta huolimatta. OpenWeather API tarjoaa kyllä myös paljon muutakin tietoa, mutta tähän meidän tarkoitukseemme ajattelimme lämpötiladatan riittävän.

![projekti](https://user-images.githubusercontent.com/102190520/234664633-10ffc090-4d03-4bd6-a598-8d479fc4703c.png)

Koodimme siis koostuu kahdesta esimerkki koodista, jotka yhdistimme ja muokkasimme aikamme, että saimme sen toimivaksi. Enää ei ole meidän lopullisessa koodissamme ollut montaa riviä alkuperäisiä netistä löydettyjä koodin pätkiä.

Alun perin oli vaikeaa saada data siirtymään Raspberrysta Azureen. Datan muoto myös oli ongelmallinen, sillä JSON tiedoston lämpötiladata näkyi Base64 muotona. Tähän löytyi jälleen kerran googlailemalla keino, jolla lämpötila data saatiin selkokieliseksi JSON tiedostoon, lisäämällä koodiin *content_encoding = "utf-8", content_type = "application/json".*
![image](https://user-images.githubusercontent.com/102190520/234672526-2cc02c19-8433-4a36-a22a-209bb5290f22.png)

Dataa tunnin välein
![image](https://user-images.githubusercontent.com/102190520/234792626-561e1ef8-6039-4984-9eb7-3eb86f868e15.png)
---


Tämän jälkeen astuu kuvioon big datan lambda arkkitehtuuri, jonka mukaisesti rakensimme datalle cold path käsittelyn siten, että hyödynsimme siihen Azuren Data Factoryn Pipelinea. Pipeline louhii dataa blob storagen masterdatabasesta ja aggregaattorifunktion avulla siirtää haluamaamme tietoa tarjoilukerroksen NoSQL-databaseen, jonka toteutimme CosmosDB:llä. Tämän jälkeen dataa voisi tarjoilukerroksesta jakaa, vaikka verkkosivulle tai sovellukselle, mutta tähän meillä ei aika tässä työssä riitä.

![projekti](https://user-images.githubusercontent.com/102190520/234664637-7888e5bb-fce3-4b32-8f8a-b476d9d37b8f.png)

Ei sekään kuitenkaan aivan ajatuksen voimalla sujunut. Saimmepa opettajankin ihmettelemään pitkän aikaa meidän datamme käyttäytymistä. Datalle oli vaikeaa mennä pipelinen läpi sinkiin. Tämän ongelman saimme ratkaistua opettajan kanssa tunnilla tuumittuamme. Tunnillakin kuitenkin mielenkiintoisesti alkuun kaikki data oli hukassa, toisin kuin aiemmin olimme dataa Azuressa nähneet. Onneksi tämäkin saatiin selvitettyä ja näin saimme työmme tehtyä loppuun asti.

Jatkokehitysideoita miettiessämme meillä heräsi ajatus siitä, että haluaisimme tehdä jotakin tällä kaikella tiedolla, mitä me Azureen nyt saamme ja siellä käsittelemme. Erityisesti keskuudestamme nousi idea nettisivusta, tai sovelluksesta, joka näyttäisi joko tämän hetken tai historia tietoa lämpötilasta. Päivän suurin lämpötila-arvo voisi myös olla kätevä saada eroteltua ja ilmoitettua. Tätä tutkiessamme huomasimme, että Azuresta suoraan saa pakattuna ZIP tiedostona arvoja JSON muodossa, mutta se ei tässä oikein auta, sillä erityisesti kiinnostaisi muuten käyttää dataa, kuin kerran ladata. Löysimme Power Bi:n Ajattelimme, että se olisi hyödyllinen tapa saada dataa ulos, mutta muistaakseni se olisi ollut niin kallis ratkaisu, että poistuimme sieltä välittömästi.

![image](https://user-images.githubusercontent.com/102190520/234672894-8feb7e4a-efba-4922-96f6-fed11d68a066.png)

Työn tekemistä edes auttoi paljon, että löysimme Azuresta IAM ominaisuuden, millä pystyimme jakamaan Azuressa tehtäviä juttuja keskenämme. Näin saimme kaikki yhtäläisen pääsyn esimerkiksi IoT Hubiimme.

![projekti](https://user-images.githubusercontent.com/102190520/234664628-93c8825a-1961-4bac-8613-8fda230eb09a.png)

Oppimiskokemuksena tämä työ on ollut laajasti silmiä avaava. Olemme oppineet paljon IoT laitteista ja datan käsittelystä. Erityisesti datan ominaisuudet ja käyttäytyminen ovat opettaneet meitä paljon ymmärtämään, miten suuret datamäärät toimivat. Tulevaisuudessa uskomme tämän harjoituksen oppien tulevan oikeasti käyttöönkin, sillä nämä samat toiminta tavat nimittäin toimivat erittäinkin isoillekin datamäärille. Meidän mielestämme opiskelijoiden parasta hyötyä ovat juuri nämä tulevaisuuden kannalta merkitykselliset rakennelmat.

---

lähteet: Stackoverflow, Microsoft, [Geeksforgeeks OpenWeather koodi](https://www.geeksforgeeks.org/python-find-current-weather-of-any-city-using-openweathermap-api/), [DEV.to datan lähetys](https://dev.to/nihalbaig0/stream-data-to-azure-iot-hub-from-raspberry-pi-1ed3#:~:text=Configuring%20Raspberry%20Pi)






![projekti (5)](https://user-images.githubusercontent.com/102190520/234664640-4aa47da4-d1c8-4555-807d-4c122759be64.png)

![image](https://user-images.githubusercontent.com/102190520/234671913-9f8a98ac-4106-4886-b35f-b9e76ce95f82.png)
