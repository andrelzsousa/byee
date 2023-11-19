// import { useEffect, useState } from "react"
import axios from 'axios';
import { Product } from "../types/Product";
import { useMutation, useQueryClient } from 'react-query';
import PageNav from '../components/PageNav';
// import { v4 as uuidv4 } from 'uuid';

function CreateProduct() {

  const queryClient = useQueryClient()
  
  const postUser = async (productData: Product) => {
    try {
      await axios.post('http://localhost:8000/create-product', productData);
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
    try {
      await mutation.mutateAsync(newProduct);
      window.setTimeout(() => {
        window.alert("Produto Criado com sucesso");
        window.location.href = '/';
      }, 0);
    } catch (e) {
      window.alert("Erro ao criar produto. " + e);
    }
  };


    return (
      <>
        <PageNav />
        <div className='flex items-center justify-center mt-28'>
          <form className='border border-black rounded-xl flex flex-col py-4 px-8 gap-2' onSubmit={handleSubmit}>
            <h1 className='text-2xl font-bold mb-2'>Cadastrar produto</h1>
            <input type="text" placeholder="Nome do produto" className='border border-gray-100 rounded p-1'/>
            <input type="text" placeholder="Preço" className='border border-gray-100 rounded p-1' />
            <select className='border border-gray-100 rounded p-1'>
                <option value="" disabled selected>Categoria</option>
                    <option value="Roupa">Roupa</option>
                    <option value="Calçado">Calçado</option>
                    <option value="Acessório">Acessório</option>
            </select>
            <input type="text" placeholder="SKU" className='border border-gray-100 rounded p-1' />
            <button className='py-2 px-4 bg-gray-100 rounded-full border border-black'>Cadastrar</button>
          </form>
        </div>
    </>
    )
}

export default CreateProduct
