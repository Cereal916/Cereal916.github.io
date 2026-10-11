export const WIKI_ROOT = '/clipcabinet/wiki';
export const WIKI_GUIDES = [
  {
    slug: '',
    label: 'Get started',
    group: 'Start here',
    title: 'Get started with ClipCabinet',
    summary:
      'Automatically import videos recorded with Steam’s built-in recorder, then organize, watch, and export them.',
    sections: [
      { id: 'first-recording', label: 'Your first recording' },
      { id: 'library', label: 'Meet your library' },
      { id: 'next', label: 'What to try next' },
    ],
  },
  {
    slug: 'organize',
    label: 'Tags & descriptions',
    group: 'Use your library',
    title: 'Keep the context with your clips',
    summary:
      'Add your own tags, descriptions, and favorites so good moments are easy to find again.',
    sections: [
      { id: 'tags', label: 'Add tags' },
      { id: 'descriptions', label: 'Write a description' },
      { id: 'favorites', label: 'Use favorites' },
    ],
  },
  {
    slug: 'browse',
    label: 'Search & views',
    group: 'Use your library',
    title: 'Find the moment you want',
    summary: 'Search your collection, combine filters, and choose the view that suits the task.',
    sections: [
      { id: 'search', label: 'Search and filter' },
      { id: 'views', label: 'List, grid, and table' },
      { id: 'sorting', label: 'Sort your library' },
    ],
  },
  {
    slug: 'playback',
    label: 'Playback & timeline',
    group: 'Use your library',
    title: 'Watch, seek, and jump to events',
    summary:
      'Play saved clips and background recordings in the built-in player, with timeline previews and Steam events.',
    sections: [
      { id: 'player', label: 'Open the player' },
      { id: 'markers', label: 'Timeline markers' },
      { id: 'shortcuts', label: 'Timeline shortcuts' },
    ],
  },
  {
    slug: 'export',
    label: 'Export videos',
    group: 'Use your library',
    title: 'Export a clip as MP4',
    summary:
      'Keep the original video quality or choose a codec for the device you want to watch on.',
    sections: [
      { id: 'export-steps', label: 'Export in three steps' },
      { id: 'codecs', label: 'Choose a codec' },
      { id: 'encoding', label: 'GPU or CPU encoding' },
    ],
  },
  {
    slug: 'settings',
    label: 'Settings & backups',
    group: 'Preferences',
    title: 'Make ClipCabinet work for you',
    summary:
      'Set your recording folder and language, adjust accessibility, and protect your annotations.',
    sections: [
      { id: 'general', label: 'General settings' },
      { id: 'accessibility', label: 'Accessibility' },
      { id: 'backup', label: 'Back up and restore' },
      { id: 'steam', label: 'Steam and privacy' },
    ],
  },
  {
    slug: 'faq',
    label: 'Frequently asked questions',
    group: 'Help',
    title: 'Frequently asked questions',
    summary: 'Quick answers about recordings, playback, export, and your data.',
    sections: [
      { id: 'recordings', label: 'Recordings and setup' },
      { id: 'video', label: 'Playback and export' },
      { id: 'data', label: 'Your data and settings' },
    ],
  },
];
