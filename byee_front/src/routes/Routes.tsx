import { BrowserRouter, Routes, Route } from "react-router-dom"

import Home from "../pages/Home"
import CreateProduct from "../pages/CreateProduct"
import Users from "../pages/Users"
import Products from "../pages/Products"
import Invoices from "../pages/Invoices"
import RoleSelect from "../pages/RoleSelect"
import { useState } from "react"
import PageNav from "../components/PageNav"
import PublicWrapper from "../components/PublicWrapper"
import AdminWrapper from "../components/AdminWrapper"

export default function AppRoutes() {

	const [role, setRole] = useState("")
	

	return (
		<BrowserRouter>
		<PageNav role={role} setRole={setRole}/>
			<Routes>
				<Route path="/" element={<RoleSelect role={role} setRole={setRole} />} />
				<Route path="/home" element={<PublicWrapper role={role}><Home /></PublicWrapper>} />
                <Route path="/invoices" element={<PublicWrapper role={role}><Invoices /></PublicWrapper>} />
				<Route path="/products" element={<AdminWrapper role={role}><Products /></AdminWrapper>} />
                <Route path="/create-product" element={<AdminWrapper role={role}><CreateProduct /></AdminWrapper>} />
                <Route path="/users" element={<AdminWrapper role={role}><Users /></AdminWrapper>} />
			</Routes>
		</BrowserRouter>
	)
}