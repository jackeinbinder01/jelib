import math


def propagation_time(distance: float, velocity: float = 3e8) -> float:
    """
    Calculate the propagation delay of a signal traveling a given distance.

    Parameters
    ----------
    distance : float
        The distance the signal travels, in meters.
    velocity : float, optional
        The propagation velocity of the signal, in meters per second.
        Defaults to the speed of light in a vacuum (3e8 m/s).

    Returns
    -------
    float
        The time delay in seconds.

    Raises
    ------
    ValueError
        If `velocity` is less than or equal to zero.

    Examples
    --------
    >>> propagation_time(300_000_000)  # distance in meters
    1.0
    >>> propagation_time(1_000, velocity=2e8)
    5e-06
    """
    if velocity <= 0:
        raise ValueError("Velocity must be greater than 0.")
    return distance / velocity


def transmission_time(packet_size: float, bandwidth: float) -> float:
    """
    Calculate the transmission delay for a data packet over a network link.

    Parameters
    ----------
    packet_size : float
        The size of the data packet in bits.
    bandwidth : float
        The transmission rate of the network link in bits per second (bps).

    Returns
    -------
    float
        The transmission time in seconds.

    Raises
    ------
    ValueError
        If `bandwidth` is less than or equal to 0.

    Examples
    --------
    >>> transmission_time(8_000_000, 1_000_000)
    8.0
    >>> transmission_time(1_500, 1_000_000_000)  # 1500-bit packet over 1 Gbps link
    1.5e-06
    """
    if bandwidth <= 0:
        raise ValueError("Bandwidth must be greater than 0.")
    return packet_size / bandwidth


def latency(propagation_time: float, transmission_time: float, queue_delay: float) -> float:
    """
    Calculate the total end-to-end latency for a packet transmission.

    Parameters
    ----------
    propagation_time : float
        The time it takes for a signal to travel from sender to receiver across the medium, in seconds.
    transmission_time : float
        The time required to push all packet bits onto the link, in seconds.
    queue_delay : float
        The time the packet spends waiting in queue before transmission, in seconds.

    Returns
    -------
    float
        The total latency in seconds.

    Examples
    --------
    >>> latency(0.01, 0.005, 0.002)
    0.017
    """
    return propagation_time + transmission_time + queue_delay


def data_in_flight(bandwidth: float, latency: float) -> float:
    """
    Calculate the amount of data in flight on a network link.

    This represents the volume of data that has been transmitted but not yet received,
    based on the bandwidth and one-way latency of the link.

    Parameters
    ----------
    bandwidth : float
        The bandwidth of the network link in megabits per second (Mbps).
    latency : float
        The one-way latency of the link in seconds.

    Returns
    -------
    float
        The amount of data in flight in megabits (Mb).

    Examples
    --------
    >>> data_in_flight(100, 0.02)  # 100 Mbps bandwidth, 20 ms latency
    2.0
    """
    return bandwidth * latency


def wavelength(speed: float, frequency: float) -> float:
    """
    Calculate the wavelength of a signal based on its propagation speed and frequency.

    Parameters
    ----------
    speed : float
        The propagation speed of the wave in meters per second (m/s).
        For example, the speed of light in a vacuum is approximately 3e8 m/s.
    frequency : float
        The frequency of the signal in hertz (Hz). Must be greater than 0.

    Returns
    -------
    float
        The wavelength in meters (m).

    Raises
    ------
    ValueError
        If `frequency` is less than or equal to 0.

    Examples
    --------
    >>> wavelength(3e8, 1e9)  # 1 GHz signal in free space
    0.3
    >>> wavelength(3e8, 2.4e9)  # 2.4 GHz Wi-Fi signal
    0.125
    """
    if frequency <= 0.0:
        raise ValueError("Frequency must be greater than 0.")
    return speed / frequency


def snr_db_to_linear(snr_db: float) -> float:
    """
    Convert signal-to-noise ratio from decibels (dB) to linear scale.

    Parameters
    ----------
    snr_db : float
        The signal-to-noise ratio in decibels (dB).

    Returns
    -------
    float
        The signal-to-noise ratio in linear (unitless) form.

    Examples
    --------
    >>> snr_db_to_linear(10)
    10.0
    >>> snr_db_to_linear(0)
    1.0
    """
    return 10 ** (snr_db / 10)


def channel_capacity(bandwidth: float, snr_linear: float) -> float:
    """
    Calculate the maximum theoretical channel capacity using the Shannon-Hartley theorem.

    The Shannon capacity represents the upper limit on the error-free data rate
    of a communication channel given its bandwidth and signal-to-noise ratio.

    Parameters
    ----------
    bandwidth : float
        The channel bandwidth in Hertz (Hz). Must be greater than 0.
    snr_linear : float
        The signal-to-noise ratio in linear scale (unitless). Must be non-negative.

    Returns
    -------
    float
        The channel capacity in bits per second (bps).

    Raises
    ------
    ValueError
        If `bandwidth` is less than or equal to 0.
        If `snr_linear` is negative.

    Examples
    --------
    >>> channel_capacity(3_000, 10)
    10378.2...
    """
    if bandwidth <= 0:
        raise ValueError("Bandwidth must be greater than 0.")
    if snr_linear < 0:
        raise ValueError("SNR (linear) cannot be negative.")
    return bandwidth * math.log2(1 + snr_linear)


def channel_capacity_db(bandwidth: float, snr_db: float) -> float:
    """
    Calculate the channel capacity using the Shannon-Hartley theorem with SNR specified in decibels.

    Parameters
    ----------
    bandwidth : float
        The channel bandwidth in Hertz (Hz). Must be greater than 0.
    snr_db : float
        The signal-to-noise ratio in decibels (dB).

    Returns
    -------
    float
        The channel capacity in bits per second (bps).

    Raises
    ------
    ValueError
        If `bandwidth` is less than or equal to 0.

    Examples
    --------
    >>> channel_capacity_db(3_000, 20)
    19974.6...
    """
    snr_linear = snr_db_to_linear(snr_db)
    return channel_capacity(bandwidth, snr_linear)


def required_snr(capacity: float, bandwidth: float) -> float:
    """
    Compute the minimum required signal-to-noise ratio (SNR) to achieve a target capacity.

    This function inverts the Shannon-Hartley theorem to solve for the linear SNR.

    Parameters
    ----------
    capacity : float
        The target channel capacity in bits per second (bps). Must be non-negative.
    bandwidth : float
        The available channel bandwidth in Hertz (Hz). Must be greater than 0.

    Returns
    -------
    float
        The required SNR in linear scale (unitless). Guaranteed to be >= 0.

    Raises
    ------
    ValueError
        If `bandwidth` is less than or equal to 0.
        If `capacity` is negative.

    Examples
    --------
    >>> required_snr(10_000, 3_000)
    9.0...
    """
    if bandwidth <= 0:
        raise ValueError("Bandwidth must be greater than 0.")
    if capacity < 0:
        raise ValueError("Capacity cannot be negative.")
    snr = 2 ** (capacity / bandwidth) - 1
    return max(snr, 0.0)



