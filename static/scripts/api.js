async function request(method, route, data = null) {
  let options = {
    method: method,
    credentials: 'include',
    headers: { 'Content-Type': 'application/json' },
  };

  if (data) {
    options.body = JSON.stringify(data);
  }

  try {
    const response = await fetch(`/registra_ai/${route}`, options);
    let body = await response.json()
    if (!response.ok) {
      console.error(body);
      return null;
    }
    return body;
  } catch (err) {
    console.error('Fetch error:', err);
  }
}

export async function getUserData() {
  return await request("GET", "/user_data");
}

export async function register(type, amount, description) {
  let body = {
    "amount": amount,
    "description": description
  }

  let res = await request("POST", `/${type}`, body);

  return res
}

export async function getHistory() {
  let res = await request("GET", "/history")
  return res;
}
