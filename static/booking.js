const req_book = async (e) => {
    const date = document.getElementById("date").value
    
    fetch(`/book?booking_date=${date}`, {
        method: "POST",
        headers: {"accept": "application/json"}
    }).then(async (response) => {
        if (!response.ok)
            document.getElementById("status").innerText = (await response.json()).detail
        else
            document.getElementById("status").innerText = await response.json()
    })
}