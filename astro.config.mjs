// @ts-check
import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';

// The public address. It sets canonical links and the sitemap; wrangler.jsonc
// attaches the same hostname.
export default defineConfig({
  site: 'https://docs.darkatelier.org',
  integrations: [
    starlight({
      title: 'DARKATELIER',
      description: 'Guides and references for the ArcavenAE projects.',
      favicon: '/favicon.svg',
      customCss: ['./src/styles/aae.css'],
      // Dark only: set the stored choice and the attribute before first paint.
      head: [
        {
          tag: 'script',
          content:
            "try{localStorage.setItem('starlight-theme','dark')}catch(e){}document.documentElement.dataset.theme='dark';",
        },
      ],
      components: {
        ThemeSelect: './src/components/NoThemeSelect.astro',
        Footer: './src/components/Footer.astro',
      },
      sidebar: [
        { label: 'Start here', items: [{ slug: 'e1-tour' }, { slug: 'about' }] },
        { label: 'Stories', items: [{ slug: 'budgets' }, { slug: 'fleet-view' }] },
        { label: 'marvel command reference', items: [{ autogenerate: { directory: 'reference' } }] },
      ],
    }),
  ],
});
