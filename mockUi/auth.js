async function getToken() {

    let url = authUrl;
    let data = {
        'username': 'leks_buy',
        'password': 1
    }
    const response = await fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    return await response.json()
}