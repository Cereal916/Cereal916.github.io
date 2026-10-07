import { Component } from '@angular/core';

/**
 * Slapcraft Games on YouTube, Instagram and Steam. The marks are simple inline
 * SVGs drawn in currentColor, so they follow the surrounding link colour and
 * hover state and need no icon library. Each mark is plain paths with no
 * url(#id) references: the site's <base href> would resolve those to another
 * page and the browser would drop the mask or gradient.
 */
@Component({
  selector: 'app-social-links',
  template: `
    <ul class="social-links">
      <li>
        <a
          href="https://www.youtube.com/@slapcraftgames"
          target="_blank"
          rel="noopener noreferrer"
          aria-label="Slapcraft Games on YouTube"
          title="YouTube"
        >
          <svg viewBox="0 0 24 24" aria-hidden="true" focusable="false">
            <path
              fill-rule="evenodd"
              d="M5.5 5h13a4 4 0 0 1 4 4v6a4 4 0 0 1-4 4h-13a4 4 0 0 1-4-4V9a4 4 0 0 1 4-4zM10 8.8v6.4l5.6-3.2z"
            />
          </svg>
        </a>
      </li>
      <li>
        <a
          href="https://www.instagram.com/slapcraftgames/"
          target="_blank"
          rel="noopener noreferrer"
          aria-label="Slapcraft Games on Instagram"
          title="Instagram"
        >
          <svg viewBox="0 0 24 24" aria-hidden="true" focusable="false">
            <rect
              x="3"
              y="3"
              width="18"
              height="18"
              rx="5"
              fill="none"
              stroke="currentColor"
              stroke-width="2.2"
            />
            <circle cx="12" cy="12" r="4.1" fill="none" stroke="currentColor" stroke-width="2.2" />
            <circle cx="17.3" cy="6.7" r="1.35" />
          </svg>
        </a>
      </li>
      <li>
        <a
          href="https://store.steampowered.com/developer/slapcraft?snr=1_5_9__2000"
          target="_blank"
          rel="noopener noreferrer"
          aria-label="Slapcraft Games on Steam"
          title="Steam"
        >
          <svg viewBox="0 0 24 24" aria-hidden="true" focusable="false">
            <path
              d="M11.979 0C5.678 0 .511 4.86.022 11.037l6.432 2.658c.545-.371 1.203-.59 1.912-.59.063 0 .125.004.188.006l2.861-4.142V8.91c0-2.495 2.028-4.524 4.524-4.524 2.494 0 4.524 2.031 4.524 4.527s-2.03 4.525-4.524 4.525h-.105l-4.076 2.911c0 .052.004.105.004.159 0 1.875-1.515 3.396-3.39 3.396-1.635 0-3.016-1.173-3.331-2.727L.436 15.27C1.862 20.307 6.486 24 11.979 24c6.627 0 11.999-5.373 11.999-12S18.605 0 11.979 0zM7.54 18.21l-1.473-.61c.262.543.714.999 1.314 1.25 1.297.539 2.793-.076 3.332-1.375.263-.63.264-1.319.005-1.949s-.75-1.121-1.377-1.383c-.624-.26-1.29-.249-1.878-.03l1.523.63c.956.4 1.409 1.5 1.009 2.455-.397.957-1.497 1.41-2.454 1.012H7.54zm11.415-9.303c0-1.662-1.353-3.015-3.015-3.015-1.665 0-3.015 1.353-3.015 3.015 0 1.665 1.35 3.015 3.015 3.015 1.663 0 3.015-1.35 3.015-3.015zm-5.273-.005c0-1.252 1.013-2.266 2.265-2.266 1.249 0 2.266 1.014 2.266 2.266 0 1.251-1.017 2.265-2.266 2.265-1.253 0-2.265-1.014-2.265-2.265z"
            />
          </svg>
        </a>
      </li>
    </ul>
  `,
  styles: `
    .social-links {
      display: flex;
      align-items: center;
      gap: 0.9rem;
      margin: 0;
      padding: 0;
      list-style: none;
    }

    a {
      display: flex;
      padding: 0.2rem;
      color: #fffdf2;
      transition: color 0.15s ease;
    }

    a:hover,
    a:focus-visible {
      color: #ff0066;
    }

    a:focus-visible {
      outline: 3px solid #ff0066;
      outline-offset: 2px;
    }

    svg {
      width: 1.6rem;
      height: 1.6rem;
      fill: currentColor;
    }
  `,
})
export class SocialLinks {}
