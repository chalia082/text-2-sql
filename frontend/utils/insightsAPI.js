export const fetchInsights = async (userInput, queryResult) => {
  const apiURI = process.env.NEXT_PUBLIC_INSIGHT_API_URI;

  try {
    const response = await fetch(apiURI, {
      method: 'POST',
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        user_input: userInput,
        query_result: queryResult
      }),
    });

    if (!response.ok) {
      throw new Error(`Network response was not ok: ${response.status}`);
    }

    const data = await response.json();
    return {
      type: 'success',
      response: data
    };
  } catch(err) {
    return {
      type: 'error',
      error: err.message || "Failed to fetch insights"
    };
  }
};