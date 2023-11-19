import { useEffect } from "react"
import { useNavigate } from "react-router-dom"

function AdminWrapper({children, role}: {children: React.ReactNode; role: string}) {

    const navigate = useNavigate();

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