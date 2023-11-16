import { useEffect, useState } from "react"
import axios from 'axios';
import  imgDefault  from "../assets/default.jpg";
import { Product } from "../types/Product";
import ShopCart from "../components/ShopCart";
import { useMutation, useQuery, useQueryClient } from "react-query";
import PageNav from "../components/PageNav";


function Home() {
    const [cartId, setCartId] = useState<number>(0)

    const queryClient = useQueryClient()
    const {data} = useQuery<Product[]>(['products'], async () => {
        const res = await axios.get("http://localhost:8000/products")
        return res.data
    })

    useEffect(() => {
        async function fetchData() {
            try{
                const res = await axios.get(`http://localhost:8000/user-cart-id/${5}`)
                setCartId(res.data)
            } catch(error){
                console.log(error)
            }
        }
        fetchData()
    }, [])

    const mutation = useMutation(async ({cart_id, product_id}:{cart_id: number, product_id: number}) => {
        return await axios.post(`http://localhost:8000/add-product-to-cart`, {cart_id, product_id})
    }, {onSuccess: async () => {
        await queryClient.invalidateQueries(["cartItems"]);
    }})

    console.log("cartId: " + cartId)

    return (
        <>
        <PageNav />
        <div className="grid grid-cols-6 p-10">
            <div className="col-span-4">
                <h1 className="text-2xl font-bold mb-4">Nossos Produtos</h1>
                <div className="flex gap-x-4 gap-y-6 flex-wrap">
                    {data?.map((product) => {
                        return(
                            <div className="shadow rounded-xl flex flex-col gap-1 items-center p-2 w-44 h-48 relative" key={product.id}>
                                <img src={imgDefault} className="w-20 h-20 rounded-full"/>
                                <h3 className="font-bold">{product.nome}</h3>
                                <p>R$ {product.preco}</p>
                                <p className="bg-black text-white rounded-full px-2 py-1 text-xs">{product.tipo}</p>
                                <div
                                    className="rounded-full h-6 w-6 flex items-center justify-center bg-black text-white bottom-2 right-2 absolute cursor-pointer"
                                    onClick={async() => await mutation.mutateAsync({cart_id: 5, product_id: product.id as number})}
                                >+</div>
                            </div>
                        )
                    })}
                </div>
            </div>
            <ShopCart cartId={cartId} />
        </div>
        </>
    )
}

export default Home
