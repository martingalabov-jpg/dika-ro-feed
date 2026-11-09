# DiKa RO - Google Merchant Center feed

`feed.tsv` is rebuilt daily by GitHub Actions from DiKa's catalogue CSV
(`images.dika.com/catalogues/3000/meta-pixel/general-ro.csv`) and fetched by Merchant Center (account 5753407031) from:

https://raw.githubusercontent.com/OWNER/dika-ro-feed/main/feed.tsv

Changes vs. source: Google-format prices, `sale_price` only when lower than `price`,
`internal_label` -> `custom_label_3`, and per-item `shipping` (Fan Courier, 25 RON under 500 RON, free from 500 RON, 2-6 business days).
Run manually: Actions -> Update DiKa RO feed -> Run workflow.
