import { Link } from 'react-router-dom'

function PageNav() {
    return (
        <nav className="w-full h-28 bg-black flex text-white py-5 px-20 items-center gap-10">
            <h1 className="font-bold text-5xl">Byee</h1>
            <ul className="flex items-center gap-4 pt-3">
                <li className="hover:text-gray-300 cursor-pointer"><Link to='/'>Home</Link></li>
                <li className="hover:text-gray-300 cursor-pointer"><Link to='/products'>Produtos</Link></li>
                <li className="hover:text-gray-300 cursor-pointer"><Link to='/users'>Usuários</Link></li>
                <li className="hover:text-gray-300 cursor-pointer"><Link to='/create-product'>Criar produto</Link></li>
            </ul>
        </nav>
    )
}

export default PageNav
