import { BrowserRouter, Routes, Route } from "react-router-dom"

import Home from "../pages/Home"
import CreateProduct from "../pages/CreateProduct"
import Users from "../pages/Users"
import Products from "../pages/Products"
import Invoices from "../pages/Invoices"
import RoleSelect from "../pages/RoleSelect"
import PageNav from "../components/PageNav"
import PublicWrapper from "../components/PublicWrapper"
import AdminWrapper from "../components/AdminWrapper"

export default function AppRoutes() {
	

	return (
		<BrowserRouter>
		<PageNav/>
			<Routes>
				<Route path="/" element={<RoleSelect />} />
				<Route path="/home" element={<PublicWrapper><Home /></PublicWrapper>} />
                <Route path="/invoices" element={<PublicWrapper><Invoices /></PublicWrapper>} />
				<Route path="/products" element={<AdminWrapper><Products /></AdminWrapper>} />
                <Route path="/create-product" element={<AdminWrapper><CreateProduct /></AdminWrapper>} />
                <Route path="/users" element={<AdminWrapper><Users /></AdminWrapper>} />
			</Routes>
		</BrowserRouter>
	)
}