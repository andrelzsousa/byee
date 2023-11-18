import { useEffect, useState } from "react"
import axios from 'axios';
import PageNav from "../components/PageNav";

interface User {
    id: number
    nome: string;
    telefone: string;
    endereco_Fk: number;
    fk_usuario_presente: number | null;
}

function Users() {
    const [users, setUsers] = useState<User[]>([])

    useEffect(() => {
        async function fetchData() {
            try{
                const res = await axios.get("http://localhost:8000/users")
                setUsers(res.data)
            } catch(error){
                console.log(error)
            }
        }
        fetchData()
    }, [setUsers])
    
    return (
        <>
            <PageNav />
            <div className="grid grid-cols-1 gap-2 p-10">
                <div className="flex items-center justify-center bg-gray-200 font-bold p-1">
                    <div className="grid grid-cols-5 w-full text-center">
                        <div>Id</div>
                        <div>Nome</div>
                        <div>Telefone</div>
                        <div>Ações</div>
                    </div>
                </div>
                {users.map((user) => (
                    <div key={user.id} className="flex items-center justify-center bg-gray-100 border border-gray-300 p-1">
                        <div className="grid grid-cols-5 w-full text-center">
                            <div>{user.id}</div>
                            <div>{user.nome}</div>
                            <div>{user.telefone}</div>
                            <div className="flex justify-around">
                                <button className="w-16 bg-blue-500 text-white hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-700 focus:ring-offset-2">Editar</button>
                                <button className="w-16 bg-red-500 text-white hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-red-700 focus:ring-offset-2">Excluir</button>
                            </div>
                        </div>
                    </div>
                ))}
            </div>
        </>
    )
}

export default Users
