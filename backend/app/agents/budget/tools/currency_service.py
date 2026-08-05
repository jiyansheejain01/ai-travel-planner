from __future__ import annotations

import time

from app.agents.budget.tools.currency_client import CurrencyClient


class CurrencyService:
    """
    Reusable currency-conversion service.

    Kept behind this interface -- rather than calling CurrencyClient
    directly from BudgetTool/BudgetAgent -- so the underlying provider
    (currently Frankfurter, see currency_client.py) can be replaced
    later without changing any agent code.
    """

    # Frankfurter publishes rates once per business day, so caching for
    # an hour avoids refetching the same pair repeatedly within a run
    # without ever serving meaningfully stale data.
    CACHE_TTL_SECONDS = 60 * 60

    def __init__(
        self,
        client: CurrencyClient | None = None,
    ) -> None:

        self.client = client or CurrencyClient()

        self._rate_cache: dict[tuple[str, str], tuple[float, float]] = {}

    async def _get_rate(
        self,
        from_currency: str,
        to_currency: str,
    ) -> float:

        from_currency = from_currency.upper()
        to_currency = to_currency.upper()

        cache_key = (from_currency, to_currency)

        cached = self._rate_cache.get(cache_key)

        if cached is not None:

            rate, cached_at = cached

            if time.monotonic() - cached_at < self.CACHE_TTL_SECONDS:
                return rate

        rate = await self.client.get_rate(
            from_currency,
            to_currency,
        )

        self._rate_cache[cache_key] = (rate, time.monotonic())

        return rate

    async def convert(
        self,
        amount: float,
        from_currency: str,
        to_currency: str,
    ) -> float:
        """
        Convert `amount` from `from_currency` to `to_currency`.

        Do NOT hardcode exchange rates -- this always goes through the
        live rate (subject to the short cache above).
        """

        if not from_currency or not to_currency:
            raise ValueError(
                "Both from_currency and to_currency are required."
            )

        from_currency = from_currency.upper()
        to_currency = to_currency.upper()

        if from_currency == to_currency:
            return round(amount, 2)

        rate = await self._get_rate(
            from_currency,
            to_currency,
        )

        return round(amount * rate, 2)
