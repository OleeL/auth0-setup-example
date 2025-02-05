import "./App.css";
import { useAuth0 } from "@auth0/auth0-react";

function App() {
  const { isAuthenticated, loginWithRedirect, logout, user, isLoading, error } =
    useAuth0();

  if (error) {
    console.error({ ...error });
  }

  console.log({ user, origin: window.location.origin });

  if (isLoading) {
    return <div>Loading...</div>;
  }

  return (
    <div className="App">
      <header className="App-header">
        <h1>Auth0 Login Example</h1>

        {!isAuthenticated ? (
          <button onClick={() => loginWithRedirect()}>Log In</button>
        ) : (
          <>
            <div>
              <h2>Welcome, {user?.name}!</h2>
              <p>Email: {user?.email}</p>
            </div>
            <button
              onClick={() =>
                logout({ logoutParams: { returnTo: window.location.origin } })
              }
            >
              Log Out
            </button>
          </>
        )}
      </header>
    </div>
  );
}

export default App;
