// Netlify serverless function for tracking page views and clicks
// Uses Netlify Blobs for persistent storage (free tier)

const { getStore } = require("@netlify/blobs");

exports.handler = async (event) => {
  const headers = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type",
    "Content-Type": "application/json",
  };

  if (event.httpMethod === "OPTIONS") {
    return { statusCode: 200, headers, body: "" };
  }

  const store = getStore("tracking");

  // GET — return all tracking data
  if (event.httpMethod === "GET") {
    try {
      const data = await store.get("stats", { type: "json" });
      return { statusCode: 200, headers, body: JSON.stringify(data || { views: {}, clicks: {} }) };
    } catch (e) {
      return { statusCode: 200, headers, body: JSON.stringify({ views: {}, clicks: {} }) };
    }
  }

  // POST — record a view or click
  if (event.httpMethod === "POST") {
    try {
      const body = JSON.parse(event.body);
      const { type, page } = body; // type: "view" or "click", page: slug

      if (!type || !page) {
        return { statusCode: 400, headers, body: JSON.stringify({ error: "Missing type or page" }) };
      }

      // Get current stats
      let stats;
      try {
        stats = await store.get("stats", { type: "json" });
      } catch (e) {
        stats = null;
      }

      if (!stats) {
        stats = { views: {}, clicks: {} };
      }

      if (type === "view") {
        stats.views[page] = (stats.views[page] || 0) + 1;
      } else if (type === "click") {
        stats.clicks[page] = (stats.clicks[page] || 0) + 1;
      }

      await store.setJSON("stats", stats);

      return { statusCode: 200, headers, body: JSON.stringify({ ok: true }) };
    } catch (e) {
      return { statusCode: 500, headers, body: JSON.stringify({ error: e.message }) };
    }
  }

  return { statusCode: 405, headers, body: JSON.stringify({ error: "Method not allowed" }) };
};
