import { useEffect } from "react"
import { useNavigate } from "react-router-dom"

function AdminWrapper({children}: {children: React.ReactNode}) {

    const navigate = useNavigate();
    const role = localStorage.getItem("role")

    useEffect(() => {
		if (role === "comprador") {
			navigate("/home")
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

export default AdminWrapper