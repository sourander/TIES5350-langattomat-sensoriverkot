import marimo

__generated_with = "0.20.2"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # LoRa Exam Retake

    I made a fair amount of mistakes in my previous exam try.  I scored only 7/16 in the exam. My errors were briefly...
    ## Kysymys 1

    Answer was fully correct. (293 bps)

    ## Kysymys 2

    The answer 611 is wrong. I suspect 670 is correct.

    I forgot to add the frame, 13 bytes mentioned in brief, like so...

    ```
    # toa_q2 = compute_time_on_air(9, 125e3, 4/5, 115)
    toa_q2 = compute_time_on_air(9, 125e3, 4/5, 115 + 13)
    ```

    ## Kysymys 3

    The 685 is wrong. 23 is correct, I suspect. I didn't realize to include the TTN limitation, like...

    ```
    # max_messages_q3 = compute_max_daily_uplinks(_toa_q3, EU868_DUTY_CYCLE, int(10e31))
    max_messages_q3 = compute_max_daily_uplinks(_toa_q3, EU868_DUTY_CYCLE, TTN_FAIR_ACCESS_LIMIT_MS)
    ```

    ## Kysymys 4

    Answer was fully correct (1 radio needed.)

    ## Kysymys 5

    The first task was CORRECT, the bitrate being 5470 bps.

    My mistake is, I suppose, not using the frame, again...

    ```
    # raw_toa = compute_time_on_air(7, 125e3, 1, (32 // 8))
    raw_toa = compute_time_on_air(7, 125e3, 1, (32 // 8) + 13) # Updated answer: 28 -> 42
    ```

    This caused the task 2, 3, 4 answers to be...

    * 28 ms instead of 43 ms
    * 1080 pcs instead of 998 pcs (pcs = kpl, kappaletta, units)
    * 3 pcs instead of 5 pcs
    """)
    return


@app.cell
def _():
    import math
    import numpy as np

    from scipy.special import erf, erfc

    return (math,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## LoRa

    ### Parameter Reference

    | Variable | Description | Engineering Unit |
    | -------- | ----------- | ---------------- |
    | BW | Bandwidth | Hz (125 kHz) |
    | SF | Spreading Factor | Integer (7–12) |
    | CR | Coding Rate | Often 4/5 |
    | T_sym | Symbol Duration | ms |
    | ToA | Time on Air | ms |
    | PL | Payload Size | Bytes |
    """)
    return


