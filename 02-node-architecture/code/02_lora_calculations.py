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
    # Node calculations

    This is my memo for looking into the: **Project Description: SmartHome LoRa Monitoring**

    In the **SmartHome** project, the apartment of an elderly person with memory disorders is monitored using motion sensors. These sensors are used to create a profile of the resident's daily rhythm. The data is transmitted to a server utilizing **LoRa radios**.

    The data transmission capacity of a LoRa radio depends on the quality of the connection as well as the regulatory restrictions imposed on radio usage. By default, a bandwidth of **125 kHz** is used unless stated otherwise in the assignment.

    In this application task, you will determine the data transmission capacity for different **Spreading Factor (SF)** values, which vary based on connection quality. To assess whether the transmission capacity is sufficient, you must also estimate the **airtime** of the transmissions and account for the usage limitations set by **EU868** (regional regulations) and **TTN** (The Things Network).
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

    LoRa uses a spreading factor (SF) between 7 and 12.

    * SF impacts the communication of LoRa
    * A larger SF increases the time on air, which increases energy consumption, reduces the data rate, and improves communication range

    ### Parameter Reference

    | Variable | Description | Engineering Unit |
    | -------- | ----------- | ---------------- |
    | BW | Bandwidth | Hz (125 kHz) |
    | SF | Spreading Factor | Integer (7–12) |
    | CR | Coding Rate | 4/(4+n), e.g. 4/5 ≈ 0.8 |
    | T_sym | Symbol Duration | ms |
    | ToA | Time on Air | ms |
    | PL | Payload Size | Bytes |

    SF is given by the following formula:

    $$
    SF = \log_2\left(\frac{R_b}{R_s}\right)
    $$

    where $R_b$ is the bit rate and $R_s$ is the symbol rate. The speading factor defines two fundamental values: (1) the number of chips contained in each symbol is $2^{SF}$, and (2) the number of raw bits that can be encoded by that symbol is SF. The symbol rate can be calculated as:

    $$
    R_s = \frac{BW}{2^{SF}}
    $$

    The table shows the ultimate LoRa trade-off: You are trading speed (chips/symbol) for range and reliability (SNR limit). This is beow calculated in the `compute_symbol_duration()` function. Note that chips/symbol is $2^{SF}$, and the SNR limit is the minimum SNR required for successful communication at that SF. We would need this SNR to compute Link Budget or Maximum Range like was done above with the Friis.

    | SF | chips/symbol | SNR limit (dB) |
    | -- | ------------ | -------------- |
    | 7  | 128  | -7.5 |
    | 8  | 256  | -10  |
    | 9  | 512  | -12.5 |
    | 10 | 1024 | -15  |
    | 11 | 2048 | -17.5 |
    | 12 | 4096 | -20  |

    Data rate can be computed as:

    $$
    DataRate = SF \cdot \frac{B}{2^{SF}} \cdot CR
    $$

    Where $B$ is bandwidth and $CR$ is coding rate amount numbers $4/5, 4/6, 4/7, \text{ or } 4/8$.
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

    return (
        compute_bit_rate,
        compute_max_daily_uplinks,
        compute_symbol_duration,
        compute_time_on_air,
    )


