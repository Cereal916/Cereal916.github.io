import { DOCUMENT } from '@angular/common';
import {
  Component,
  DestroyRef,
  ElementRef,
  computed,
  effect,
  inject,
  signal,
  viewChild,
} from '@angular/core';
import { toSignal } from '@angular/core/rxjs-interop';
import { Meta } from '@angular/platform-browser';
import { ActivatedRoute, RouterLink, RouterLinkActive } from '@angular/router';
import { WIKI_GUIDES, WIKI_ROOT } from './clipcabinet-guides';

export const WIKI_ASSETS = WIKI_ROOT + '/assets/';
export const LIBRARY_VIEWS = [
  {
    id: 'list',
    label: 'List',
    file: '01-library-list_english.png',
    caption: 'List view keeps thumbnails, tags, descriptions, and clip details together.',
  },
  {
    id: 'grid',
    label: 'Grid',
    file: '02-grid-view_english.png',
    caption: 'Grid view lets you recognize clips by their thumbnails.',
  },
  {
    id: 'table',
    label: 'Table',
    file: '03-table-view_english.png',
    caption: 'Table view helps compare clip details in sortable, resizable columns.',
  },
];
export const FAQ_GROUPS = [
  {
    id: 'recordings',
    title: 'Recordings and setup',
    items: [
      {
        question: 'Does ClipCabinet record gameplay?',
        answer:
          'Steam does the recording. Enable Steam Game Recording and capture your gameplay there; ClipCabinet helps you browse, organize, play, and export those recordings.',
      },
      {
        question: 'Are my recordings imported automatically?',
        answer:
          'Yes. ClipCabinet looks for your Steam recording folder and loads its videos when you open the app. If you record more while ClipCabinet is open, click Refresh. If your folder is not found, select it in Settings > General > Recording folder.',
      },
      {
        question: 'Why is my library empty?',
        answer:
          'Check that Steam Game Recording is enabled and that Steam has saved a recording. In ClipCabinet, select the folder containing your Steam recording sessions, then click Refresh. Clear the search, game, tag, favorites, and timeline filters if clips still seem missing.',
      },
      {
        question: 'Which computers are supported?',
        answer:
          'ClipCabinet supports Windows 10 22H2 and Windows 11 on 64-bit PCs. macOS and Linux are not supported.',
      },
    ],
  },
  {
    id: 'video',
    title: 'Playback and export',
    items: [
      {
        question: 'Why do some videos stutter or fail to play?',
        answer:
          'Playback depends on the recording codec, your hardware, and your graphics drivers. Keep drivers current. For another device or player, try exporting as H.264 instead of Original; copying the original codec does not change its compatibility.',
      },
      {
        question: 'Why are timeline markers missing?',
        answer:
          'Markers appear only when Steam saved timeline data for that recording. Event types and achievement information depend on the game and the available Steam data. A recording without markers can still be watched and exported.',
      },
      {
        question: 'Why is export slow?',
        answer:
          'Original copies the streams without re-encoding. H.264, HEVC, and AV1 re-encode the video. Enable hardware encoding to try a compatible GPU; ClipCabinet falls back to software when needed. CPU encoding can take longer.',
      },
      {
        question: 'Do I need to install VLC, FFmpeg, or .NET?',
        answer:
          'No. The Windows release includes the runtime and media tools. Keep the full installed or extracted application folder together. If an export tool is missing, verify the installation in Steam or extract the complete portable release again.',
      },
    ],
  },
  {
    id: 'data',
    title: 'Your data and settings',
    items: [
      {
        question: 'Does ClipCabinet change my original recordings?',
        answer:
          'No. Tags, descriptions, and favorites are stored separately. Exports create a separate MP4 file; your original Steam recordings stay unchanged.',
      },
      {
        question: 'Does Steam Cloud upload my videos?',
        answer:
          'No. Optional Steam Cloud sync covers tags, descriptions, and favorites only. Recordings and recording folders stay local; transfer the videos separately when moving to another PC.',
      },
      {
        question: 'Can I use the app without Steam running?',
        answer:
          'Local browsing, playback, annotation editing, backups, and export work without Steam. Cloud sync and friends-list activity need Steam and its corresponding services enabled.',
      },
      {
        question: 'What does a metadata backup include?',
        answer:
          'It contains favorites, descriptions, and tags, not video files. Back up the recordings separately. Importing a metadata backup replaces your current annotations; the app creates a safety backup before the replacement.',
      },
      {
        question: 'Can I change the language or make text larger?',
        answer:
          'Yes. Choose a language in Settings > General. In Settings > Accessibility, set interface size to 100%, 110%, or 125%, enable stronger contrast, reduce motion, or disable hover previews.',
      },
      {
        question: 'Where can I ask for help?',
        answer:
          'Use the Support link on this page to contact Slapcraft Games. Include your ClipCabinet version, Windows version, what you were doing, and the error message. You can inspect app logs with Open log; review logs before sharing any recording paths or personal details.',
      },
    ],
  },
];

