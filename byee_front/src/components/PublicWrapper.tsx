import { useEffect } from "react"
import { useNavigate } from "react-router-dom"

function PublicWrapper({children}: {children: React.ReactNode}) {

    const navigate = useNavigate();
    const role = localStorage.getItem("role")

    useEffect(() => {
		if (role === "admin") {
			navigate("/products")
		} else if (role === ""){
            navigate("/")
        }
	}, [role, navigate])

    return (
        <div>
            {children}
        </div>
    )
}

export default PublicWrapper
