import { Component } from '@angular/core';

let instances = 0;

/**
 * Slapcraft Games on YouTube, Instagram and Steam. The marks are simple inline
 * SVGs drawn in currentColor, so they follow the surrounding link colour and
 * hover state and need no icon library.
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
            <mask [attr.id]="steamMask">
              <rect width="24" height="24" fill="#fff" />
              <path
                d="M0.8 12.4 8.4 15.6 15.6 8.4"
                fill="none"
                stroke="#000"
                stroke-width="2.3"
                stroke-linecap="round"
                stroke-linejoin="round"
              />
              <circle cx="15.6" cy="8.4" r="4.3" fill="#000" />
              <circle cx="15.6" cy="8.4" r="2.6" fill="#fff" />
              <circle cx="8.4" cy="15.6" r="2.8" fill="#000" />
              <circle cx="8.4" cy="15.6" r="1.4" fill="#fff" />
            </mask>
            <circle cx="12" cy="12" r="11" [attr.mask]="'url(#' + steamMask + ')'" />
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
export class SocialLinks {
  // Each instance needs its own mask id so two copies never share one.
  protected readonly steamMask = `steam-mark-${++instances}`;
}
