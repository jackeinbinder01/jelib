import math


def propagation_delay(distance: float, velocity: float = 3e8) -> float:
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
        The propagation delay in seconds.

    Raises
    ------
    ValueError
        If `velocity` is less than or equal to zero.

    Examples
    --------
    >>> propagation_delay(300_000_000)  # distance in meters
    1.0
    >>> propagation_delay(1_000, velocity=2e8)
    5e-06
    """
    if velocity <= 0:
        raise ValueError("Velocity must be greater than 0.")

    return distance / velocity


def transmission_delay(packet_size: float, bandwidth: float) -> float:
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
    >>> transmission_delay(8_000_000, 1_000_000)
    8.0
    >>> transmission_delay(1_500, 1_000_000_000)  # 1500-bit packet over 1 Gbps link
    1.5e-06
    """
    if bandwidth <= 0:
        raise ValueError("Bandwidth must be greater than 0.")

    return packet_size / bandwidth


def latency(propagation_delay: float, transmission_delay: float, queue_delay: float = 0) -> float:
    """
    Compute the total one-way end-to-end latency for a packet transmission.

    This latency includes:
      • Propagation delay (physical travel time through the medium),
      • Transmission delay (time to push the packet bits onto the wire),
      • Queueing delay (time spent waiting in buffers due to congestion).

    Parameters
    ----------
    propagation_delay : float
        One-way propagation delay in seconds. Must be >= 0.
    transmission_delay : float
        Time to transmit the packet onto the link, in seconds. Must be >= 0.
    queue_delay : float, optional
        Time spent waiting in transmission queues, in seconds. Defaults to 0. Must be >= 0.

    Returns
    -------
    float
        Total one-way latency in seconds.

    Examples
    --------
    >>> latency(0.01, 0.005)
    0.015
    >>> latency(0.01, 0.005, 0.002)
    0.017
    """
    if propagation_delay < 0 or transmission_delay < 0 or queue_delay < 0:
        raise ValueError("All delay values must be non-negative.")

    return propagation_delay + transmission_delay + queue_delay


def data_in_flight(bandwidth: float, latency: float) -> float:
    """
    Compute the volume of in-flight data on a link (bandwidth-delay product).

    This represents the maximum amount of data (in bits) that can exist on the network
    at any instant — data that has been transmitted but not yet acknowledged or received.

    Parameters
    ----------
    bandwidth : float
        Link bandwidth in bits per second (bps). Must be > 0.
    latency : float
        One-way latency of the link in seconds. Must be >= 0.

    Returns
    -------
    float
        Amount of data in flight, in bits.

    Raises
    ------
    ValueError
        If `bandwidth` is less than or equal to 0, or if `latency` is negative.

    Examples
    --------
    >>> data_in_flight(1_000_000, 0.02)  # 1 Mbps, 20 ms latency
    20000.0
    """
    if bandwidth <= 0:
        raise ValueError("Bandwidth must be greater than 0.")
    if latency < 0:
        raise ValueError("Latency cannot be negative.")

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


def sliding_window_size(rtt: float, bandwidth: float) -> float:
    """
    Compute the sliding window size required to fully utilize a network link.

    This function calculates the bandwidth-delay product (BDP), which represents
    the maximum amount of data that can be in transit (in-flight) on the network
    before an acknowledgment is received. It is a fundamental concept in flow
    control protocols such as TCP sliding window.

    Parameters
    ----------
    rtt : float
        The network delay in seconds. Represents the round-trip time. Must be >= 0.
    bandwidth : float
        The link bandwidth in bits per second (bps). Must be greater than 0.

    Returns
    -------
    float
        The sliding window size in bits. Guaranteed to be >= 0.

    Raises
    ------
    ValueError
        If `bandwidth` is less than or equal to 0.
        If `rtt` is negative.

    Examples
    --------
    >>> sliding_window_size(0.1, 1_000_000)
    100000.0
    >>> sliding_window_size(0.05, 10_000_000)
    500000.0
    """
    if bandwidth <= 0:
        raise ValueError("Bandwidth must be greater than 0.")
    if rtt < 0:
        raise ValueError("Round-trip time cannot be negative.")

    return rtt * bandwidth


def round_trip_time(propagation_delay: float, transmission_delay: float = 0.0) -> float:
    """
    Compute the round-trip time (RTT) for a network connection.

    RTT represents the total time it takes for a signal to travel from the sender
    to the receiver and back again. It is commonly used in latency, congestion control,
    and sliding window calculations.

    Parameters
    ----------
    propagation_delay : float
        One-way propagation delay in seconds. Represents how long a signal
        takes to travel across the medium from source to destination. Must be >= 0.
    transmission_delay : float, optional
        Additional delay due to the time required to place the packet onto the link
        (in seconds). Defaults to 0. Must be >= 0.

    Returns
    -------
    float
        Round-trip time (RTT) in seconds.

    Raises
    ------
    ValueError
        If `propagation_delay` or `transmission_delay` is negative.

    Examples
    --------
    >>> round_trip_time(0.05)
    0.1
    >>> round_trip_time(0.02, transmission_delay=0.005)
    0.045
    """
    if propagation_delay < 0:
        raise ValueError("Propagation delay cannot be negative")
    if transmission_delay < 0:
        raise ValueError("Transmission delay cannot be negative")

    return 2 * propagation_delay + transmission_delay

