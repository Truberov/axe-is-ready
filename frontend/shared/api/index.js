import { useBaseFetch } from '~/composables/useBaseFetch.js';

export async function getAnswer(question) {
  const { data } = await useBaseFetch('/assist', {
    method: 'POST',
    body: {
      query: question,
    },
  });

  return data.value.text;
}