@app.cell
def _(compute_bit_rate, compute_symbol_duration):
    # Data rate and symbol duration for each SF at 125 kHz BW, CR=4/5
    def datarate_n_symbol_durations():
        print(f"{'SF':<4} {'Bit Rate (bps)':>15} {'Symbol Duration (ms)':>22}")
        print("-" * 44)
        for sf in range(7, 13):
            dr = compute_bit_rate(sf, 125e3, 4/5)
            ts = compute_symbol_duration(sf, 125e3)
            print(f"SF{sf:<2} {dr:>15.2f} {ts:>22.3f}")

    datarate_n_symbol_durations()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## LoRaWAN data rate

    Data rate supported by LoRaWAN as table...

    | Data rate | SF | BW (kHz) | Bytes/sec | Range |
    | --------- | -- | -------- | --------- | ----- |
    | DR0         | 12 | 125      | 31       | Longest  |
    | DR1        | 11 | 125      | 55       | Longer |
    | DR2       | 10 | 125      | 122      | Long |
    | DR3       | 9  | 125      | 220      | Short |
    | DR4       | 8  | 125      | 390      | Shorter |
    | DR5        | 7  | 125      | 683      | Shortest |

    What is that table? This is poorly explained in the lecture. In LoRaWAN, instead of forcing developers to manually set SF and BW every time, the protocol defines standard Data Rate (DR) indices (DR0, DR1, DR2, etc.). In the EU868 region, DR0 is strictly defined as SF12 / 125 kHz. DR5 is SF7 / 125 kHz.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## LoRa total air transmission

    Total air transmission can be calculated as...

    $$
    T_{packet} = T_{preamble} + T_{payload}
    $$

    Symbol rate $T_{SR}$ is time to send one symbol. It depends on SF value and bandwidth

    $$
    T_{SR} = \frac{2^{SF}}{BW}
    $$

    LoRa packet includes preamble, header and payload

    * Number of preamble symbols is (8 + 4, 25)
    * The size of the header is typically 13 bytes and it is added to payload
    * Maximum payload depends on spreading factor SF
    """)
    return


@app.cell
def _(compute_time_on_air):
    # LoRaWAN EU868 maximum payload per SF (bytes), using explicit header + CRC
    # Ref: https://www.thethingsnetwork.org/docs/lorawan/regional-parameters/
    def maximum_payload_per_sf_explicit_header_crc():
        max_payload = {7: 222, 8: 222, 9: 115, 10: 51, 11: 51, 12: 51}

        print(f"{'SF':<4} {'Max PL (B)':>10} {'ToA (ms)':>12}")
        print("-" * 30)
        for sf, pl in max_payload.items():
            toa = compute_time_on_air(sf, 125e3, 4/5, pl)
            print(f"SF{sf:<2} {pl:>10} {toa:>12.1f}")

    maximum_payload_per_sf_explicit_header_crc()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Preample time on air

    Number of preamble symbols is (8 + 4, 25) and then Time-on-Air of preamble is

    $$
    ToA_{preample} = N_{preamble} \cdot T_{SR}
    $$

    For example: If SF9 and TSR is 4,096ms, the Time-on-Air of Preamble is

    $$
    ToA_{preample} = (8 + 4.25) \cdot 4.096ms = 50.176ms
    $$
    """)
    return


@app.cell
def _():
    def calculate_preamble_percentage(toa_packet_ms, toa_preamble_ms):
        """Calculates the percentage of total airtime that the preamble occupies."""
        percentage = (toa_preamble_ms / toa_packet_ms) * 100
        return round(percentage, 2)

    toa_packet = 1200 # ms
    toa_preamble = 50 # ms

    preamble_pct = calculate_preamble_percentage(toa_packet, toa_preamble)

    print(f"Preamble osuus kokonaisajasta: {preamble_pct:.2f}%")
    return


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
    # Tentti

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

    _lora_sf = 7
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
def _(
    EU868_DUTY_CYCLE,
    TTN_FAIR_ACCESS_LIMIT_MS,
    compute_bit_rate,
    compute_max_daily_uplinks,
    compute_time_on_air,
    math,
):
    # a. Calculate bit rate towards the Gateway
    print("A: ", compute_bit_rate(7, 125e3, 4/5))

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
    # Find my errors

    I scored only 7/16 in the exam. My fully correct answers were Kysymys 1 (answer: 293 bps) and Kysymys 4 (answer: 1 radio needed). For the last question, Kysymys 5, my first section was correct (answer: 5470 bps). Below are the wrong answers:

    ## Kysymys 2

    The answer 611 is wrong.

    ## Kysymys 3

    The 685 is wrong.

    ## Kysymys 5

    As already mentioned, the 5470 bps is CORRECT.

    All the rest are wrong: 28 ms, 1080 kpl and 3 kpl.

    Updated suggestions are: 43 ms, 698 kpl and 5 kpl.
    """)
    return


if __name__ == "__main__":
    app.run()
