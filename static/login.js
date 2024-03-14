const login = async (e) => {

    const unameInput = document.getElementById("username").value

    fetch(`/login?username=${unameInput}`, {
         method: "POST",
         headers: {"accept": "application/json"}
      }).then((response) => {
        if (!response.ok) {
            document.getElementById("err msg").hidden = false
        }
        else window.location.replace('/')
      })

}