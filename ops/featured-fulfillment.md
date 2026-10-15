# Featured Listing fulfillment checklist

Product: "The AI Loadout — Featured Listing" (Stripe product `prod_VRXrVcpP9oTMxR`, price `price_1UQelTL3anCVpwrEDxDffDqm`, $49/mo USD).
Payment Link: `plink_1UQelYL3anCVpwrE5rEStGg5` (https://buy.stripe.com/aFa8wQ0wa5wL6Cy7bPgEg02). It collects email, Tool name and Tool URL, then redirects to `/submit/?featured=thanks`.

What Featured means on the site (see `scripts/build.py`): the tool gets a ★ Featured badge and is pinned to the top of its loadout. **Its tier and rank do not change.** We never sell a better tier.

## On each new subscription
1. In Stripe, open the new subscription / checkout session and read the custom fields (Tool name, Tool URL) and customer email.
2. Sanity-check the tool: the URL loads, it is a real AI tool, and it fits a loadout. If it does not fit, tell Zach before doing anything (a refund is a money decision, so Zach decides).
3. If the tool is already in `tools.json`, set `"featured": true` on its entry (one entry per loadout it should be featured in).
4. If it is new, add an entry with an honest verdict, real pricing from its site, a tier/rank we would give it anyway, and `"featured": true`. Never invent facts.
5. Push `tools.json` (one batch). The Build site Action regenerates pages; confirm the tool page and loadout page return 200 and show the badge.
6. Add the tool to `newsletter/drafts/accum.md` under a "Featured" note for the next Sunday issue, labeled as featured/sponsored.
7. Log it in `ops/overnight-log.md` (date, tool, loadout). Tell Zach — a first paying customer is a big win.

## On cancellation or failed payment
1. When the subscription ends (canceled, or unpaid after Stripe's retries), remove `"featured": true` from that tool's entries.
2. Keep the tool listed at its normal tier unless it no longer earns a spot.
3. Push, verify, log.

## Checks each run (daily releases routine already reports this)
- Count active subscriptions on the Featured price. Compare to tools with `featured: true`. They should match; fix any drift and log it.

## Not set up yet (needs Zach's OK)
- A Stripe webhook that flips the flag automatically (needs a small serverless endpoint and a GitHub token).
- A public business name and support email in Stripe for this brand (the account is currently named "Web Pilot").
