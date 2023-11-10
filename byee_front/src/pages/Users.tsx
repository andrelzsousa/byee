import { useEffect, useState } from "react"
import axios from 'axios';

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
        <div>
            {users.map((user) => {
                return(
                    <>
                    <div key={user.id} className="flex items-center gap-1">
                        <p>{user.id}</p>
                        <p>{user.nome}</p>
                        <p>{user.telefone}</p>
                    </div>
                    </>
                )
            })}
        </div>
    )
}

export default Users
