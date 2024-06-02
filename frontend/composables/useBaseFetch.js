export const useBaseFetch = async (url, options) => {
  const config = useRuntimeConfig();

  const headers = { ...config.public.headers };
  return useFetch(url, {
    baseURL: config.public.baseURL,
    headers,
    ...options,
  });
};
