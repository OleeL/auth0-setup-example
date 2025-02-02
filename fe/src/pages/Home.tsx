import { useNavigate } from "react-router-dom";
import "../App.css";
import { useAuth0 } from "@auth0/auth0-react";

const Home = () => {
  const { isAuthenticated, loginWithRedirect, logout, user, isLoading } =
    useAuth0();

  const navigate = useNavigate();

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
            <button onClick={() => navigate("/profile")}>Profile</button>
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
};

export default Home;
