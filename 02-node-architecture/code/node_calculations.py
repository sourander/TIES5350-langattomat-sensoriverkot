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

    return (math,)


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


if __name__ == "__main__":
    app.run()
