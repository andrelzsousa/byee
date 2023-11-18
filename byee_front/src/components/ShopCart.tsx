// import axios from "axios"
// import { useEffect, useState } from "react"

import { useQuery } from "react-query"
import { Product } from "../types/Product"
import axios from "axios"

// eslint-disable-next-line @typescript-eslint/no-explicit-any
function ShopCart({cartId}: {cartId: any}) {

    const {data} = useQuery<Product[]>(['cartItems'], async () => {
        const res = await axios.get(`http://localhost:8000/cart-items/${5}`)
        return res.data
    })

    const {data: total} = useQuery<number>(['cartTotal'], async () => {
        const res = await axios.get(`http://localhost:8000/cart-total/${5}`)
        return res.data
    })

    console.log(cartId)

    return (
        <div className="col-span-2 bg-gray-300 rounded p-5">
            <h1 className="font-bold text-3xl">Seu Carrinho</h1>
            {data?.map((product) => {
                return(
                    <div className=" flex justify-between p-1 shadow my-1 rounded">
                        <h3 className="text-xl">{product.nome}</h3>
                        <p>R$ {product.preco}</p>
                    </div>
                )
            })}
            <p className="my-2 font-bold"><span className="text-xl">Valor total:</span> R${total}</p>
            <div>
                <button className="bg-black text-white rounded px-2 py-1">Finalizar compra</button>
            </div>  
        </div>
    )
}

export default ShopCart
