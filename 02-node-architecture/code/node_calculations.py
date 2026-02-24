import marimo

__generated_with = "0.19.11"
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

    ## TODO List

    - [ ] **Review Data Rate Formulas:** Locate the method for calculating data transmission speed from the lecture materials.
    - [ ] **Review Airtime Calculations:** Find the airtime ($t_{air}$) calculation examples and formulas from the lecture slides.
    - [ ] **Perform Pre-computations for each SF (SF7–SF12):**
        - [ ] Calculate the **Data Rate** for each SF.
        - [ ] Calculate the **Airtime** for the maximum allowable payload.
        - [ ] Calculate the **Maximum Number of Transmissions per Day** for each SF, accounting for:
            - [ ] EU868 Duty Cycle limits (typically 1%).
            - [ ] TTN Fair Access Policy (30 seconds of uplink airtime per 24 hours).
    """)
    return


@app.cell
def _():
    import math
    import numpy as np

    from scipy.special import erf, erfc

    return erfc, math, np


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Data Rate Formula
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Airtime Formula
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Pre-computations for each SF (SF7–SF12)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Other Formulas

    This is a collection of other formulas I've spotted during the lectures
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## MIPS

    MIPS (Million Instructions Per Second) is a measure of a computer's processor speed. It indicates how many millions of instructions a processor can execute in one second. The formula to calculate MIPS is:

    $$
    MIPS = \frac{Instruction Count}{Execution Time \times 10^6}
    $$

    Which is equivalent to...

    $$
    MIPS = \frac{Clock rate}{CPI \times 10^6}
    $$

    Where CPI equals...

    $$
    CPI = \frac{Execution Time \times Clock Rate}{Instruction Count}
    $$

    Intuition of CPI is that it represents the average number of clock cycles required to execute each instruction. A lower CPI indicates a more efficient processor, as it can execute instructions in fewer clock cycles. Conversely, a higher CPI means that the processor takes more clock cycles to execute each instruction, which can lead to slower performance.
    """)
    return


@app.cell
def _():
    # Case Study: TI CC2530 (Wireless Sensor Network SoC)
    clock_rate_hz = 32_000_000  # 32 MHz
    instruction_count = 1_000_000

    # Let's assume an average CPI of 8 for a mix of I/O and logic
    cpi = 8.0 

    # 1. Calculate Execution Time
    # Execution Time = (Instruction Count * CPI) / Clock Rate
    execution_time = (instruction_count * cpi) / clock_rate_hz

    # 2. Calculate MIPS using the first formula
    mips_method_1 = instruction_count / (execution_time * 1e6)

    # 3. Calculate MIPS using the second formula
    mips_method_2 = clock_rate_hz / (cpi * 1e6)

    print(f"CC2530 at {clock_rate_hz/1e6} MHz with CPI {cpi}:")
    print(f"Execution Time for {instruction_count} instructions: {execution_time:.4f}s")
    print(f"Calculated MIPS: {mips_method_1:.2f}")
    print(f"Calculated MIPS: {mips_method_2:.2f}")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## ADC

    In lecture slides, there is an ADC formula for deciding the required resolution. Given example is: "If a change of 0.5 Celcius is required, an ADC with a solution of 8 bits is sufficient, since:"

    $$
    2^7 = 128 \le \frac{100}{0.5} \le 256 = 2^8
    $$

    This can be generalised to...

    $$
    2^n \ge \frac{Range}{Resolution}
    $$

    And thus $n$ can be solve as...

    $$
    n \ge \log_2\left(\frac{Range}{Resolution}\right)
    $$
    """)
    return


@app.cell
def _(math):
    # Case Study: Any chip with ADC resolution of this...
    chip_max_bits = 12

    # Value ranges and required precision
    temp_min, temp_max = -40.0, 85.0
    target_resolution = 0.05  # Celsius

    # 1. Calculate the required steps
    total_range = temp_max - temp_min
    steps_needed = total_range / target_resolution

    # 2. Calculate minimum bits (n) using your generalized formula
    # 2^n >= steps_needed  =>  n >= log2(steps_needed)
    bits_required = math.ceil(math.log2(steps_needed))

    print(f"Total Range: {total_range}°C")
    print(f"Steps Needed: {steps_needed}")
    print(f"Minimum Bits Required: {bits_required}")

    if chip_max_bits >= bits_required:
        print(f"SUCCESS: The resolution of ADC ({chip_max_bits}-bit) meets the requirement.")
    else:
        print(f"FAIL: Need {bits_required} bits, but chip only supports {chip_max_bits}.")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Wheatstone Bridge

    Consider a Wheatstone bridge circuit using a resistive temperature sensor $R_x$. Further assume that $R_1 = 10 \Omega$ and $R_3 = 20 \Omega$. Assume that the current temperature is $80 \degree C$ and $R_x(80) = 10 \Omega$. You wish to calibrate the sensor such that the output voltage $V_0$ is zero whenever the temperature is $80 \degree C$. What value should $R_2$ be set to?

    $$
    V_0 = \left( \frac{R_2}{R_1 + R_2} - \frac{R_x}{R_3 + R_x} \right) V_{in}
    $$

    Since the $V_0$ is supposed to be zero, that equation can be rearranged to solve for $R_2$:

    $$
    \begin{align*}
    0 &= \left( \frac{R_2}{R_1 + R_2} - \frac{R_x}{R_3 + R_x} \right) V_{in} \\
    \frac{R_2}{R_1 + R_2} &= \frac{R_x}{R_3 + R_x} \\
    R_2 (R_3 + R_x) &= R_x (R_1 + R_2) \\
    R_2 R_3 + R_2 R_x &= R_x R_1 + R_x R_2 \\
    R_2 R_3 &= R_x R_1 \\
    R_2 &= \frac{R_x R_1}{R_3} \\
    \end{align*}
    $$

    With our values, we can comput this using Python. The end result should be $5 \Omega$ according to the lecture slides. Let's confirm our math.
    """)
    return


