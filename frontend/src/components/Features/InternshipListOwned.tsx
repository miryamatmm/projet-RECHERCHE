import { Internship } from "../../types";
import InternshipCard from "./InternshipCard";
import { internshipGateway } from "../../adapters"
import { useState, useEffect } from "react";
import { useAuth } from "../../providers/Auth";

// This component displays the list of internships owned by the currently logged-in user.
function InternshipListOwned() {
  const [internships, setInternships] = useState<Internship[]>([]);
  const [loading, setLoading] = useState(true);
  const {user} = useAuth();

  // Fetch the internships posted by the current user
  useEffect(() => {
    const fetchData = async () => {
      try {
        setInternships(await internshipGateway.posted_by(user.id));
      } catch (error) {
        console.error("Erreur lors du fetch des stages :", error);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  // Remove the internship from the list when deleted
  const handleDelete = (id: number) => { 
    setInternships(internships.filter((internship) => internship.id !== id));
  };

  // Display loading message while fetching internships
  if (loading) {
    return <p>Chargement des stages...</p>;
  }

  return (
    <div className="flex flex-wrap w-[90%] mx-auto">
      {internships.map((internship) => (
        <InternshipCard key={internship.id} internship={internship} onDelete={handleDelete} isMainPage={false}/>
      ))}
    </div>
  );
}

export default InternshipListOwned;
