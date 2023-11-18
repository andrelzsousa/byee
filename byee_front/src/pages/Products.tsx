import { useEffect, useState } from "react";
import axios from 'axios';
import PageNav from "../components/PageNav";

interface Product {
    id?: number;
    nome: string;
    tipo: string;
    preco: number;
    SKU: string;
    is_del: boolean;
    fk_Usuario_vendedor_fk: number;
}

function Products() {
    const [products, setProducts] = useState<Product[]>([])

    useEffect(() => {
        async function fetchData() {
            try {
                const res = await axios.get("http://localhost:8000/products")
                setProducts(res.data)
            } catch (error) {
                console.log(error)
            }
        }
        fetchData()
    }, [setProducts])

    const handleDeleteClick = (productId :number) => {
        try {
            axios.put("http://localhost:8000/delete-product", productId)
            window.alert("Produto deletado com sucesso. ");
            window.location.href = '/products';
        } catch (error) {
            console.log(error)
        }
    };

    return (
        <>
            <PageNav />
            <div className="grid grid-cols-1 gap-2">
                <div className="flex items-center justify-center bg-gray-200 font-bold">
                    <div className="grid grid-cols-5 w-full text-center">
                        <div>Nome</div>
                        <div>Tipo</div>
                        <div>Preço</div>
                        <div>SKU</div>
                        <div>Ações</div>
                    </div>
                </div>
                {products.map((product) => (
                    // Verifica se o produto não está marcado como deletado (is_del === false)
                    !product.is_del && (
                        <div key={product.id} className="flex items-center justify-center bg-gray-100 border border-gray-300">
                            <div className="grid grid-cols-5 w-full text-center">
                                <div>{product.nome}</div>
                                <div>{product.tipo}</div>
                                <div>{product.preco}</div>
                                <div>{product.SKU}</div>
                                <div className="flex justify-around">
                                    <button className="w-16 bg-blue-500 text-white hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-700 focus:ring-offset-2">Editar</button>
                                    <button  onClick={() => product.id && handleDeleteClick(product.id)} className="w-16 bg-red-500 text-white hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-red-700 focus:ring-offset-2">Excluir</button>
                                </div>
                            </div>
                        </div>
                    )
                ))}
            </div>
        </>
    )
}

export default Products;