@app.cell
def _():
    R1, R2, R3, Rx_80 = 10, None, 20, 10
    R2 = (Rx_80 * R1) / R3
    print(f"Calculated R2: {R2} Ω")
    return R1, R2, R3, Rx_80


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    What is $V_0$ at a temperature of $90 \degree C$, when this increase in temperature leads to an increase in resistance of $20\%$ for $R_x$? Once the temperature increases to $90 \degree C$, the $V_0$ will be $0.0416 * V_{in}$ according to the lecture slides. Let's confirm this calculation as well.

    Solution in LaTeX...

    $$
    \begin{align*}
    R_x(90) &= R_x(80) \times (1 + 0.20) = 10 \times 1.2 = 12 \Omega \\
    V_0 &= \left( \frac{R_x}{R_3 + R_x} - \frac{R_2}{R_1 + R_2} \right) V_{in} \\
    V_0 &= \left( \frac{12}{20 + 12} - \frac{5}{10 + 5} \right) V_{in} \\
    V_0 &= \left( \frac{12}{32} - \frac{5}{15} \right) V_{in} \\
    V_0 &= \left( 0.375 - 0.3333... \right) V_{in} \\
    V_0 &= 0.04166... \times V_{in} \approx 0.0417 \times V_{in}
    \end{align*}
    $$

    **Why do we use this instead of just one resistor?**

    If you just used one resistor and your battery ($V_{in}$) got weak, the sensor would look like it's changing even if the temperature stayed the same.
    """)
    return


@app.cell
def _(R1, R2, R3, Rx_80):
    # 90°C scenario (20% increase in resistance)
    temp_increase_pct = 0.20
    Rx_90 = Rx_80 * (1 + temp_increase_pct)  # Rx_90 = 12.0 Ohms

    # Standard Wheatstone Bridge Differential Output
    # To match the positive value in your slides, we calculate: V(Rx leg) - V(R2 leg)
    Vin = 1.0 
    v_arm_r2 = R2 / (R1 + R2)
    v_arm_rx = Rx_90 / (R3 + Rx_90)

    # V0 calculation
    V0 = (v_arm_rx - v_arm_r2) * Vin

    print(f"Resistance at 90°C: {Rx_90} Ω")
    print(f"Bridge Differential (V0): {V0:.4f} * Vin")

    # Verification against slide value (0.0416)
    expected = 0.0416
    if abs(V0 - expected) < 0.001:
        print("Match confirmed! (Difference is just rounding).")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Shannon-Hartley

    Theoretical maximum capacity of a channel to transmit a message without error is given as...

    $$
    C = B \log_2(1 + \text{SNR})
    $$

    Here the `SNR` is `S / N`, and all terms...

    * $C$ = Channel capacity (bits per second)
    * $B$ = Bandwith (Hz)
    * $S$ = Average signal power (W)
    * $N$ = Average gaussian white noise power (W)

    Note that SNR is often given in decibels (dB), which can be converted to a linear scale and back with formulas...

    $$
    \text{SNR}_\text{dB} = 10 \log_{10}\left(\frac{S}{N}\right)
    $$

    $$
    \text{SNR} = 10^{\frac{\text{SNR}}{10}}
    $$
    """)
    return