@app.cell
def _(math):
    def compute_bit_rate(SF, BW, CR):
        """Calculates the raw LoRa bit rate in bits per second."""
        # Formula from Slide 157/174
        return SF * (BW / 2**SF) * CR

    def compute_symbol_duration(SF, BW):
        """Calculates the duration of one LoRa symbol in milliseconds."""
        # Formula from slide 162/174
        return (2**SF / BW) * 1000

    def compute_time_on_air(SF, BW, CR, PL, header=True):
        """Calculates the total Time on Air (ToA) for a LoRa packet in milliseconds."""
        T_sym = compute_symbol_duration(SF, BW)
        T_preamble = (8 + 4.25) * T_sym

        # DE is 0 when SF <= 10, and DE is 1 when SF >= 11
        DE = 1 if SF >= 11 else 0

        # This is some mind-boggline conversion to get the CR into an integer form.
        CR_int = round((1 / CR - 1) * 4)  # converts 4/5→1, 4/6→2, 4/7→3, 4/8→4

        # Formula from lecture slides
        payload_sym = 8 + ((8 * PL - 4 * SF + 28 + 16) / (4 * (SF - 2 * DE))) * (CR_int + 4)

        # Number of payload symbols * duration of one symbol gives us the payload time
        T_payload = payload_sym * T_sym
        return T_preamble + T_payload

    def compute_max_daily_uplinks(ToA, duty_cycle_limit=0.01, ttn_fair_access_limit=30_000):
        """Calculates max daily uplinks respecting the EU868 duty cycle and TTN fair access limits."""
        day_ms = 24 * 60 * 60 * 1000
        max_by_duty_cycle = math.floor((day_ms * duty_cycle_limit) / ToA)
        max_by_ttn = math.floor(ttn_fair_access_limit / ToA)
        return min(max_by_duty_cycle, max_by_ttn)

    return compute_bit_rate, compute_max_daily_uplinks, compute_time_on_air


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Max LoRa messages in one hour

    The Time on Air for a single LoRa message is 400 ms and the duty cycle is 1%. What is the maximum number of messages that can be sent within one hour?
    """)
    return


@app.cell
def _(compute_bit_rate, compute_max_daily_uplinks, compute_time_on_air, math):
    # Maximum daily uplinks per SF using max allowed payload, EU868 + TTN limits
    max_payload = {7: 222, 8: 222, 9: 115, 10: 51, 11: 51, 12: 51}
    BW = 125e3
    CR = 4/5

    EU868_DUTY_CYCLE = 0.01  # 1% legal limit
    TTN_FAIR_ACCESS_LIMIT_MS = 30_000  # 30 seconds per 24h

    print(f"{'SF':<4} {'ToA (ms)':>10} {'Max/day (EU868)':>17} "
          f"{'Max/day (TTN)':>15} {'Limiting Factor':>17} {'Bitrate':>12}")
    print("-" * 80)
    for sf, pl in max_payload.items():
        toa = compute_time_on_air(sf, BW, CR, pl)
        bitrate = compute_bit_rate(sf, BW, CR)
        day_ms = 24 * 60 * 60 * 1000

        max_eu = math.floor((day_ms * EU868_DUTY_CYCLE) / toa)
        max_ttn = math.floor(TTN_FAIR_ACCESS_LIMIT_MS / toa)
        limit = "EU868" if max_eu < max_ttn else "TTN"
        max_combined = compute_max_daily_uplinks(toa, EU868_DUTY_CYCLE, TTN_FAIR_ACCESS_LIMIT_MS)

        # The .0f rounds to zero decimal places for display purposes
        print(f"SF{sf:<2} {toa:>10.1f} {max_eu:>17} {max_ttn:>15} {limit:>17} {bitrate:>12.0f}")
    return EU868_DUTY_CYCLE, TTN_FAIR_ACCESS_LIMIT_MS, max_payload


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Uusi yritys alkaa

    Here beging my 2nd try at doing the exam.

    **RULE:** Do not touch the functions. Those have been tested to match the lecture notes. I know that the calculations do not match to industry practices, but this is what the professor uses.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Kysymys 1

    Laske luennoilla esitetyllä tavalla LoRa radion tiedonsiirtonopeus (bps) spreading factorilla SF11.

    Laske aluksi tiedonsiirtonopeus muodossa bittiä per sekunti (bps) itsellesi paperille
    Tarkista, että et tehnyt laskuvirhettä
    Anna pelkkä numeerinen vastaus, ilman yksikköä, alla olevaan kohtaan.
    """)
    return


@app.cell
def _(compute_bit_rate):
    compute_bit_rate(11, 125e3, 4/5)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Kysymys 2

    Maximum payload SF11 arvolla on 51 tavua. Kehys vie 13 tavua. Laske ilma-aika (time-on-air) kun lähetetään maximum payload SF11 arvolla.
    """)
    return


@app.cell
def _(compute_time_on_air):
    print(f"Kysymys 2:", compute_time_on_air(11, 125e3, 4/5, 51 + 13))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Kysymys 3

    Kun huomioidaan LoRaWAN ja EU868 asettamat rajoitukset LoRa viestiliikenteeseen, niin kuinka monta viestiä maximi payloadilla voidaan lähettää vuorokaudessa (24 tuntia) spreading factorilla SF7?
    """)
    return


