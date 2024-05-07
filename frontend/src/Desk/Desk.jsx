import { useState, useContext, useEffect } from "react";
import { TokenContext } from "../Navigator/Navigator";

function Desk() {
 
    const {token} = useContext(TokenContext)

    const [img, setImg] = useState(null)

    let url = ""

    if (img == null) {
        fetch(global.config.api_img, {
            method: "GET",
            headers: {
                "Authorization": token
            }
        }).then(async (response) => {
            if (response.ok) {
                setImg(await response.blob())
            }
            else setImg("Error1")
        }).catch(e => {
            setImg("Error2")
        })
    } else {
        url = URL.createObjectURL(img)
    }


    const [seat, setSeat] = useState(null)

    if (seat == null) {
        fetch(global.config.api_seat + "?d="
            + String(global.config.today.getFullYear()).padStart(4, '0')
            + '-' + String(global.config.today.getMonth() + 1).padStart(2, '0')
            + '-' + String(global.config.today.getDate()).padStart(2, '0')
        , {
            method: "GET",
            headers: {
                "Authorization": token
            }
        }).then(async (response) => {
            if (response.ok) {
                setSeat(await response.json())
            }
            else setSeat("Error1")
        }).catch(e => {
            setSeat("Error2")
        })
    }

    useEffect(() => {
        if (url !== "") {
            var c = document.getElementById("canvas")
            var ctx = c.getContext("2d")
            var image = new Image;
            image.onload = function(){
                c.width = image.width; c.height = image.height
                ctx.drawImage(image, 0, 0)

                //draw desk spot
                if (seat !== null && seat !== "Error") {
                    ctx.fillStyle = '#ff0000'
                    ctx.beginPath();
                    ctx.arc(seat.x, seat.y, 10, 0, 2 * Math.PI, true)
                    ctx.fill()
                    ctx.stroke()
                }
            }
            image.src = url

            
        }
    })
        

    return (
        <div>
            <h1>Desk</h1>
            {url !== "" && <canvas id="canvas"></canvas>}
        </div>
    )

}

export default Desk