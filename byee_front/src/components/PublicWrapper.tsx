import { useEffect } from "react"
import { useNavigate } from "react-router-dom"

function PublicWrapper({children, role}: {children: React.ReactNode; role: string}) {

    const navigate = useNavigate();

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