def transfer_time(rtt: float, file_size: float, bandwidth: float) -> float:
    """
    Compute the total time required to transfer a file over a network connection.

    This calculation uses a simplified model where the transfer time consists of one
    round-trip time (RTT) of latency plus the time required to transmit the entire file
    at a constant bandwidth. It assumes an ideal network with no congestion, packet loss,
    or protocol overhead, and is commonly used in theoretical throughput and latency
    analysis.

    Parameters
    ----------
    rtt : float
        Round-trip time in seconds. Represents the latency between the sender and receiver,
        including propagation and processing delays. Must be >= 0.
    file_size : float
        Size of the file to be transferred, in bytes (or bits if bandwidth is expressed in bits/s).
        Must be >= 0.
    bandwidth : float
        Available network bandwidth in bytes per second (or bits per second if matching units with file_size).
        Must be > 0.

    Returns
    -------
    float
        Total file transfer time in seconds.

    Raises
    ------
    ValueError
        If `rtt` or `file_size` is negative, or if `bandwidth` is less than or equal to zero.

    Examples
    --------
    >>> transfer_time(0.1, file_size=1_000_000, bandwidth=10_000_000)
    0.2
    >>> transfer_time(0.05, file_size=500_000, bandwidth=5_000_000)
    0.15
    """
    if bandwidth <= 0:
        raise ValueError("Bandwidth must be greater than 0.")
    if file_size < 0:
        raise ValueError("File size cannot be negative.")
    if rtt < 0:
        raise ValueError("Round-trip time cannot be negative.")

    return rtt + (file_size / bandwidth)


def stop_and_wait_utilization(transmission_delay: float, rtt: float) -> float:
    """
    Compute the link utilization for a stop-and-wait protocol.

    Utilization represents the fraction of time the sender is actively transmitting data
    on the link, as opposed to waiting for acknowledgments. This simplified model assumes
    a single outstanding frame at a time and calculates utilization using the ratio of
    transmission time to the total cycle time (transmission plus round-trip delay).

    Parameters
    ----------
    transmission_delay : float
        Time required to place the entire frame onto the link (in seconds). Must be >= 0.
    rtt : float
        Round-trip time in seconds, including propagation and acknowledgment delays.
        Represents the waiting period before the sender can transmit the next frame.
        Must be >= 0.

    Returns
    -------
    float
        Link utilization as a value between 0 and 1, where 0 means the link is idle and
        1 means it is being used continuously for transmission.

    Raises
    ------
    ValueError
        If `transmission_delay` or `rtt` is negative, or if both are zero.

    Examples
    --------
    >>> stop_and_wait_utilization(0.01, rtt=0.09)
    0.1
    >>> stop_and_wait_utilization(0.05, rtt=0.05)
    0.5
    """
    if transmission_delay < 0:
        raise ValueError("Transmission cannot be negative.")
    if rtt < 0:
        raise ValueError("Round-trip time cannot be negative.")
    if transmission_delay == 0 and rtt == 0:
        raise ValueError("Both transmission_delay and rtt cannot be zero.")

    return transmission_delay / (transmission_delay + rtt)


def sliding_window_utilization(window_size: int, rtt: float, bandwidth: float) -> float:
    """
    Compute the link utilization for a sliding window protocol.

    Utilization represents the efficiency of data transmission when multiple frames can be
    in transit before waiting for acknowledgments. This model accounts for pipelining and
    becomes optimal when the window size is large relative to the bandwidth-delay product.

    Parameters
    ----------
    window_size : int
        The number of frames (or bytes) that can be sent without waiting for an acknowledgment.
        Must be > 0.
    rtt : float
        Round-trip time in seconds, representing the total time from sending a packet to
        receiving its acknowledgment. Must be >= 0.
    bandwidth : float
        Available bandwidth in bytes per second (or bits per second if matching units with
        window_size). Must be > 0.

    Returns
    -------
    float
        Link utilization as a value between 0 and 1. A utilization of 1.0 indicates the link
        is fully utilized with no idle time.

    Raises
    ------
    ValueError
        If `window_size` is less than or equal to zero, or if `rtt` or `bandwidth` is negative.

    Examples
    --------
    >>> sliding_window_utilization(10, rtt=0.1, bandwidth=1_000_000)
    0.99...
    >>> sliding_window_utilization(5, rtt=0.05, bandwidth=500_000)
    0.99...
    """
    if window_size < 0:
        raise ValueError("Window size cannot be negative.")
    if rtt < 0:
        raise ValueError("Round-trip time cannot be negative.")
    if bandwidth < 0:
        raise ValueError("Bandwidth cannot be negative.")
    if rtt == 0 and bandwidth == 0:
        raise ValueError("Both round-trip time and bandwidth cannot be zero.")

    return window_size / (window_size + rtt * bandwidth)
