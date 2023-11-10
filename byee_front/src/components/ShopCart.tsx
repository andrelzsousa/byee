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

    console.log(data)

    console.log(cartId)

    return (
        <div className="col-span-2 bg-gray-500 rounded p-5">
            <h1 className="font-bold text-3xl">Carrinho (id: {5})</h1>
            {data?.map((product) => {
                return(
                    <div>
                        <h3 className="font-bold text-xl">{product.nome}</h3>
                        <p>R$ {product.preco}</p>
                    </div>
                )
            })}  
        </div>
    )
}

export default ShopCart
