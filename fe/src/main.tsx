import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.tsx'
import { Auth0Provider } from '@auth0/auth0-react';

const domain = process.env.AUTH0_DOMAIN
const clientId = process.env.AUTH0_CLIENT_ID
if (!domain) throw new Error("auth0 domain not set")
if (!clientId) throw new Error("auth0 client id not set")

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <Auth0Provider
      domain={domain}
      clientId={clientId}
      authorizationParams={{
        redirect_uri: window.location.origin,
      }}
    >
      <App />
    </Auth0Provider>
  </StrictMode>,
)
