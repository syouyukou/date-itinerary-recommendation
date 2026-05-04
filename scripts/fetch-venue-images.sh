#!/usr/bin/env bash
# Re-fetch thumbnails into images/venues/ (sources at time of writing):
#   hammer, soundsgood, single-origin: Google usercontent URLs exposed by iFoodie og:image listings
#   coffee-flair: Strikingly static CDN (official coffeeflair.me)
#   d23: 聯合報系 pgw thumbnail (travel.udn.com article referenced D23 storefront)
#   luguo: Shopify theme header image on luguo Shopify storefront
#   cho: TVBS SuperTaste infocard OG image (same venue name/address scope)
#   beanroom,vwi,oasis: CYBERBIZ / official storefront OG CDN
#   orbit: Orbit Coffee Company Square Online splash asset (store.orbit.coffee)
#   wu (蕪): no stable direct URL fetched; keeps PLACES.photo = null until you drop a local file.

set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
OUT="$ROOT/images/venues"
UA="Mozilla/5.0 (compatible; VenueLocalAssets/1.0; +https://example.invalid)"
mkdir -p "$OUT"

fetch () {
  local key="$1" url="$2" dest="$3"
  echo "Fetching $key <- $url"
  curl -sfL -A "$UA" "$url" -o "$dest"
}

fetch "hammer" \
  'https://lh3.googleusercontent.com/nAtjrPtxzMmkI2tlSpvy26Ef1IRmCfUoumOlzstuUkBz_dKQYY4EqYPp4u7N8UxXMFSqtZnm7oWQyZRKyMwqHOKdPgsBUjOKsFHCyLkfzftJ=s1000' \
  "$OUT/hammer.jpeg"

fetch "coffee-flair" \
  'https://user-images.strikinglycdn.com/res/hrscywv4p/image/upload/c_limit,fl_lossy,h_630,w_1200,f_auto,q_auto/1266754/COFFEE_FLAIR_3_y0b3md.jpg' \
  "$OUT/coffee-flair.jpeg"

fetch "d23" \
  'https://pgw.udn.com.tw/gw/photo.php?u=https://uc.udn.com.tw/photo/2025/12/25/0/34040756.jpeg&s=Y&x=0&y=0&sw=1280&sh=853&exp=3600' \
  "$OUT/d23.jpeg"

fetch "luguo" \
  'https://cdn.shopify.com/s/files/1/0446/8029/files/luguo_himg_w_logo_w1200.jpg?v=11883471648995872575' \
  "$OUT/luguo.jpeg"

fetch "cho" \
  'https://cc.tvbs.com.tw/img/program/upload/2025/11/06/20251106113727-05fa9d99.jpg' \
  "$OUT/cho.jpeg"

fetch "beanroom" \
  'https://cdn-next.cybassets.com/media/W1siZiIsIjI4MzM5L2F0dGFjaGVkX3Bob3Rvcy8xNzI0MTQ4NjAzXyhiZWFucm9vbSkg5aSW6KeA54Wn54mHLmpwZy5qcGVnIl1d.jpeg?sha=cca2cb39b6cb4b7d' \
  "$OUT/beanroom.jpeg"

fetch "vwi" \
  'https://cdn-next.cybassets.com/media/W1siZiIsIjE4NDUzL2F0dGFjaGVkX3Bob3Rvcy8xNzYyNDM3Mzg3XzExMTYxLmpwZy5qcGVnIl1d.jpeg?sha=672e0487a94b0a22' \
  "$OUT/vwi.jpeg"

fetch "oasis" \
  'https://cdn-next.cybassets.com/media/W1siZiIsIjI5Mjk2L2F0dGFjaGVkX3Bob3Rvcy8xNzIxOTk1MDQ3X09BU0lTRkFUSUNPTjJf5bel5L2c5Y2A5Z-fIDEuanBnLmpwZWciXV0.jpeg?sha=ac512defa0f7a2cb' \
  "$OUT/oasis.jpeg"

fetch "orbit" \
  'https://store.orbit.coffee/uploads/b/88218730-314d-11ec-97d3-3590e647a42a/splash_2048x4435.jpg?width=1200&fit=crop' \
  "$OUT/orbit.png"

fetch "soundsgood" \
  'https://lh3.googleusercontent.com/spkmYJBHSKRe2LZR_ZGQmsJ0dlXM0xWZ1OCD6D3BrVE6ot43wsVwuc-jwZYM2qAsILxP455DsIq4DHhV3tjCJZ-KpTgcTeOVxWXPDekmhVv7sg=s1000' \
  "$OUT/soundsgood.jpeg"

fetch "single-origin" \
  'https://lh3.googleusercontent.com/AZohukDMz60dQEPAUevXX6Decy6a5uHDu-IchQOX5KoJ9TlhlpPNV_gBHxnkzQRnlkPcCI5ngXXzl2lNkljFda3IgXuQcv_IvtrnwDgpCb0=s1000' \
  "$OUT/single-origin.jpeg"

echo OK
ls -la "$OUT"
