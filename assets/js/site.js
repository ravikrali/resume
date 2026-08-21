/* Ravi Kiran Rali — site behaviour.
   No dependencies. Progressive: everything works without JS except the
   roadmap accordion, which degrades to all-panels-open via .no-js. */

(function () {
  'use strict';

  document.documentElement.classList.remove('no-js');

  /* ---- masthead shadow on scroll ------------------------------------- */
  var head = document.querySelector('.masthead');
  if (head) {
    var onScroll = function () {
      head.classList.toggle('is-stuck', window.scrollY > 12);
    };
    onScroll();
    window.addEventListener('scroll', onScroll, { passive: true });
  }

  /* ---- scroll reveals ------------------------------------------------ */
  var risers = document.querySelectorAll('.rise');
  if (risers.length) {
    if ('IntersectionObserver' in window) {
      var io = new IntersectionObserver(function (entries) {
        entries.forEach(function (e) {
          if (!e.isIntersecting) return;
          e.target.classList.add('is-in');
          io.unobserve(e.target);
        });
      }, { rootMargin: '0px 0px -8% 0px', threshold: 0.06 });
      risers.forEach(function (el) { io.observe(el); });
      /* Belt and braces: nothing stays invisible, whatever the browser does. */
      window.setTimeout(function () {
        risers.forEach(function (el) { el.classList.add('is-in'); });
      }, 2000);
    } else {
      risers.forEach(function (el) { el.classList.add('is-in'); });
    }
  }

  /* ---- roadmap ------------------------------------------------------- */
  var rm = document.querySelector('[data-roadmap]');
  if (rm) {
    var items = Array.prototype.slice.call(rm.querySelectorAll('.rm__item'));
    var dots  = Array.prototype.slice.call(document.querySelectorAll('.ribbon__dot'));

    function syncRibbon(id) {
      dots.forEach(function (d) {
        d.setAttribute('aria-current', String(d.dataset.target === id));
      });
    }

    /* Animate a panel between 0 and its content height. Settling on `auto`
       after opening keeps it correct when the viewport is resized. */
    function slide(item, shouldOpen, instant) {
      var panel = item.querySelector('.rm__panel');
      var inner = item.querySelector('.rm__panelin');
      if (!panel || !inner) return;

      if (panel._slideEnd) {
        panel.removeEventListener('transitionend', panel._slideEnd);
        panel._slideEnd = null;
      }

      if (instant) {
        panel.style.transition = 'none';
        panel.style.height = shouldOpen ? 'auto' : '0px';
        panel.offsetHeight;                       // flush
        panel.style.transition = '';
        return;
      }

      panel.style.height = panel.offsetHeight + 'px';
      panel.offsetHeight;                         // flush, so the change animates
      panel.style.height = (shouldOpen ? inner.offsetHeight : 0) + 'px';

      if (shouldOpen) {
        panel._slideEnd = function (ev) {
          if (ev.target !== panel || ev.propertyName !== 'height') return;
          panel.style.height = 'auto';
          panel.removeEventListener('transitionend', panel._slideEnd);
          panel._slideEnd = null;
        };
        panel.addEventListener('transitionend', panel._slideEnd);
      }
    }

    function open(item, opts) {
      opts = opts || {};
      items.forEach(function (other) {
        var isTarget = other === item;
        var wasOpen = other.classList.contains('is-open');
        other.classList.toggle('is-open', isTarget);
        var btn = other.querySelector('.rm__head');
        if (btn) btn.setAttribute('aria-expanded', String(isTarget));
        if (isTarget || wasOpen) slide(other, isTarget, opts.instant);
      });
      syncRibbon(item.id);

      if (opts.scroll) {
        var top = item.getBoundingClientRect().top + window.scrollY - 96;
        window.scrollTo({
          top: top,
          behavior: window.matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth'
        });
      }
      if (opts.hash) {
        history.replaceState(null, '', '#' + item.id);
      }
    }

    function close(item) {
      item.classList.remove('is-open');
      var btn = item.querySelector('.rm__head');
      if (btn) btn.setAttribute('aria-expanded', 'false');
      slide(item, false, false);
      syncRibbon(null);
    }

    items.forEach(function (item) {
      var btn = item.querySelector('.rm__head');
      if (!btn) return;
      btn.addEventListener('click', function () {
        if (item.classList.contains('is-open')) { close(item); return; }
        open(item, { hash: true });
      });
    });

    dots.forEach(function (dot) {
      dot.addEventListener('click', function () {
        var target = document.getElementById(dot.dataset.target);
        if (target) open(target, { scroll: true, hash: true });
      });
    });

    /* keyboard: up/down moves between milestone headers */
    rm.addEventListener('keydown', function (ev) {
      if (ev.key !== 'ArrowDown' && ev.key !== 'ArrowUp') return;
      var heads = items.map(function (i) { return i.querySelector('.rm__head'); });
      var idx = heads.indexOf(document.activeElement);
      if (idx === -1) return;
      ev.preventDefault();
      var next = heads[idx + (ev.key === 'ArrowDown' ? 1 : -1)];
      if (next) next.focus();
    });

    /* deep link, else open the most recent milestone */
    var fromHash = window.location.hash ? document.getElementById(window.location.hash.slice(1)) : null;
    if (fromHash && fromHash.classList.contains('rm__item')) {
      open(fromHash, { scroll: true, instant: true });
    } else if (items.length) {
      open(items[0], { instant: true });
    }
  }

  /* ---- footer year --------------------------------------------------- */
  var y = document.querySelector('[data-year]');
  if (y) y.textContent = String(new Date().getFullYear());
})();