@app.cell
def _(
    EU868_DUTY_CYCLE,
    TTN_FAIR_ACCESS_LIMIT_MS,
    compute_max_daily_uplinks,
    compute_time_on_air,
    max_payload,
):
    _k3 = compute_time_on_air(7, 125e3, 4/5, max_payload[11])
    print("Kysymys 3: ", compute_max_daily_uplinks(_k3, EU868_DUTY_CYCLE, TTN_FAIR_ACCESS_LIMIT_MS))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Kysymys 4

    SmartHome-projektissa muistisairaan vanhuksen asuntoa monitoroidaan liiiketunnistimilla, joiden avulla pyritään luomaan kuva vanhuksen vuorokausirytmistä. Jokainen yksittäinen liiketunnistin tallentaa viiden sekunnin välein bittijonoon arvon yksi, jos on havaittu liikettä ja muutoin arvon nolla. Yksittäinen liiketunnistin kerää dataa 10 minuutin ajan eli liiketunnistinta vastaavan bittijonon pituus on 120 bittiä. Bittijono voidaan tiivistää 30 bitin tiivisteeksi. Jokaista liiketunnistinta vastaava tiivistetty bittijono halutaan saada palvelimelle kymmenen minuutin välein. Tarkastele tilannetta yhden vuorokauden aikana.

    1. Käytössä LoRa verkko, joka voi käyttää spreading factoria SF10
    2. Tiedonsiirto noudattaa LoRaWANin ja EU868n mukaisia rajoituksia
    3. Oletetaan, että verkko toimii häiriöittä
    4. Asunnossa on 4 liiketunnistinta
    5. Laske lähetettävän viestin ilma-aika ja huomioi LoRaWANin 30s rajoite vuorokaudessa
    6. Montako LoRa radiota tarvitaan välittämään viestit eteenpäin?
    7. Anna tarvittavien LoRa radioiden lkm alla olevaan ruutuun.
    """)
    return


@app.cell
def _(
    EU868_DUTY_CYCLE,
    TTN_FAIR_ACCESS_LIMIT_MS,
    compute_max_daily_uplinks,
    compute_time_on_air,
    math,
):
    _data_per_sensor_bits = 30
    _num_sensors = 4
    _transmission_interval_minutes = 10

    _lora_sf = 10
    _lora_bw = 125e3  # 125 kHz
    _lora_cr = 4 / 5

    # Calculate total data to be sent every 10 minutes (all sensors total)
    _total_data_bits_per_message = _data_per_sensor_bits * _num_sensors
    _payload_bytes = math.ceil(_total_data_bits_per_message / 8)

    # 10 minutes is 6 times per hour, and thus, per day...
    _total_messages_needed_per_day = 24 * 6

    # 4. Calculate Time on Air (ToA) for a single message with the determined payload
    _toa_ms = compute_time_on_air(_lora_sf, _lora_bw, _lora_cr, _payload_bytes)
    _toa_daily_seconds = (_toa_ms / 1000) * _total_messages_needed_per_day


    # Maximum number of messages a single LoRa radio can send per day
    # using the EU868 duty cycle and TTN fair access limits.
    _max_messages_per_radio_per_day = compute_max_daily_uplinks(
        _toa_ms, EU868_DUTY_CYCLE, TTN_FAIR_ACCESS_LIMIT_MS
    )

    # 6. Determine the number of LoRa radios required
    _num_lora_radios_needed = math.ceil(
        _total_messages_needed_per_day / _max_messages_per_radio_per_day
    )

    print(f"Calculated payload per message: {_payload_bytes} bytes")
    print(f"Total messages required per day: {_total_messages_needed_per_day:.0f}")
    print(f"Time on Air per message (SF{_lora_sf}, PL={_payload_bytes}): {_toa_ms:.1f} ms")
    print(f"Total Time on Air per day: {_toa_daily_seconds:.2f} seconds")
    print(f"Max messages per radio per day: {_max_messages_per_radio_per_day:.0f}")
    print(f"Number of LoRa radios needed: {_num_lora_radios_needed:.0f}")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Kysymys 5
    """)
    return


