import { useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../providers/Auth"

// This component is responsible for logging the user out of the application.
const Logout = () => {
    const { setUser } = useAuth();
    const navigate = useNavigate();

    useEffect(() => {
        setUser(null); // Set the user to null to log out
        navigate("/"); // Redirect the user to the homepage after logging out
    }, [navigate]);

    return null; 
};

export default Logout;
