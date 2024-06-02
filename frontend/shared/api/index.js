import { useBaseFetch } from '~/composables/useBaseFetch.js';

export async function getAnswer(question) {
  const { data } = await useBaseFetch('/assist_legacy', {
    method: 'POST',
    body: {
      query: {
        question,
      },
    },
  });

  return data.value.text;
}
