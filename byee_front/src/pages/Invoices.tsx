
import axios from "axios"
import { useEffect, useState } from "react"

function formatDate(dateStr: string): string {
    const parts = dateStr.split('-');
    return parts[2] + '/' + parts[1] + '/' + parts[0];
}

interface metrics {
    id: number;
    valor: number;
}

function Invoices() {
    const [invoices, setInvoices] = useState([]);
    const [average, setAverage] = useState();
    const [cheapest, setCheapest] = useState<metrics>();
    const [expensive, setExpensive] = useState<metrics>();

    useEffect(() => {
        const fetchInvoices = async () => {
            try {
                    const res = await axios.get(`http://localhost:8000/get-user-invoices/${5}`);
                    setInvoices(res.data);
            } catch (error) {
                console.log('Erro ao buscar o total do carrinho:', error);
            }
        };

        fetchInvoices();
    }, []);

    useEffect(() => {
        const fetchInvoices = async () => {
            try {
                    const res = await axios.get(`http://localhost:8000/get-user-invoices-average/${5}`);
                    setAverage(res.data);
            } catch (error) {
                console.log('Erro:', error);
            }
        };

        fetchInvoices();
    }, []);

    useEffect(() => {
        const fetchInvoices = async () => {
            try {
                    const res = await axios.get(`http://localhost:8000/get-user-most-expensive-invoice/${5}`);
                    setExpensive(res.data);
            } catch (error) {
                console.log('Erro:', error);
            }
        };

        fetchInvoices();
    }, []);

    useEffect(() => {
        const fetchInvoices = async () => {
            try {
                    const res = await axios.get(`http://localhost:8000/get-user-cheapest-invoice/${5}`);
                    setCheapest(res.data);
            } catch (error) {
                console.log('Erro:', error);
            }
        };

        fetchInvoices();
    }, []);

    return (
        <div>
            <div className="p-10">
                
                <h1 className="text-3xl font-bold">Suas compras</h1>  
                <div className="flex gap-4 py-5">
                    <div className="bg-black text-white border rounded shadow p-5 flex flex-col items-center gap-2 w-64">
                        <h2 className="text-lg">Valor médio das compras</h2>
                        <p className="font-bold text-xl">R$ {average}</p>
                    </div>
                    <div className="bg-black text-white border rounded shadow p-5 flex flex-col items-center gap-2 w-64">
                        <h2 className="text-lg">Compra mais cara</h2>
                        <p className="font-bold text-xl">R$ {expensive?.valor}</p>
                    </div>
                    <div className="bg-black text-white border rounded shadow p-5 flex flex-col items-center gap-2 w-64">
                        <h2 className="text-lg">Compra mais barata</h2>
                        <p className="font-bold text-xl">R$ {cheapest?.valor}</p>
                    </div>
                </div>
                <div>
                    {/* eslint-disable-next-line @typescript-eslint/no-explicit-any */}
                    {invoices.map((invoice: any) => {
                        return(
                            <div className="rounded shadow p-2 my-2" key={invoice.id}>
                               <h2 className="font-bold">Compra de {formatDate(invoice.data_venda)}</h2> 
                               <p className="text-sm text-gray-500">Código: {invoice.codigo}</p>
                               <p className="font-bold text-xl my-2">R${invoice.valor}</p>
                               <p>Status:{" "}
                                    <span 
                                        className={`font-bold ${invoice.status === ("Em separação" || "pendente") && "text-yellow-500"}
                                        ${invoice.status === ("Enviado") && "text-green-500"}
                                        ${invoice.status === ("Cancelado") && "text-red-500"}
                                        `}
                                    > 
                                        {invoice.status}
                                    </span>
                               </p>
                            </div>
                        )
                    })}
                </div>
            </div>
            
        </div>
    )
}

export default Invoices
