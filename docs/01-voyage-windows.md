# 1. Voyage Windows — When the Endeavor Sails

*Ocean fishing is a friendly duty: you queue up, board The Endeavor, and cast for about thirty
minutes while the crew does all the steering. No gear grinding, no complicated timers — you just
need to know when the boat leaves.*

**Hand-maintained, not automated.** This project uses no sniffing, no scraping, and no account
data. Every table here is written and updated by a real person, and each one is stamped with the
date it was last hand-checked against the live game.

Last hand-checked: **2026-10-31**

## Booking your trip

1. Board as a **Fisher** (any level that has unlocked the duty works, and the voyage is one of the
   friendliest sources of fisher experience in the game).
2. Open the **Duty Finder** and find **Ocean Fishing**.
3. Join the queue. Parties are filled with other fishers from your data center — it is very social.
4. When the duty pops, say hello in chat, pick your spot on the deck, and cast when you're ready.

## Departure schedule (plain table)

Ocean fishing departures repeat on a fixed clock. Confirm the current pattern from your in-game
Duty Finder tile, then write it down here so future-you doesn't have to remember. If Square Enix
adjusts the schedule in a patch, just update the table and move the verify date.

| Day | First departure (UTC) | Notes |
| --- | --- | --- |
| All days | Fill in from your Duty Finder tile | Voyages repeat on a fixed interval (commonly reported as roughly every two hours) |

**Verify tip:** check the times shown on the Ocean Fishing duty entry on two different days. If
they match, the schedule is a fixed clock — record it in the table above and stamp the verify
date. If they ever seem to drift, trust the game (and patch notes), not your memory, and tell us
via a pull request.

## What actually happens on the boat

- The voyage is roughly **30 minutes**: usually three stretches of open water, each with its own
  school of fish, and the crew announcing what's biting.
- Everyone on deck earns from the same catches — there's no competition for one fish, so nobody
  is racing you. You can also see your fellow fishers' catches and points in a shared tally.
- **Spectral waters** can roll in mid-voyage: the water glitters, rarer fish show up, and the
  whole boat usually goes a little bit feral with excitement. Enjoy it whether or not you catch
  anything fancy.
- The voyage ends with a scoreboard of everyone's points. "Team North America" versus "Team
  Everything Else"? It rotates — don't take the team names too seriously, and do take the
  congratulations seriously.

## Expectation setting, kindly

If it's your first voyage: your goal is simply **to finish the trip with any points at all**.
Bronze. That's a real, good, complete goal. Everything past that is a pleasant bonus.

## Testing, verification and hand-editing trail

- This file is plain Markdown under `docs/`, converted to HTML by the project's build script.
- Tables carry a hand-check stamp; if the ship's schedule changes, update both the table and the
  stamp in the same commit.
- The build is fully local: no network calls, no telemetry, no logins. See `README.md`.