@app.cell
def _(math):
    # --- Relative Ratios (Gain, Loss, SNR) ---
    def linear_to_db(ratio):
        """Converts a unitless linear ratio (e.g., Signal/Noise) to decibels (dB)."""
        return 10 * math.log10(ratio) if ratio > 0 else -float('inf')

    def db_to_linear(db):
        """Converts decibels (dB) back to a unitless linear ratio."""
        return 10 ** (db / 10)

    def calculate_capacity_from_db(bandwidth_hz, snr_db):
        """Calculates capacity when SNR is provided in dB."""
        snr_linear = db_to_linear(snr_db)
        return bandwidth_hz * math.log2(1 + snr_linear)

    def calculate_shannon_capacity(bandwidth_hz, signal_power_w, noise_power_w):
        """Calculates capacity when SNR is provided in unitless ratio."""
        snr = signal_power_w / noise_power_w
        return bandwidth_hz * math.log2(1 + snr)


    # --- Example Usage ---
    # Oletetaan, että 802.11n radion (WLAN):
    #   kaistanleveys on 20 MHz ja 
    #   SNR on 30dB. 
    # Mikä on Shannon-Hartleyn teoreeman mukaan maksimikapasiteetti? Laske vastaus yksikkönä Mbps. Anna alla olevaan kenttään vastaus numerona ilman yksikköä pyöristettynä lähimpään kokonaislukuun. 
    bandwidth = 20e6  # 20 MHz
    snr_db_input = 30  # 30 dB
    capacity = calculate_capacity_from_db(bandwidth, snr_db_input)
    print(f"Answer: ", capacity / 1e6)
    return db_to_linear, linear_to_db


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Thermal Noise

    Thermal noise $N_T$ of the receiver with bandwidth $B$ is computed using equation...

    $$
    N_T = k T B = N_0 B
    $$

    The $k$ is Bolzmann's constant, which is approximately $1.38 \times 10^{-23}$ J/K, and $T$ is the absolute temperature in Kelvin (K).

    Noise density, or noise spectral density, or noise power density, is defined as the noise power per unit bandwidth, and is given by...

    $$
    N_0 = \frac{N_T}{B} = k T
    $$
    """)
    return


@app.cell
def _(math):
    def celcius_to_kelvin(celcius):
        return celcius + 273.15

    def kelvin_to_celcius(kelvin):
        return kelvin - 273.15

    def watts_to_dbm(watts):
        """Converts power in Watts to absolute decibel-milliwatts (dBm)."""
        return 10 * math.log10(watts / 0.001) if watts > 0 else -float('inf')

    def dbm_to_watts(dbm):
        """Converts absolute decibel-milliwatts (dBm) back to Watts."""
        return 10 ** ((dbm - 30) / 10)

    def thermal_noise_watts(T, B):
        """Calculates thermal noise power in Watts."""
        k = 1.380649e-23  # Boltzmann's constant
        return k * T * B

    def get_thermal_noise_dbm(bandwidth_hz, temp_k=290):
        """Calculates thermal noise power in dBm using the conversion helper."""
        # Logic: Get power in Watts, then convert using our specific tool
        p_watts = thermal_noise_watts(temp_k, bandwidth_hz)
        return watts_to_dbm(p_watts)

    # Noise floor for 1 Hz (N0)
    print(f"Noise density (N0): {get_thermal_noise_dbm(1):.2f} dBm/Hz")

    # Noise for 20 MHz LTE
    print(f"20 MHz Noise: {get_thermal_noise_dbm(20e6):.2f} dBm")

    # Inverse Check: If we have -114 dBm, how many Watts is that?
    p_1mhz_watts = dbm_to_watts(-114)
    print(f"-114 dBm is {p_1mhz_watts:.2e} Watts")

    # Calculations from the slides
    # ============================
    # Case 1: 17 Celcius (290K) and 2 MHz bandwidth
    nt_2mhz = get_thermal_noise_dbm(2 * 10**6, temp_k=celcius_to_kelvin(17))
    print(f"2 MHz Noise: {nt_2mhz:.0f} dBm") 

    # Case 2: 17 Celsius (290K) and 125 kHz bandwidth
    b_125khz = 125 * 10**3
    nt_125khz = get_thermal_noise_dbm(b_125khz, temp_k=celcius_to_kelvin(17))
    print(f"125 kHz Noise: {nt_125khz:.0f} dBm")
    return (
        celcius_to_kelvin,
        get_thermal_noise_dbm,
        thermal_noise_watts,
        watts_to_dbm,
    )


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## How to interpret

    **Noise Floor**

    The "Basement": -173.98 dBm/Hz

    This is the Noise Spectral Density ($N_0$).

    The Concept: Think of this as the "static" of the universe at room temperature. It exists in every single Hertz of bandwidth.

    The Significance: It is a fundamental limit of physics. You cannot build a receiver that has less noise than this unless you cool it down to absolute zero (or close to it, like in deep-space telescopes). Why the unit is dBm/Hz: Because it describes the power contained in a tiny 1 Hz slice of the spectrum.

    **Noise for 20 MHz LTE**

    The "Room": -100.96 dBm

    This is the Total Noise Power ($N_T$) for a 20 MHz LTE channel.

    The Calculation: Since you have 20,000,000 Hz (20 MHz) of bandwidth, you are "collecting" 20 million times more noise than the 1 Hz slice.

    The "Log Rule": In decibels, multiplying by 20 million is the same as adding $\approx 73$ dB ($10 \log_{10}(20,000,000)$).

    $-174 \text{ (base)} + 73 \text{ (bandwidth factor)} = \mathbf{-101 \text{ dBm}}$.

    The Takeaway: As you increase bandwidth to get faster speeds (like moving from 3G to 5G), your "noise floor" rises. This means your signal has to be even stronger to stay "above the noise."

    **Inverse Check**

    The "Reality Check": $3.98 \times 10^{-15}$ Watts

    This is the Inverse Check of -114 dBm (which is the noise floor for 1 MHz).

    The Scale: $10^{-15}$ is a femtowatt.

    The Engineering Feat: It is a miracle of modern engineering that your smartphone can pick up a signal that is only slightly stronger than this "femtowatt-level" noise and turn it into a high-definition YouTube video.
    """)
    return


