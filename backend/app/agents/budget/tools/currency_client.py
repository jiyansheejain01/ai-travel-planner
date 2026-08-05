import asyncio

import httpx


class CurrencyClient:
    """
    Thin HTTP client for the Frankfurter exchange-rate API.

    Frankfurter is free, open-source, and requires no API key or signup:
    https://frankfurter.dev/. It's kept behind this client (and, one
    layer up, behind CurrencyService) so the provider can be swapped
    later without touching any agent code.
    """

    BASE_URL = "https://api.frankfurter.dev/v1/latest"

    TIMEOUT = 10.0
    MAX_RETRIES = 2

    async def get_rate(
        self,
        base: str,
        symbol: str,
    ) -> float:
        """
        Return the exchange rate that converts 1 unit of `base` into `symbol`.
        """

        if base == symbol:
            return 1.0

        last_exception = None

        for attempt in range(self.MAX_RETRIES + 1):

            try:
                timeout = httpx.Timeout(
                    self.TIMEOUT,
                    connect=self.TIMEOUT,
                )

                async with httpx.AsyncClient(
                    timeout=timeout,
                ) as client:

                    response = await client.get(
                        self.BASE_URL,
                        params={
                            "base": base,
                            "symbols": symbol,
                        },
                    )

                    response.raise_for_status()

                    data = response.json()

                    rate = data.get("rates", {}).get(symbol)

                    if rate is None:
                        raise ValueError(
                            f"Frankfurter did not return a rate for "
                            f"{base} -> {symbol}."
                        )

                    return float(rate)

            except (
                httpx.TimeoutException,
                httpx.ConnectError,
                httpx.NetworkError,
            ) as exc:

                last_exception = exc

                # No more retries left
                if attempt >= self.MAX_RETRIES:
                    break

                # Small delay before retrying
                await asyncio.sleep(1)

            except httpx.HTTPStatusError as exc:

                status_code = exc.response.status_code

                raise RuntimeError(
                    f"Currency exchange API returned HTTP "
                    f"{status_code}: "
                    f"{exc.response.text}"
                ) from exc

        # If all retry attempts failed
        raise RuntimeError(
            "Currency exchange service could not be reached "
            f"after {self.MAX_RETRIES + 1} attempts. "
            f"Last error: "
            f"{type(last_exception).__name__}"
        ) from last_exception
