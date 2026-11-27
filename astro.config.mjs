// @ts-check
import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';

// The site address is not chosen yet, so no `site` or `base` is set here.
export default defineConfig({
  integrations: [
    starlight({
      title: 'ArcavenAE',
      description: 'Guides and references for the ArcavenAE projects.',
      sidebar: [
        { label: 'Start here', items: [{ slug: 'e1-tour' }] },
        { label: 'marvel command reference', items: [{ autogenerate: { directory: 'reference' } }] },
      ],
    }),
  ],
});
