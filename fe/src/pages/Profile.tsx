import { useAuth0 } from "@auth0/auth0-react";
import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import config from "../config";

const { apiUri } = config;

const Profile = () => {
  const { user, getAccessTokenSilently, logout } = useAuth0();
  const navigate = useNavigate();
  const [protectedData, setProtectedData] = useState<null | {
    secret_image: string;
    message: string;
  }>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const getProtectedData = async () => {
      try {
        const token = await getAccessTokenSilently();
        const response = await fetch(apiUri + "/protected", {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });

        if (!response.ok) {
          throw new Error(`Error: ${response.status} - ${response.statusText}`);
        }

        const responseData = await response.json();
        setProtectedData(responseData);
      } catch (e) {
        console.error(e);
        setError("Unable to contact api");
      } finally {
        setLoading(false);
      }
    };
    getProtectedData();
  }, [getAccessTokenSilently]);

  return (
    <div>
      <button onClick={() => navigate("/")}>Back to home</button>
      <h1>Profile Page</h1>
      {user && (
        <div>
          <p>Name: {user.name}</p>
          <p>Email: {user.email}</p>
          <button
            onClick={() =>
              logout({ logoutParams: { returnTo: window.location.origin } })
            }
          >
            Log Out
          </button>

          {loading && <p>Loading protected data...</p>}
          {error && <p style={{ color: "red" }}>Error: {error}</p>}
          {protectedData && (
            <div>
              <p>
                Protected Data message from api:{" "}
                <code>{protectedData.message}</code>
              </p>
              {protectedData.secret_image && (
                <img
                  src={`data:image/jpeg;base64,${protectedData.secret_image}`}
                  alt="Secret"
                  style={{ maxWidth: "100%" }}
                />
              )}
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default Profile;
