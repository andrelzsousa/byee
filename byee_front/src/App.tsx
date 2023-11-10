import AppRoutes from "./routes/Routes"
import {	
	QueryClient,
	QueryClientProvider,
  } from 'react-query'

export default function App() {
	const queryClient = new QueryClient()

	return<QueryClientProvider client={queryClient}> <AppRoutes /></QueryClientProvider>
}