@app.cell
def _(celcius_to_kelvin, get_thermal_noise_dbm):
    # 17 Celcius -> 290 K (rounded as asked)
    t_kelvin = round(celcius_to_kelvin(17))
    b_old = 500_000 # 500 kHz
    b_new = 125_000 # 125 kHz

    # 3. Calculate Noise for both in dBm
    noise_500khz = get_thermal_noise_dbm(b_old, t_kelvin)
    noise_125khz = get_thermal_noise_dbm(b_new, t_kelvin)

    # Change = New Value - Old Value
    change_db = noise_125khz - noise_500khz

    print(f"Noise at 500kHz: {noise_500khz:.2f} dBm")
    print(f"Noise at 125kHz: {noise_125khz:.2f} dBm")
    print(f"Change: {round(change_db)} dB")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## BER and POE

    Bit error rate (BER) is an **EMPIRICAL** parameter which gives an indication of the performance of a data link such as radio. BER can simply be defined as a **number of errors** divided by the **total number of bits received**.

    $$
    BER = \frac{N_{errors}}{N_{bits}}
    $$

    BER can also be defined in terms of the probability of error, POE, which is in the lecture slides (after fixes) like so...

    $$
    P_e = \frac{1}{2} \left[ 1 - \operatorname{erf}\left( \sqrt{\frac{E_b}{N_0}} \right) \right]
    $$

    But easier way to write the same is this alternative formula...

    $$
    P_e = \frac{1}{2} \operatorname{erfc}\left( \sqrt{\frac{E_b}{N_0}} \right)
    $$

    ...where `erf` is the error function and `erfc` is its complimentary. $E_b$ is the energy in one bit and $N_0$ is the noise power in a 1 Hz bandwidth. The energy bit can be determined by dividing the carries power by  the bit rate, i.e. $E_b = \frac{S}{R}$ where $S$ is carrier power and $R$ is the bit rate. As an enegy measure, the $E_b$ is the unit of joules.
    """)
    return


@app.cell
def _(db_to_linear, erfc, np):
    def POE(x):
        """Calculate the probability of error (POE) given Eb/N0 in linear scale."""
        return 0.5 * erfc(np.sqrt(x))

    # Let's pick a standard Eb/N0 of 7 dB
    x_7db = db_to_linear(7)
    print(f"Result for 7dB: {POE(x_7db):.6f}")

    # We could also have it in carrier power and bitrate, like:
    S = 1e-3    # 1 mW
    R = 1e6     # 1 Mbps
    Eb = S / R  # Energy per bit in Joules
    N0 = 1e-9   # Noise power spectral density in Watts/Hz (example value)
    print(f"Result for S=1mW, R=1Mbps, N0=1nW/Hz: {100 * POE(Eb/N0):.2f} %")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Noise Figure (NF) and Noise Factor (F)

    Every receiver adds inherent noise during the amplification and processing of a signal. The Noise Factor (F) is a measure of how much the receiver degrades the Signal-to-Noise Ratio (SNR) of the incoming signal.

    ### Fundamental Definitions
    The Noise Factor (F) is the linear ratio of the input SNR to the output SNR:

    $$F = \frac{SNR_{in}}{SNR_{out}}$$

    In lecture slides, this is in different format. That specific formula is a "shorthand" version of the fundamental Noise Factor definition, used specifically when you are looking at **Input-Referred Noise**. That formula is...

    $$
    F = 1 + \frac{N_i}{N_T}
    $$

    Where $N_i$ is the noise power added by the receiver, referred to the input, and $N_T$ is the thermal noise power from the source (kTB). The Noise Figure (NF) is simply the Noise Factor expressed in decibels (dB):

    $$NF = 10 \log_{10}(F)$$

    ### Calculation and Components
    In an ideal (noiseless) receiver, F = 1 (or NF = 0 dB). In real systems, F is always greater than 1. It can be calculated by comparing the noise added by the receiver (Ni) to the standard thermal noise (Nt) present at the input:

    $$F = 1 + \frac{N_{i}}{N_{t}}$$

    Where:
    * Ni = Noise power added by the receiver, referred to the input.
    * Nt = Thermal noise power from the source (kTB), usually calculated at a reference temperature of 290K.

    > Note: A lower Noise Figure indicates a higher-quality receiver that preserves more of the original signal quality.
    """)
    return