@app.cell
def _(
    EU868_DUTY_CYCLE,
    TTN_FAIR_ACCESS_LIMIT_MS,
    compute_bit_rate,
    compute_max_daily_uplinks,
    compute_time_on_air,
    math,
):
    # a. Calculate bit rate towards the Gateway
    print("A: ", compute_bit_rate(7, 500e3, 4/5))

    # b. Calculate Time on Air for one sensor's data packet
    # raw_toa = compute_time_on_air(7, 125e3, 1, (32 // 8))
    raw_toa = compute_time_on_air(7, 125e3, 1, (32 // 8) + 13) # Updated answer: 28 -> 42
    print("B: ", raw_toa)

    # c. Calculate how many measurement packets can be sent by one LoRaWAN device per day
    max_packets_per_day = compute_max_daily_uplinks(raw_toa, EU868_DUTY_CYCLE, TTN_FAIR_ACCESS_LIMIT_MS)
    print("C: ", max_packets_per_day) # Updated answer: 1080 -> 998

    # d. Calculate how many LoRaWAN devices are needed to transmit all measurements
    num_sensors = 20
    measurements_per_sensor_per_day = 24 * 6  # every 10 minutes
    total_measurements_per_day = num_sensors * measurements_per_sensor_per_day
    num_lorawan_devices_needed = math.ceil(total_measurements_per_day / max_packets_per_day)
    print("D: ", num_lorawan_devices_needed)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Vanha tentti

    Alla oleva tentti on muistiinpanona omien virheiden analysointia varten.

    ## Kysymys 1

    Laske luennoilla esitetyllä tavalla LoRa radion tiedonsiirtonopeus (bps) spreading factorilla SF12.

    Laske aluksi tiedonsiirtonopeus muodossa bittiä per sekunti (bps) itsellesi paperille
    Tarkista, että et tehnyt laskuvirhettä
    Anna pelkkä numeerinen vastaus, ilman yksikköä, alla olevaan kohtaan.
    Vastauksen arvioinnissa huomioidaan mahdollinen pieni pyöristysvirhe.
    """)
    return


@app.cell
def _(compute_bit_rate):
    compute_bit_rate(12, 125e3, 4/5)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Kysymys 2

    Maximum payload SF9 arvolla 115 tavua. Kehys vie 13 tavua. Laske ilma-aika (time-on-air) kun lähetetään maximum payload SF9 arvolla.

    Katso esimerkki luentokalvoilta.

    Laske ensin ilma-aika millisekunneissa (ms) paperille
    Tarkista, että et ole tehnyt laskuissa virhettä
    Laita ainoastaan numeerinen vastaus millisenkunteina (ms) ilman yksikköä alla olevaan ruutuun.
    Arvioinnissa huomioidaan mahdollinen pyöristysvirhe.

    **Päivitys:** Sain tentissä väärän tuloksen. Oletan, että virhe tulee siitä, että en summannut payloadin ja kehyksen kokoja, vaan laitoin vain payloadin koon yksin.
    """)
    return


@app.cell
def _(compute_time_on_air):
    # toa_q2 = compute_time_on_air(9, 125e3, 4/5, 115)
    toa_q2 = compute_time_on_air(9, 125e3, 4/5, 115 + 13)

    print(f"{toa_q2:.1f}")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Kysymys 3

    Kun huomioidaan LoRaWAN ja EU868 asettamat rajoitukset LoRa viestiliikenteeseen, niin kuinka monta viestiä maximi payloadilla voidaan lähettää vuorokaudessa (24 tuntia) spreading factorilla SF11?

    Laske ensin vastaus paperille
    Tarkista, että et ole tehnyt virheitä
    Siirrä pelkkä numeerinen vastaus alla olevaan lokeroon
    Arvioinnissa huomioidaan pieni pyöristysvirhe

    **Päivitys:** Tentin vastauksessa ilmeiseti pitää olla myös TTN:n asettama 30s/vrk rajoite huomioituna, eikä vain EU868n 1% duty cycle.
    """)
    return


@app.cell
def _(
    EU868_DUTY_CYCLE,
    TTN_FAIR_ACCESS_LIMIT_MS,
    compute_max_daily_uplinks,
    compute_time_on_air,
    max_payload,
):
    _toa_q3 = compute_time_on_air(11, 125e3, 4/5, max_payload[11])
    # Make the TTN to be effectively unlimited by setting it to a very high value (10e31 ms is about 3.17 trillion years)
    # This way we are only limited by the EU868 duty cycle, which is the intended focus of this question.
    # max_messages_q3 = compute_max_daily_uplinks(_toa_q3, EU868_DUTY_CYCLE, int(10e31))
    max_messages_q3 = compute_max_daily_uplinks(_toa_q3, EU868_DUTY_CYCLE, TTN_FAIR_ACCESS_LIMIT_MS)

    print(f"{max_messages_q3:.0f}") # Updated answer: 685 -> 23
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Kysymys 4

    Liiketunnistin tuottaa dataa 30 bittiä per 10 minuuttia. Jokaista liiketunnistinta (4 kpl) vastaava tiivistetty bittijono halutaan saada palvelimelle kymmenen minuutin välein. Tarkastele tilannetta yhden vuorokauden aikana.

    1. Käytössä LoRa verkko, joka voi käyttää spreading factoria SF7
    2. Tiedonsiirto noudattaa LoRaWANin ja EU868n mukaisia rajoituksia
    3. Oletetaan, että verkko toimii häiriöittä
    4. Asunnossa on 4 liiketunnistinta
    5. Laske lähetettävän viestin ilma-aika ja huomioi LoRaWANin 30s rajoite vuorokaudessa
    6. Montako LoRa radiota tarvitaan välittämään viestit eteenpäin?
    7. Anna tarvittavien LoRa radioiden lkm alla olevaan ruutuun.
    """)
    return


