export async function onRequestGet({ request }) {
  const type = new URL(request.url).searchParams.get('type') || 'unknown';
  const messages = { subscription: 'Institutional access or an individual plan is required', library: 'Free with a participating library card or academic access', database: 'Institutional access may be required', rights: 'Contact the rights holder for a quote' };
  return Response.json({ status: 'quote_or_access_required', sourceType: type, message: messages[type] || 'Price unavailable' });
}
