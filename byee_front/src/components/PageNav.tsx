import { Link, useLocation, useNavigate } from 'react-router-dom'

// eslint-disable-next-line @typescript-eslint/no-explicit-any
function PageNav() {

    const location = useLocation();
    const navigate = useNavigate();
    const showHeader = location.pathname !== '/';
    const role = localStorage.getItem("role")
    
    return (showHeader &&
        <nav className="w-full h-28 bg-black flex text-white py-5 px-20 items-center justify-between">
            <div className='flex items-center gap-10'>
                <h1 className="font-bold text-5xl">Byee</h1>
                <ul className="flex items-center gap-4 pt-3">
                    {role === "comprador" &&
                        <>
                            <li className="hover:text-gray-300 cursor-pointer"><Link to='/home'>Home</Link></li>
                            <li className="hover:text-gray-300 cursor-pointer"><Link to='/invoices'>Compras</Link></li>
                        </>
                    }
                    {role === "admin" &&
                        <>
                            <li className="hover:text-gray-300 cursor-pointer"><Link to='/products'>Produtos</Link></li>
                            <li className="hover:text-gray-300 cursor-pointer"><Link to='/users'>Usuários</Link></li>
                            <li className="hover:text-gray-300 cursor-pointer"><Link to='/create-product'>Criar produto</Link></li>
                        </>
                    }
                </ul>
            </div>
            <p className='pt-3 cursor-pointer hover:text-gray-300' 
            onClick={() => {
                navigate('/')
                localStorage.setItem("role", "")
            }}>Sair</p>
        </nav>
    )
}

export default PageNav
