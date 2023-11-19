export interface Product {
    id?: number
    nome: string;
    tipo: string;
    preco: number;
    SKU: string;
    is_del?: boolean;
    fk_Usuario_vendedor_fk: number;
}
