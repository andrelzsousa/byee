import { useState } from "react";
import axios from 'axios';
import PageNav from "../components/PageNav";
import { useMutation, useQuery, useQueryClient } from "react-query";

interface Product {
    id?: number;
    nome: string;
    tipo: string;
    preco: number;
    SKU: string;
    fk_Usuario_vendedor_fk: number;
}

function Products() {
    const [isOpened, setIsOpened] = useState<boolean>(false)
    const [nome, setNome] = useState<string>("")
    const [tipo, setTipo] = useState<string>("")
    const [preco, setPreco] = useState<number | null>(null)
    const [SKU, setSKU] = useState<string>("")
    const [id, setId] = useState<number>(0)
    const [fk_Usuario_vendedor_fk, setFk_Usuario_vendedor_fk] = useState<number>(0)

    const queryClient = useQueryClient()
    const { data } = useQuery<Product[]>(['products'], async () => {
        const res = await axios.get("http://localhost:8000/products")
        return res.data
    })

    const postUpdateProduct = async (productData: Product) => {
        try {
          await axios.put('http://localhost:8000/update-product', productData);
        } catch (error) {
          console.error(error);
        }
      };
      
      const mutation = useMutation(postUpdateProduct, {onSuccess: async () => {
        await queryClient.invalidateQueries(["products"]);
        setIsOpened(false)
      }})

    const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault()
        const updatedProduct = {nome, tipo, preco: preco as number, SKU, fk_Usuario_vendedor_fk, id}

        await mutation.mutateAsync(updatedProduct)
    }
    
    return (
        <>
            <PageNav />
            <div className="grid grid-cols-1 gap-2 relative p-10">
            <form onSubmit={handleSubmit} className={`flex-col gap-4 p-5 absolute top-[45%] left-[50%] bg-gray-600 shadow rounded -translate-x-[50%] w-72 ${isOpened ? "flex" : "hidden"} transition-all`}>
                <h1 className="font-bold text-2xl text-white">Atualizar produto</h1>
                <input placeholder="Nome" className="border border-black p-1 rounded" type="text" value={nome} onChange={(e) => setNome(e.target.value)}/>
                <select className='border border-gray-100 rounded p-1' value={tipo} onChange={(e) => setTipo(e.target.value)}>
                    <option value="" disabled selected>Categoria</option>
                    <option value="Roupa">Roupa</option>
                    <option value="Calçado">Calçado</option>
                    <option value="Acessório">Acessório</option>
                </select>
                <input placeholder="Preço" className="border border-black p-1 rounded" type="text" value={preco as number} onChange={(e) => setPreco(Number(e.target.value))}/>
                <input placeholder="SKU" className="border border-black p-1 rounded" type="text" value={SKU} onChange={(e) => setSKU(e.target.value)}/>
                <button type="submit" className="bg-gray-400 rounded p-1">Salvar</button>
                <div className="absolute top-1 right-4 text-white font-bold text-2xl hover:text-black cursor-pointer" onClick={() => setIsOpened(false)}>x</div>
            </form>
                <div className="flex items-center justify-center bg-gray-200 font-bold p-1">
                    <div className="grid grid-cols-5 w-full text-center">
                        <div>Nome</div>
                        <div>Tipo</div>
                        <div>Preço</div>
                        <div>SKU</div>
                        <div>Ações</div>
                    </div>
                </div>
                {data?.map((product) => (
                    <div key={product.id} className="flex items-center justify-center bg-gray-100 border border-gray-300 p-1">
                        <div className="grid grid-cols-5 w-full text-center">
                            <div>{product.nome}</div>
                            <div>{product.tipo}</div>
                            <div>{product.preco}</div>
                            <div>{product.SKU}</div>
                            <div className="flex justify-around">
                                <button 
                                className="w-16 bg-blue-500 text-white hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-700 focus:ring-offset-2"
                                onClick={() => {
                                    setNome(product.nome)
                                    setTipo(product.tipo)
                                    setPreco(product.preco)
                                    setSKU(product.SKU)
                                    setId(product.id as number)
                                    setFk_Usuario_vendedor_fk(product.fk_Usuario_vendedor_fk)
                                    setIsOpened(true)
                                }}
                                >
                                    Editar
                                </button>
                                <button className="w-16 bg-red-500 text-white hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-red-700 focus:ring-offset-2"
                                >
                                    Excluir
                                </button>
                            </div>
                        </div>
                    </div>
                ))}
            </div>
        </>
    )
}

export default Products;
