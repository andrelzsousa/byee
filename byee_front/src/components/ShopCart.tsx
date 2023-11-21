// import axios from "axios"
import { useEffect, useState } from "react"

import { useQuery, useQueryClient } from "react-query"
import { Product } from "../types/Product"
import axios from "axios"
import { useNavigate } from "react-router-dom";

function getCurrentDateFormatted(): string {
    const today = new Date();
    const year = today.getFullYear();
    const month = (today.getMonth() + 1).toString().padStart(2, '0'); // getMonth() retorna 0-11
    const day = today.getDate().toString().padStart(2, '0');

    return `${year}-${month}-${day}`;
}
// eslint-disable-next-line @typescript-eslint/no-explicit-any
function ShopCart({cartId}: {cartId: any}) {
    const [total, setTotal] = useState(0);

    const navigate = useNavigate();
    const queryClient = useQueryClient();
    
    const {data} = useQuery<Product[]>(['cartItems'], async () => {
        const res = await axios.get(`http://localhost:8000/cart-items/${5}`)
        return res.data
    })

    // const {data: total} = useQuery<number>(['cartTotal'], async () => {
    //     const res = await axios.get(`http://localhost:8000/cart-total/${5}`)
    //     return res.data
    // })

    useEffect(() => {
        const fetchCartTotal = async () => {
            try {
                if (cartId?.cart_id !== undefined) {
                    const res = await axios.get(`http://localhost:8000/cart-total/${5}`);
                    setTotal(res.data);
                }
            } catch (error) {
                console.log('Erro ao buscar o total do carrinho:', error);
            }
        };

        fetchCartTotal();
    }, [cartId, data]);

    

    const createSale = async () => {
        const saleData = {
            valor: total,
            cnpj_emissor: "24.176.134/0001-26",
            codigo: "123456789",
            data_geracao: getCurrentDateFormatted(),
            status: "Em separação",
            transportadora: "Correios",
            data_envio: getCurrentDateFormatted(),
            data_venda: getCurrentDateFormatted(),
            valor_frete: 10,
            fk_id_comprador: 5,
        };

        try {
            const response = await axios.post('http://localhost:8000/payment-invoice', saleData);
            console.log('Venda criada com sucesso:', response.data);
            alert("Compra realizada com sucesso");
            data?.forEach(async (product) => {
                await axios.delete(`http://localhost:8000/remove-product-from-cart/${5}/${product.id}`);
            });
            queryClient.invalidateQueries('cartItems');
            navigate('/invoices');
        } catch (error) {
            console.error('Erro ao criar venda:', error);
        }
    };

    const deleteItem = async (cartId: number, productId: number) => {
        try {
            await axios.delete(`http://localhost:8000/remove-product-from-cart/${cartId}/${productId}`);
            queryClient.invalidateQueries('cartItems');
        } catch (error) {
            console.error('Erro ao remover produto:', error);
        }
    }

    return (
        <div className="col-span-2 bg-gray-300 rounded p-5">
            <h1 className="font-bold text-3xl">Seu Carrinho</h1>
            {data?.map((product) => 
                !product.is_del && (
                    <div className=" flex justify-between p-1 shadow my-1 rounded" key={product.id}>
                        <h3 className="text-xl">{product.nome}</h3>
                        <div className="flex items-center gap-4">
                            <p>R$ {product.preco}</p>
                            <div className="cursor-pointer text-red-500 hover:text-red-700 font-bold text-xl" onClick={() => deleteItem(5, product.id as number)}>x</div>
                        </div>
                    </div>
                )
            )}
            <p className="my-2 font-bold"><span className="text-xl">Valor total:</span> R${total}</p>
            <div>
                <button className="bg-black text-white rounded px-2 py-1" onClick={createSale}>Finalizar compra</button>
            </div>  
        </div>
    )
}

export default ShopCart
