// import { useEffect, useState } from "react"
import axios from 'axios';
import { Product } from "../types/Product";
import { useMutation, useQueryClient } from 'react-query';
// import { v4 as uuidv4 } from 'uuid';

function CreateProduct() {

  const queryClient = useQueryClient()
  
  const postUser = async (productData: Product) => {
    try {
      const response = await axios.post('http://localhost:8000/create-product', productData);
      console.log(response.data);
    } catch (error) {
      console.error(error);
    }
  };
  
  const mutation = useMutation(postUser, {onSuccess: async () => {
    await queryClient.invalidateQueries(["products"]);
  }})

  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  const handleSubmit = async (event: any) => {
    event.preventDefault();
    const nome = event.target[0].value
    const preco = event.target[1].value
    const tipo = event.target[2].value
    const SKU = event.target[3].value
    const newProduct: Product = { nome, preco, tipo, SKU, fk_Usuario_vendedor_fk: 1 };
    await mutation.mutateAsync(newProduct);
  };


    return (
    <div className='flex items-center justify-center h-screen'>
      <form className='border border-black rounded-xl flex flex-col py-4 px-8 gap-2' onSubmit={handleSubmit}>
        <h1 className='text-2xl font-bold mb-2'>Cadastrar produto</h1>
        <input type="text" placeholder="Nome do produto" className='border border-amber-200 rounded p-1'/>
        <input type="text" placeholder="Preço" className='border border-amber-200 rounded p-1' />
        <select className='border border-amber-200 rounded p-1'>
          <option value="">Categoria</option>
          <option value="camisa">Camisa</option>
          <option value="calca">Calça</option>
          <option value="tenis">Tênis</option>
        
        </select>
        <input type="text" placeholder="SKU" className='border border-amber-200 rounded p-1' />
        <button className='py-2 px-4 bg-amber-300 rounded-full border border-black'>Salvar</button>
      </form>
    </div>
    )
}

export default CreateProduct
