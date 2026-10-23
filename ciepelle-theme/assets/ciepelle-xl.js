/* Ciepelle : tailles L et XL -> variante "220 g XL" (commandee chez le fournisseur en XL 60-90 kg).
   S, M -> variante "220 g" (fournisseur L 40-70 kg / taille unique). Invisible pour la cliente : meme prix, meme produit. */
(function () {
  function pick(list, test) { for (var i = 0; i < list.length; i++) { if (test(list[i])) return list[i]; } return null; }
  document.addEventListener('submit', function (e) {
    var f = e.target;
    if (!f || !f.querySelector) return;
    var size = f.querySelector('[data-size-input]');
    var vi = f.querySelector('input[name="id"]');
    if (!size || !vi || !size.value) return;
    var xl = size.value === 'XL' || size.value === 'L';
    try {
      var pj = document.querySelector('[data-product-json]');
      var tj = document.querySelector('[data-trio-json]');
      if (pj && f.querySelector('[data-variant-input]')) {
        var d = JSON.parse(pj.textContent);
        var v = pick(d.variants, function (x) { return String(x.id) === vi.value; });
        if (!v) return;
        var base = String(v.o3).replace(/ XL$/, '');
        var want = xl ? base + ' XL' : base;
        var t = pick(d.variants, function (x) { return x.o1 === v.o1 && x.o2 === v.o2 && x.o3 === want && x.available; });
        if (t) vi.value = t.id;
      } else if (tj && f.querySelector('[data-trio-input]')) {
        var td = JSON.parse(tj.textContent);
        var tv = pick(td.variants, function (x) { return String(x.id) === vi.value; });
        if (!tv) return;
        var tbase = String(tv.w).replace(/ XL$/, '');
        var twant = xl ? tbase + ' XL' : tbase;
        var tt = pick(td.variants, function (x) { return x.w === twant && x.available; });
        if (tt) vi.value = tt.id;
      }
    } catch (err) {}
  }, true);
  function cleanCart() {
    var els = document.querySelectorAll('.cart-item__meta');
    for (var i = 0; i < els.length; i++) {
      var el = els[i];
      if (el.children.length === 0 && /220 g XL/.test(el.textContent)) el.textContent = el.textContent.replace('220 g XL', '220 g');
    }
  }
  cleanCart();
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', cleanCart);
})();
