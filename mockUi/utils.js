
async function customFetch(options) {
    const response = await fetch(options.url, {
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `token ${options.token}`
        }
    })
    return await response.json();
}