#! /bin/bas/python

"""
Enterprise Value as a growing perpetuity.
"""


def value(fcff: float, r: float, t: float) -> float:
    """
    Enterprise value V, of a firm is the present value of its future free
    cash flows (FCFF) to the firms capital providers. Free cash flows are
    discounted at the firm's cost of capital (r).

    Parameters
    ----------
    fcff : float
        Future Free Cash Flow
    r : float
        Cost of Capital
    t : float
        Periods until cash flow
    """
    return fcff / (1 + r) ** t


def future_free_cash_flow(nopat: float, ic: float, g:flaot=None) -> float:
    """
    Free Cash Flow equals net operating profit after tax (nopat) minus the
    change in invested capital (delta_ic), which is the change in invested
    capital from the beginning to the end of the period.

    Parameters
    ----------
    nopat : float
        Net Operating Prtofit After Tax
    ic : float
        if g is supplied, this will equal the previous period's invested
        capital. If g is not supplied, this will equal the change in invested
        capital over the previous period.
    g : float
        invested capital growth rate, typically set to the risk-free rate.
    """
    if g is not None:
        ic = ic * g
    return nopat - ic


def return_on_invested_capital(nopat: float, ic: float) -> float:
    """
    Return on invested capital (roic) equals nopat divided by the opening
    invested capital.

    Parameters
    ----------
    nopat : float
        Net Operating Profit After Tax
    ic : float
        previous period's invested capital

    Returns
    -------
    float
        Current period Return on invested capital : float
    """
    return nopat / ic


def value_2(nopat: float, g: float, roic: float, r: float) -> float:
    """
    If growth, return on invested capital (roic), and the cost of capital (r)
    are assumed to remain constant, this expression simplifies to the growing
    perpetuity equation.

    Parameters
    ----------
    nopat : float
        future net operating profit after tax
    g : float

    roic : float
    r : float
    """
    return (nopat * (1.0 - g / roic)) / (r - g)


def economic_profit(nopat_1: , ic_0, r, f, g, t=1):
    """Economic Profit
    Relaxing condition that ROIC is constant.
    While invested capital growth rate (g) will remain constant, the spread
    of (ROIC - r), decays to zero, or mean-reverts at a fade-rate (f).
    The economic profit decays to zero when the fade rate exceeds the growth
    rate, eliminating the unrealistic assumption of perpetual excess returns.

    Parameters
    ----------
    nopat_1 : float
        Net Operating Profit After Tax in period 1.
    
    ic_0 : float
        Invested Capital in period 0. The opening enterprise book value.
    
    r : float
        Constant cost of capital. Can be set as the group average.
    
    f : float
        Fade rate. Speed at which the return on capital converges toward the
        cost of capital.
    
    g : float
        Constant growth of invested capital. Usually set to the risk-free rate
        of return

    t : float
        periods into the future

    Returns
    -------
    float
        Economic Profit
    """
    term1 = (nopat_1 / ic_0) - r
    term2 = (1 - f)**(t - 1)
    term3 = (1 + g)**(t - 1)

    return term1 * term2 * term3 * ic_0


def EV_fade(nopat_1, ic_0, r, f, g):
    """Enterprise Value with fade
    
    It is important to note that some industries intrinsically have higher
    costs than others. This is why comparing NOPATs is generally most
    meaningful among companies within the same industry, and the definition of
    a "high" or "low" ratio should be made within this context.
    """

    ep_1 = ((nopat_1 / ic_0) - r) * ic_0
    term2 = r - (1.0 + g) * (1.0 - f) + 1.0
    return ic_0 + ep_1 / term2


def EV_fade2(nopat_1, roic_1, r, f, g):
    """
    Makes things a little easier to line up since you're using the NOPAT and
    ROIC from the same period.

    The Fade rate can double as the probability of the profitability spread
    being shut off forever at each interval. The inversion of the fade rate
    would then be equivalent to the Expected Competetive Advantage Period
    (e.g. a fade rate of .5 indicates an Expected Competetive Advantage Period
    of 2 years from the initial period.)
    """
    enterprise_value = nopat_1 * (1.0 - (g - f) / roic_1)
    discount = r - g + f
    return enterprise_value / discount
