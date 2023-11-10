import { BrowserRouter, Routes, Route } from "react-router-dom"

import Home from "../pages/Home"
import CreateProduct from "../pages/CreateProduct"
import Users from "../pages/Users"

export default function AppRoutes() {
	return (
		<BrowserRouter>
			<Routes>
				<Route path="/" element={<Home />} />
                <Route path="/create-product" element={<CreateProduct />} />
                <Route path="/users" element={<Users />} />
			</Routes>
		</BrowserRouter>
	)
}