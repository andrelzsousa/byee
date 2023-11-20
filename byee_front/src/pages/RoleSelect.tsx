import { useNavigate } from "react-router-dom";

// eslint-disable-next-line @typescript-eslint/no-explicit-any
function RoleSelect() {

    const navigate = useNavigate();

	// useEffect(() => {
	// 	if (role === "comprador") {
	// 		navigate("/home")
	// 	} else if (role === "admin") {
	// 		navigate("/produtos")
	// 	}
	// }, [role, navigate])
    
    return (
        <div>
            <h1 className="font-bold text-4xl pt-5 px-10">Escolha como desejar acessar a aplicação: </h1>
            <div className="px-10 py-5 grid grid-cols-2 h-96 gap-10">
                <div
                    className="bg-gray-300 rounded flex items-center justify-center text-5xl font-bold hover:scale-105 cursor-pointer transition-all"
                    onClick={() => {
                        // setRole("comprador")
                        navigate("/home")
                        localStorage.setItem("role", "comprador")
                    }}
                >
                    Comprador
                </div>
                <div
                    className="bg-gray-700 text-white rounded flex items-center justify-center text-5xl font-bold hover:scale-105 cursor-pointer transition-all"
                    onClick={() => {
                        // setRole("admin")
                        navigate("/products")
                        localStorage.setItem("role", "admin")
                    }}
                >
                    Admin
                </div>
            </div>
        </div>
    )
}

export default RoleSelect