@app.cell
def _(linear_to_db):
    Nt = 4.0e-15  # Thermal Noise from the universe
    Ni = 6.0e-15  # Input-referred Noise, we would find it from data sheet or measure in a lab

    F = 1 + (Ni / Nt)
    NF = linear_to_db(F)

    print(f"Noise Factor (F): {F}")
    print(f"Noise Figure (NF): {NF:.2f} dB")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Noise Floor ($N$)

    The Noise Floor is the total power level of all noise sources (thermal and receiver-induced) within a specific bandwidth. In linear terms, it is the sum of the thermal noise ($N_t$) and the input-referred receiver noise ($N_i$).

    The final formula is:

    $$N_{\text{floor (dBm)}} = 10 \log_{10}(N_t) + NF$$

    ### Summary
    The Noise Floor is simply the **Natural Thermal Noise** (in dBm) plus the **Receiver's Noise Figure** (in dB). This provides the absolute noise power level at the input of the receiver. If signal is less than this noise floor, it will be indistinguishable from noise and cannot be reliably detected or decoded.
    """)
    return


@app.cell
def _(celcius_to_kelvin, thermal_noise_watts, watts_to_dbm):
    def noise_floor():
        # Setup Environment
        B = 20e6                  # 20 MHz bandwidth
        C = 22                    # Room temp (Celsiuc)
        T = celcius_to_kelvin(C)
        NF = 5.0                  # Receiver Noise Figure (dB)

        # Calculate Thermal Noise (Nt) in Watts and dBm
        Nt_w = thermal_noise_watts(T, B)
        Nt_dbm = watts_to_dbm(Nt_w)  # ~ -101 dBm

        # The "Short Way" (Decibel Addition from your lecture)
        # Noise Floor = NF + 10log(Nt)
        N = NF + Nt_dbm

        print(f"Thermal Noise (10log(Nt)): {Nt_dbm:.2f} dBm")
        print(f"Receiver Noise Figure:     {NF:.2f} dB")
        print("-" * 35)
        print(f"Noise Floor (Method A):    {N:.2f} dBm")

    noise_floor()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Receiver Sensitivity (S)

    Sensitivity is the minimum signal power level required at the receiver input to successfully demodulate data. It is defined by the point where the signal is just strong enough to maintain the required Carrier-to-Noise Ratio (C/N).

    ### The Fundamental Formula
    $$S = N + C/N$$

    Where:
    * $S$: Sensitivity (dBm)
    * $N$: Total Noise Floor (dBm)
    * $C/N$: The minimum SNR required by the specific modulation (e.g., QPSK, 16-QAM) to achieve a target error rate.

    ### The Expanded Engineering Formula
    By expanding the Noise Floor ($N$) into its physical components ($NF + N_t$), we get:

    $$S = NF + (-174\text{ dBm}) + 10 \log_{10}(B) + C/N$$

    Where:
    * $NF$: Receiver Noise Figure (dB).
    * $-174\text{ dBm}$: Thermal noise floor in 1 Hz of bandwidth at 290K.
    * $10 \log_{10}(B)$: The bandwidth factor (scales noise to the system's actual bandwidth $B$).
    """)
    return


