async function fetchCatch(url, options) {
  try {
    const res = await fetch(url, options);
    return res;
  }
  catch (error) {
    return new Response(new Blob(), {status: 503, statusText: error.message});
  }
}

export default fetchCatch;