@app.cell
def _():
    # removed due to same question being again
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Kysymys 5

    Sovelluksessa liikkumista varastotilassa seurataan liiketunnistimilla. Liiketunnistimet muodostavat LoRa-radioihin pohjautuvan mesh-verkon, missä laitteet voivat välittää omat mittaustulokset LoRaWAN yhteyden omaaville laitteille. LoRaWAN-laite välittää saamansa mittaustulokset yksitellen gateway-laitteelle.

    Jokainen yksittäinen liiketunnistin tallentaa viiden sekunnin välein bittijonoon arvon yksi, jos on havaittu liikettä ja muutoin arvon nolla. Yksittäinen liiketunnistin kerää dataa 10 minuutin ajan eli liiketunnistinta vastaavan bittijonon pituus on 120 bittiä. Bittijono voidaan tiivistää 32 bitin tiivisteeksi. Jokaista liiketunnistinta vastaava tiivistetty bittijono pyritään välittämään LoRaWAN-laitteen kautta palvelimelle kymmenen minuutin välein.

    Oletukset : Oletetaan, että käytössä oleva LoRaWAN-verkko toimii häiriöittä ja tiedonsiirto noudattaa LoRaWANin ja EU868n mukaisia rajoituksia. Laitteet eivät ole ajallisesti synkronoitu keskenään. Verkon asetukset

    Kaistanleveys B=125KHz, Spreading Factor SF=7
    Varastossa on 20 liiketunnistinta

    ### Tehtävät

    a. Laske käytössä olevien LoRaWAN laitteiden (kaikki identtisiä) tiedonsiirtonopeus kohti Gateway-laitetta. Anna vastaus pyöristettynä täyteen kymmenlukuun, esimerkiksi 3567 annetaan muodosssa 3570. Käytä laskuissa CR=4/5. Vastauksen yksikö on bps.

    b. Laske yhden liiketunnistimen 10 minuutin mittausjaksolla keräämän datan välittämiseen kuluva ilma-aika LoRaWAN laitteella. Huomioi kehyksen koko 13 tavua. Käytä laskuissa CR=1 ja DE=0. Anna vastaus kokonaislukuna. Vastauksen yksikö on ms.

    c. Laske kuinka monen mittausjakson datapaketit voisit korkeintaan välittää yhdellä LoRaWAN laitteella vuorokaudessa, kun huomioidaan LoRaWANin 30s/vrk rajoite. Yksikkö on kpl/vrk.

    d. Montako LoRaWAN yhteyden omaavaa laitetta tarvitaan vähintään välittämään varaston kaikki mittaustulokset vuorokaudessa eteenpäin? Yhden mittauspisteen viestit välitetään aina samalla LoRaWAN-laitteella. Vastaus on n kappaletta.

    **Päivitys:** Tentin tulosten myötä oletan, että kohta B on väärin, koska en huomioinut kehyksen koko 13 tavua. Tämä muuttaa myös kahta seuraavaa muuta vastausta.
    """)
    return


@app.cell
def _():
    # removed due to question being the same in 2nd exam
    return


if __name__ == "__main__":
    app.run()
