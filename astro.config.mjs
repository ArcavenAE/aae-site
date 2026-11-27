// @ts-check
import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';

// The site address is not chosen yet, so no `site` or `base` is set here.
export default defineConfig({
  integrations: [
    starlight({
      title: 'DARKATELIER',
      description: 'Guides and references for the ArcavenAE projects.',
      logo: { src: './src/assets/aae-mark.svg', alt: '' },
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
        { label: 'marvel command reference', items: [{ autogenerate: { directory: 'reference' } }] },
      ],
    }),
  ],
});
