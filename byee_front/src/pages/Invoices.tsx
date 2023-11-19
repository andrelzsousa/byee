
import axios from "axios"
import { useEffect, useState } from "react"
import PageNav from "../components/PageNav";

function formatDate(dateStr: string): string {
    const parts = dateStr.split('-');
    return parts[2] + '/' + parts[1] + '/' + parts[0];
}
function Invoices() {
    const [invoices, setInvoices] = useState([]);

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

    console.log(invoices);

    return (
        <div>
            <PageNav />
            <div className="p-10">
                <h1 className="text-3xl font-bold mb-4">Suas compras</h1>  
                <div>
                    {/* eslint-disable-next-line @typescript-eslint/no-explicit-any */}
                    {invoices.map((invoice: any) => {
                        return(
                            <div className="rounded shadow p-2 my-2">
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
