# Pricing and sourcing deployment

## Build the source data

Run `node scripts/build-procurement-data.mjs chapter-14-bibliography.html data/procurement-source.json` after editing the bibliography. Review titles, categories, ISBNs, and links before publishing: automated extraction does not establish a purchasable edition or price.

## Deploy with Cloudflare Pages

1. Create a free Cloudflare account and choose **Workers & Pages → Create → Pages → Connect to Git**.
2. Select this repository and the `pricing-and-sourcing` branch. Use the repository root as the build output directory; no framework build command is required.
3. In **Settings → Variables and Secrets**, add `SERPAPI_KEY`, `EBAY_CLIENT_ID`, `EBAY_CLIENT_SECRET`, and optionally `GOOGLE_BOOKS_API_KEY` as encrypted secrets. Never put actual values in committed files.
4. Deploy. Pages serves `pricing-and-sourcing.html`; the Functions endpoints are available at `/api/prices` and `/api/access-costs`.

## Local testing

Install Wrangler, copy `.dev.vars.example` to `.dev.vars`, add only local development credentials, then run `npx wrangler pages dev . --compatibility-date=2026-08-12`.

## Price and rights rules

Only publish a lowest price after matching ISBN or exact edition, condition, currency, shipping, and retailer. Treat missing provider results as `No verified current price`. JSTOR, academic databases, school collections, archives, subscriptions, and media licensing may require institutional access or a rights quote; do not convert those states into consumer-price claims.

## Troubleshooting

- A 503 from `/api/prices` means the price-provider secret is not configured.
- Do not call retailer pages directly from browser code: it can expose keys, encounter CORS blocks, and be rate-limited.
- Add caching and provider-specific response validation before enabling public live-price results.
