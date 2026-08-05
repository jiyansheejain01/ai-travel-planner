import asyncio
import json
from pathlib import Path

import httpx

from app.agents.hotel.tools.hotelbeds_client import HotelbedsClient


OUTPUT_FILE = (
    Path(__file__).parent
    / "app"
    / "data"
    / "hotelbeds"
    / "hotels.json"
)

PROGRESS_FILE = (
    Path(__file__).parent
    / "app"
    / "data"
    / "hotelbeds"
    / "sync_progress.json"
)

BATCH_SIZE = 1000


def load_existing_hotels() -> list[dict]:
    """Load hotels already downloaded."""

    if not OUTPUT_FILE.exists():
        return []

    try:
        with OUTPUT_FILE.open(
            "r",
            encoding="utf-8",
        ) as file:
            data = json.load(file)

        if isinstance(data, list):
            return data

    except (json.JSONDecodeError, OSError):
        pass

    return []


def save_hotels(hotels: list[dict]) -> None:
    """Save current progress to disk."""

    OUTPUT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    # Write to temporary file first so an interrupted write
    # does not corrupt the real cache.
    temp_file = OUTPUT_FILE.with_suffix(".tmp")

    with temp_file.open(
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(
            hotels,
            file,
            ensure_ascii=False,
        )

    temp_file.replace(OUTPUT_FILE)

def load_progress() -> int:
    """Load the next HBX pagination position."""

    if not PROGRESS_FILE.exists():
        return 1

    try:
        with PROGRESS_FILE.open(
            "r",
            encoding="utf-8",
        ) as file:
            data = json.load(file)

        return int(data.get("next_start", 1))

    except (json.JSONDecodeError, OSError, ValueError, TypeError):
        return 1


def save_progress(next_start: int) -> None:
    """Save the next HBX pagination position."""

    PROGRESS_FILE.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    temp_file = PROGRESS_FILE.with_suffix(".tmp")

    with temp_file.open(
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(
            {
                "next_start": next_start,
            },
            file,
            indent=2,
        )

    temp_file.replace(PROGRESS_FILE)

async def main():

    client = HotelbedsClient()

    # ---------------------------------------------------------
    # Load previous progress
    # ---------------------------------------------------------

    all_hotels = load_existing_hotels()

    existing_codes = {
        str(hotel.get("code"))
        for hotel in all_hotels
        if hotel.get("code") is not None
    }

    # Resume after however many records we already have.
    start = load_progress()

    print()
    print("=" * 60)
    print("HBX HOTEL CONTENT SYNC")
    print("=" * 60)

    if all_hotels:
        print(f"Existing hotels: {len(all_hotels)}")
        print(f"Resuming from: {start}")
    else:
        print("No existing cache found.")
        print("Starting from hotel 1.")

    print()

    # ---------------------------------------------------------
    # Download batches
    # ---------------------------------------------------------

    while True:

        end = start + BATCH_SIZE - 1

        print(
            f"Fetching hotels {start}-{end}..."
        )

        try:

            result = await client.get_hotels(
                start=start,
                end=end,
            )

        except httpx.HTTPStatusError as exc:

            status = exc.response.status_code

            print()
            print("=" * 60)
            print("HBX REQUEST STOPPED")
            print("=" * 60)
            print(f"HTTP status: {status}")

            try:
                print(
                    "Response:",
                    exc.response.json(),
                )
            except Exception:
                print(
                    "Response:",
                    exc.response.text,
                )

            print()
            print(
                f"Hotels safely cached: "
                f"{len(all_hotels)}"
            )

            print(
                f"Next resume position: {start}"
            )

            print(
                f"Cache file: {OUTPUT_FILE}"
            )

            # Everything before the failed request
            # has already been saved.
            break

        except Exception as exc:

            print()
            print("Unexpected error:")
            print(repr(exc))

            print(
                f"Hotels safely cached: "
                f"{len(all_hotels)}"
            )

            break

        # -----------------------------------------------------
        # Extract batch
        # -----------------------------------------------------

        hotels = result.get(
            "hotels",
            [],
        )

        if not hotels:

            print()
            print("No more hotels returned.")
            break

        # -----------------------------------------------------
        # Prevent duplicate hotel codes
        # -----------------------------------------------------

        added = 0

        for hotel in hotels:

            code = hotel.get("code")

            if code is None:
                continue

            code = str(code)

            if code in existing_codes:
                continue

            all_hotels.append(hotel)

            existing_codes.add(code)

            added += 1

        # -----------------------------------------------------
        # SAVE IMMEDIATELY
        # -----------------------------------------------------

        save_hotels(all_hotels)

        next_start = start + BATCH_SIZE
        save_progress(next_start)

        print(
            f"Received {len(hotels)} hotels | "
            f"Added {added} | "
            f"Total cached: {len(all_hotels)}"
        )

        print(
            f"Progress saved. Next batch starts at {next_start}."
        )

        # -----------------------------------------------------
        # Last page
        # -----------------------------------------------------

        if len(hotels) < BATCH_SIZE:
            print()
            print("Final HBX page reached.")
            break

        start += BATCH_SIZE

    # ---------------------------------------------------------
    # Final save
    # ---------------------------------------------------------

    save_hotels(all_hotels)

    print()
    print("=" * 60)
    print("HBX HOTEL CACHE FINISHED")
    print("=" * 60)

    print(
        f"Hotels cached: {len(all_hotels)}"
    )

    print(
        f"Saved to: {OUTPUT_FILE}"
    )


if __name__ == "__main__":
    asyncio.run(main())