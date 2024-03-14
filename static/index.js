const logout = async (e) => {

    fetch('/logout', {
         method: "POST",
         headers: {"accept": "application/json"}
      }).then((response) => {
        window.location.replace('/login')
      })

}