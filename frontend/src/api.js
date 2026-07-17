const API_URL = 'http://localhost:8000';

export async function sendMessage(message, sessionId = "default_session") {
  try {
    const response = await fetch(`${API_URL}/chat`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ message, session_id: sessionId }),
    });
    
    if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    const data = await response.json();
    return data;
  } catch (error) {
    console.error("Error communicating with backend:", error);
    return { response: "Connection error. Ensure the FastAPI backend is running.", persona: "System" };
  }
}
