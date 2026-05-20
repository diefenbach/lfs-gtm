/**
 * Listens for lfs:consent-changed from lfs_cookie_consent and applies
 * Google Consent Mode v2, GTM dataLayer events, and Google cookie cleanup.
 * Register listener synchronously (do not defer inside DOMContentLoaded).
 */
(function () {
    'use strict';

    function deleteGACookies() {
        const allCookies = document.cookie.split(';').map(c => c.trim().split('=')[0]);
        const prefixes = ['_ga', '_gid', '_gat', '_gat_gtag', '_gat_UA', '__utma', '__utmb', '__utmc', '__utmz', '__utmt'];
        const domain = window.location.hostname.replace(/^www\./, '');
        const paths = ['/', window.location.pathname];
        const domains = [undefined, domain, '.' + domain];

        const gaCookies = allCookies.filter(name =>
            prefixes.some(prefix => name.startsWith(prefix))
        );

        gaCookies.forEach(name => {
            paths.forEach(path => {
                domains.forEach(d => {
                    let cookieString = `${name}=; Max-Age=0; path=${path};`;
                    if (d) cookieString += ` domain=${d};`;
                    document.cookie = cookieString;
                });
            });
        });
    }

    function deleteAdsCookies() {
        const allCookies = document.cookie.split(';').map(c => c.trim().split('=')[0]);
        const prefixes = ['_gcl_', '_gclid', '_gcl_aw', '_gcl_dc', '_gcl_gb', '_gcl_ha', '_gcl_hb', '_gcl_hc', '_gcl_hd', '_gcl_he', '_gcl_hf', '_gcl_hg', '_gcl_hh', '_gcl_hi', '_gcl_hj', '_gcl_hk', '_gcl_hl', '_gcl_hm', '_gcl_hn', '_gcl_ho', '_gcl_hp', '_gcl_hq', '_gcl_hr', '_gcl_hs', '_gcl_ht', '_gcl_hu', '_gcl_hv', '_gcl_hw', '_gcl_hx', '_gcl_hy', '_gcl_hz', 'IDE', 'test_cookie', 'NID', '1P_JAR', 'CONSENT', 'DV'];
        const domain = window.location.hostname.replace(/^www\./, '');
        const paths = ['/', window.location.pathname];
        const domains = [undefined, domain, '.' + domain];

        const adsCookies = allCookies.filter(name =>
            prefixes.some(prefix => name.startsWith(prefix))
        );

        adsCookies.forEach(name => {
            paths.forEach(path => {
                domains.forEach(d => {
                    let cookieString = `${name}=; Max-Age=0; path=${path};`;
                    if (d) cookieString += ` domain=${d};`;
                    document.cookie = cookieString;
                });
            });
        });
    }

    function applyConsentDetail(detail) {
        if (!detail || typeof detail.analytics !== 'boolean' || typeof detail.advertising !== 'boolean') {
            return;
        }

        if (typeof gtag === 'function') {
            gtag('consent', 'update', {
                analytics_storage: detail.analytics ? 'granted' : 'denied',
                ad_storage: detail.advertising ? 'granted' : 'denied',
            });
        }

        window.dataLayer = window.dataLayer || [];
        const analyticsEvent = detail.analytics ? 'analytics_consent_granted' : 'analytics_consent_denied';
        const advertisingEvent = detail.advertising ? 'advertising_consent_granted' : 'advertising_consent_denied';
        window.dataLayer.push({ event: analyticsEvent });
        window.dataLayer.push({ event: advertisingEvent });

        if (!detail.analytics) {
            deleteGACookies();
        }
        if (!detail.advertising) {
            deleteAdsCookies();
        }
    }

    document.addEventListener('lfs:consent-changed', function (e) {
        applyConsentDetail(e.detail);
    });
})();
