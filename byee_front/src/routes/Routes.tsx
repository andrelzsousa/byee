import { BrowserRouter, Routes, Route } from "react-router-dom"

import Home from "../pages/Home"
import CreateProduct from "../pages/CreateProduct"
import Users from "../pages/Users"
import Products from "../pages/Products"
import Invoices from "../pages/Invoices"

export default function AppRoutes() {
	return (
		<BrowserRouter>
			<Routes>
				<Route path="/" element={<Home />} />
				<Route path="/products" element={<Products />} />
                <Route path="/create-product" element={<CreateProduct />} />
                <Route path="/users" element={<Users />} />
                <Route path="/invoices" element={<Invoices />} />
			</Routes>
		</BrowserRouter>
	)
}