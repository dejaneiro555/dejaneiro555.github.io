import { defineCollection } from 'astro:content';
import { glob } from 'astro/loaders';
import { z } from 'astro/zod';

// Each Markdown file in src/content/projects becomes one case-study page.
const projects = defineCollection({
  loader: glob({ base: './src/content/projects', pattern: '**/*.md' }),
  schema: z.object({
    title: z.string(),
    summary: z.string(),
    status: z.string(),
    stack: z.array(z.string()),
    repo: z.url().optional(),
    order: z.number(),
  }),
});

export const collections = { projects };