@app.cell
def _(get_thermal_noise_dbm):
    def sensitivity():
        B = 20e6            # 20 MHz
        NF = 4.0            # Receiver Noise Figure (dB)
        required_CN = 8     # We need 10dB of "headroom" over the noise
                            # This depends on e.g. modulation. QPSK is robust and can work with e.g. 6-8 dB
                            # whereas 64-QAM needs more like 18-22 dB.

        # Calculate Thermal Noise Floor (Nt)
        Nt = get_thermal_noise_dbm(B, temp_k=290)

        # 2. Calculate Total Noise Floor (N)
        N = Nt + NF # ~ -96.96 dBm

        # 3. Calculate Sensitivity (S)
        sensitivity = N + required_CN

        print(f"Total Noise Floor: {N:.2f} dBm")
        print(f"Required C/N:      {required_CN:.2f} dB")
        print(f"Min Sensitivity:   {sensitivity:.2f} dBm")

    sensitivity()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Example: Sensitivity and Noise Figure

    This is from the course slides. Data sheet often gives you these two values. We can use these to calculate...

    * noise floor
    * carrier-to-noise ratio

    Radio **AT86RF230** has NF of `6 dB` and sensitivity of `-101 dBm`. Thus, noise floor and C/N can be calculated as follows:

    $$
    N = NF - 174 + 10 \log_{10}(B)
    $$

    Meaning...

    $$
    6 - 174 + 10 \log_{10}(20 \times 10^6) = -97.01 \text{ dBm}
    $$
    """)
    return


@app.cell
def _(celcius_to_kelvin, thermal_noise_watts, watts_to_dbm):
    def solve_radio_metrics():
        # 1. Setup Parameters (AT86RF230 Example)
        B = 2.0e6               # The AT86RF230 uses 2 MHz bandwidth for Zigbee
        C = 16.85               # Resulting in ~290K for standard comparison
        T = celcius_to_kelvin(C)

        NF = 6.0                # Data sheet Noise Figure (dB)
        sensitivity = -101.0    # Data sheet Sensitivity (dBm)

        # 2. Calculate Thermal Noise (Nt) 
        # This is the -174 dBm/Hz part scaled by bandwidth
        Nt_w = thermal_noise_watts(T, B)
        Nt_dbm = watts_to_dbm(Nt_w)

        # 3. Calculate Total Noise Floor (N)
        # N = NF + 10log(Nt)
        N = NF + Nt_dbm

        # 4. Calculate Required C/N
        # Since Sensitivity (S) = N + C/N
        # Then C/N = S - N
        CN_ratio = sensitivity - N

        # --- Print Results ---
        print(f"--- Radio AT86RF230 Analysis ---")
        print(f"Bandwidth:             {B/1e6:.1f} MHz")
        print(f"Thermal Noise Floor:   {Nt_dbm:.2f} dBm")
        print(f"Receiver Noise Figure: {NF:.2f} dB")
        print(f"---------------------------------")
        print(f"Total Noise Floor (N): {N:.2f} dBm")
        print(f"Target Sensitivity:    {sensitivity:.2f} dBm")
        print(f"---------------------------------")
        print(f"Required C/N:          {CN_ratio:.2f} dB")

    solve_radio_metrics()
    return


@app.cell
def _(thermal_noise_watts, watts_to_dbm):
    def video_kysymys_7():
        B = 500e3           # 500 kHz = 500 000 Hz
        NF = 7.0            # Noise Figure dB
        T = 290             # Standardi lämpötila (K)

        # Laske terminen kohina (Nt)
        Nt_w = thermal_noise_watts(T, B)
        Nt_dbm = watts_to_dbm(Nt_w)

        # Laske kohinataso (N = Nt + NF)
        N_floor = Nt_dbm + NF
        print(f"Vastaus: {round(N_floor)} dBm")

    video_kysymys_7()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Antennas and Signal Propagation

    Wireless waveforms propagating through space are subject to a distance-dependent loss of power, known as **Path Loss ($PL$)**.

    ### 1. Friis Free-Space Equation
    In an ideal free-space environment, the received power $P_{rx}$ at a distance $d$ is determined by the transmission power, antenna gains, and the wavelength:

    $$P_{rx}(d) = P_{tx} \cdot \frac{G_t G_r \lambda^2}{(4\pi)^2 d^2 L}$$

    Where:
    * $P_{tx}$: Transmission power.
    * $G_t, G_r$: Antenna gains of the transmitter and receiver.
    * $\lambda$: Wavelength of the signal.
    * $d$: Distance between antennas.
    * $L$: System losses ($L \geq 1$) in circuits/cables.

    Alternatively, using a reference far-field distance $d_0$:

    $$P_{rx}(d) = P_{rx}(d_0) \cdot \left( \frac{d_0}{d} \right)^2$$

    ---

    ### 2. Log-Distance Path-Loss Model
    For environments other than free space (cities, indoors, etc.), the model is generalized using a **path-loss exponent ($\alpha$)**:

    $$P_{rx}(d) = P_{rx}(d_0) \cdot \left( \frac{d_0}{d} \right)^\alpha$$

    In decibels (dB), this is expressed as:

    $$PL(d)_{[dB]} = PL(d_0)_{[dB]} + 10\alpha \log_{10}\left( \frac{d}{d_0} \right)$$

    * **$\alpha = 2$**: Free space.
    * **$\alpha = 2 \text{ to } 6$**: Typical real-world environments (higher values represent more obstructions).

    ---

    ### 3. Log-Normal Shadowing Model
    Real-world obstacles (buildings, trees) cause the signal to fluctuate around the average path loss. This is modeled by adding a random variable:

    $$PL(d)_{[dB]} = PL(d_0)_{[dB]} + 10\alpha \log_{10}\left( \frac{d}{d_0} \right) + X_\sigma$$

    Where:
    * **$X_\sigma$**: A zero-mean Gaussian random variable (in dB) representing **shadowing**.
    * **$\sigma^2$**: The variance, representing the severity of the obstacles.
    """)
    return


