export async function onRequestGet({ request, env }) {
  const url = new URL(request.url);
  const isbn = url.searchParams.get('isbn');
  if (!isbn) return Response.json({ error: 'isbn is required' }, { status: 400 });
  if (!env.SERPAPI_KEY) return Response.json({ status: 'unconfigured', message: 'Live shopping lookup requires SERPAPI_KEY. No price has been displayed.' }, { status: 503 });
  return Response.json({ status: 'unconfigured', message: 'Provider adapter is ready for configuration. Validate edition, condition, currency, shipping, and retailer before returning a lowest price.' }, { status: 503 });
}