@Component({
  selector: 'app-clipcabinet-wiki',
  standalone: true,
  imports: [RouterLink, RouterLinkActive],
  templateUrl: './clipcabinet-wiki.html',
  styleUrl: './clipcabinet-wiki.scss',
})
export class ClipCabinetWiki {
  private readonly route = inject(ActivatedRoute);
  private readonly document = inject(DOCUMENT);
  private readonly meta = inject(Meta);
  private readonly destroyRef = inject(DestroyRef);
  private readonly routeData = toSignal(this.route.data, {
    initialValue: this.route.snapshot.data,
  });
  private readonly imageDialog = viewChild.required<ElementRef<HTMLDialogElement>>('imageDialog');
  readonly root = WIKI_ROOT;
  readonly assets = WIKI_ASSETS;
  readonly pages = WIKI_GUIDES;
  readonly groups = [...new Set(WIKI_GUIDES.map((page) => page.group))];
  readonly faqGroups = FAQ_GROUPS;
  readonly views = LIBRARY_VIEWS;
  readonly page = computed(
    () => this.pages.find((page) => page.slug === this.routeData()['pageId']) ?? this.pages[0],
  );
  readonly menuOpen = signal(false);
  readonly selectedView = signal(LIBRARY_VIEWS[0]);
  readonly enlargedImage = signal<{ file: string; caption: string } | null>(null);

  constructor() {
    const wasWikiPage = this.document.body.classList.contains('clipcabinet-wiki-page');
    this.document.body.classList.add('clipcabinet-wiki-page');
    const oldDescription = this.meta.getTag('name="description"')?.content;
    const oldCanonical = this.document.querySelector<HTMLLinkElement>('link[rel="canonical"]');
    const oldCanonicalUrl = oldCanonical?.href;
    const canonical = oldCanonical ?? this.document.createElement('link');
    canonical.rel = 'canonical';
    if (!oldCanonical) this.document.head.appendChild(canonical);
    effect(() => {
      const page = this.page();
      this.meta.updateTag({ name: 'description', content: page.summary });
      canonical.href = 'https://www.slapcraftgames.com' + this.pageUrl(page.slug);
    });
    this.destroyRef.onDestroy(() => {
      if (!wasWikiPage) this.document.body.classList.remove('clipcabinet-wiki-page');
      if (
        oldDescription === undefined ||
        WIKI_GUIDES.some((guide) => guide.summary === oldDescription)
      )
        this.meta.removeTag('name="description"');
      else this.meta.updateTag({ name: 'description', content: oldDescription });
      if (oldCanonicalUrl && !new URL(oldCanonicalUrl).pathname.startsWith(WIKI_ROOT))
        canonical.href = oldCanonicalUrl;
      else canonical.remove();
    });
  }
  pageUrl(slug: string): string {
    return this.root + (slug ? '/' + slug : '');
  }
  skipToContent(event: Event): void {
    event.preventDefault();
    this.document.getElementById('wiki-content')?.focus();
  }
  openImage(file: string, caption: string): void {
    this.enlargedImage.set({ file, caption });
    this.imageDialog().nativeElement.showModal();
  }
  closeImage(): void {
    this.imageDialog().nativeElement.close();
  }
  closeBackdrop(event: MouseEvent): void {
    if (event.target === this.imageDialog().nativeElement) this.closeImage();
  }
}