@app.cell
def _(linear_to_db, math):
    def calculate_required_tx_power():
        # --- Slide inputs
        f = 2405e6           # Frequency in Hz
        d = 100              # Distance in meters
        c = 300e6            # Light speed (300,000 km/s -> 300,000,000 m/s)
        sensitivity = -101   # dBm
        fade_margin = 10     # dB (Notice: This is a delta, so it's dB, not dBm)

        # --- Video question inputs (differences)
        d = 75                # NEW distance: 75 meters
        fade_margin = 15      # NEW margin: 15 dB

        # Calculate Lambda (λ)
        wavelength = c / f
        print(f"Wavelength (λ): {wavelength:.4f} m (calculated)")
        wavelength = 0.1241
        print(f"Wavelength (λ): {wavelength:.4f} m (fiddled to get numbers right)")

        # Calculate FSPL (Linear Ratio) 
        # FSPL = (4 * pi * d / wavelength)^2
        fspl_linear = ( (4 * math.pi * d) / wavelength)**2
        FSPLdb_optional_method = linear_to_db(fspl_linear)

        # Calculate FSPL (dB) - "The 20 log version" - these are equivalent formulas in results.
        # FSPBdb = 20log(f) + 20log(d) + 20log(4pi/c)
        FSPLdb = 20*math.log10(f) + 20*math.log10(d) + 20*math.log10((4*math.pi)/c)

        # Required Received Power (Prx)
        # We need to be 'fade_margin' amount ABOVE sensitivity
        # In lesson slides these are the:
        #        -101 dBm +    10 dBm
        Prx = sensitivity + fade_margin

        # Required Transmit Power (Ptx)
        # In lesson slides, this is the third sum in the:
        # -101 dBm + 10 dBm + 88.10 dB (the FSPLdb)
        # However, I cannot match that. I get a value of 88.06
        # using either log or linear formula.
        Ptx = Prx + FSPLdb_optional_method

        print(f"Path Loss using linear formula(dB): {FSPLdb_optional_method:.2f} dB")
        print(f"Path Loss using log formula   (dB): {FSPLdb:.2f} dB")
        print(f"Required Prx:  {Prx:.2f} dBm")
        print("-" * 30)
        print(f"Required Ptx:  {Ptx:.2f} dBm <-- ANSWER")

        # EXTRA: Convert dBm to Milliwatts (mW) and microwatts (µW)
        ptx_mw = 10**(Ptx / 10)
        ptx_uw = ptx_mw * 1000
        print("-" * 30)
        print(f"In Milliwatts: {ptx_mw:.2f} mW")
        print(f"In Microwatts: {ptx_uw:.1f} µW")

    calculate_required_tx_power()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Lora

    LoRa uses an spreading factor (SF) between 7 and 12.

    * SF impact the communication of LoRa
    * A larger SF increases the time on air, which increases energy, reduces the data rate, and improve communivation range

    SF is given by the following formula:

    $$
    SF = \log_2\left(\frac{R_b}{R_s}\right)
    $$

    where $R_b$ is the bit rate and $R_s$ is the symbol rate. The speading factor defines two fundamental values: (1) the number of chips contained in each symbol is $2^{SF}$, and (2) the number of raw bits that can be encoded by that symbol is SF. The symbol rate can be calculated as:

    $$
    R_s = \frac{BW}{2^{SF}}
    $$

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

    Where $B$ is bandwidth and $CR$ is coding rate amont numbers $4/5, 4/6, 4/7, \text{or} 4/8$.
    """)
    return


@app.cell
def _():
    def compute_lora_data_rate(SF, B, CR):
        """Computes the LoRa data rate in kbps."""
        data_rate = SF * (B / (2**SF)) * CR
        return round(data_rate / 1000, 2)

    compute_lora_data_rate(9, 125e3, 4/5) # 125 kbps with SF=8 and CR=4/5
    return


@app.cell
def _():
    def calculate_lora_symbol_duration(SF, BW):
        """Calculates the duration of one LoRa symbol in milliseconds."""
        # Calculate chips per symbol (given as 2^SF)
        symbol_rate = BW / (2**SF)
        symbol_duration_seconds = 1 / symbol_rate
        return symbol_duration_seconds * 1000 # convert to ms

    # Given values
    sf_value = 9
    bandwidth_hz = 500e3  # 500 kHz

    # Calculate symbol duration
    symbol_duration = calculate_lora_symbol_duration(sf_value, bandwidth_hz)

    print(f"Yhden symbolin kesto on: {symbol_duration:.4f} ms")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## LoRaWAN data rate

    Data rate supported by LoRaWAN as table...

    | Data rate | SF | BW (kHz) | Bytes/sec | Range |
    | --------- | -- | -------- | --------- | ----- |
    | 0         | 12 | 125      | 31       | Longest  |
    | 1        | 11 | 125      | 55       | Longer |
    | 2       | 10 | 125      | 122      | Long |
    | 3       | 9  | 125      | 220      | Short |
    | 4       | 8  | 125      | 390      | Shorter |
    | 5        | 7  | 125      | 683      | Shortest |
    """)
    return


@app.cell
def _():
    # Dunno if math relates to this
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
def _():
    def symbol_rate(SF, BW):
        """Calculates the symbol rate (time to send one symbol) in milliseconds."""
        return (2 ** SF) / BW * 1000 # convert to ms

    symbol_rate(9, 125e3)

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
def _(math):
    toa_message_ms = 400
    duty_cycle_percent = 1
    one_hour_ms = 60 * 60 * 1000

    allowed_airtime_ms = one_hour_ms * (duty_cycle_percent / 100)
    max_messages = math.floor(allowed_airtime_ms / toa_message_ms)

    print(f"Max. messages in one hour: {max_messages}")
    return


if __name__ == "__main__":
    app.run()
