import { useEffect, useState } from "react"
import axios from 'axios';
import PageNav from "../components/PageNav";

interface User {
    id: number
    nome: string;
    telefone: string;
    endereco_FK: number | null;
    rua: string | null;
    numero: string | null;
    bairro: string | null;
    cidade: string | null;
    fk_usuario_presente: number | null;
}


function Users() {
    const [users, setUsers] = useState<User[]>([]);
    useEffect(() => {
        async function fetchData() {
            try {
              const response = await axios.get("http://localhost:8000/users");
              setUsers(response.data);
            } catch (error) {
              console.error(error);
            }
          }          
        
        fetchData()
    }, [setUsers])
    
    const handleDeleteClick = async (endereco_FK: number) => {
        const decision = window.confirm("Realmente deseja apagar esse item?");
        if (decision) {
            try {
                await axios.delete(`http://localhost:8000/delete-addr/${endereco_FK}`);
                window.alert("Endereço deletado com sucesso.");
                window.location.href = '/users';
            } catch (error) {
                console.log(error);
            }
        }
    };
    
    return (
        <>
            <PageNav />
            <div className="grid grid-cols-1 gap-2 p-10">
                <div className="flex items-center justify-center bg-gray-200 font-bold p-1">
                    <div className="grid grid-cols-8 w-full text-center">
                        <div>Id</div>
                        <div>Nome</div>
                        <div>Telefone</div>
                        <div>Rua</div>
                        <div>Numero</div>
                        <div>Bairro</div>
                        <div>Cidade</div>
                        <div> </div>
                    </div>
                </div>
                {users.map((user) => {
                    return (
                        <div key={user.id} className="flex items-center justify-center bg-gray-100 border border-gray-300 p-1">
                            <div className="grid grid-cols-8 w-full text-center">
                                <div>{user.id}</div>
                                <div>{user.nome}</div>
                                <div>{user.telefone}</div>
                                <div>{user.rua ? user.rua : 'Não informado'}</div>
                                <div>{user.numero ? user.numero : 'Não informado'}</div>
                                <div>{user.bairro ? user.bairro : 'Não informado'}</div>
                                <div>{user.cidade ? user.cidade : 'Não informado'}</div>
                                <div className="flex justify-around">
                                    <button onClick={() => user.endereco_FK && handleDeleteClick(user.endereco_FK)} className="w-20 bg-red-500 text-white hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-red-700 focus:ring-offset-2">Excluir Endereço</button>
                                </div>
                            </div>
                        </div>
                    );
                })}
            </div>
        </>
    );
}

export default Users;