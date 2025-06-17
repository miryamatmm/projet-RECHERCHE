import {internshipGateway} from "../adapters"
import { useState, useEffect } from "react";
import { useAuth } from "../providers/Auth";
import { useNavigate } from "react-router-dom";

// This component allows the user to select a supervisor from a list.
const SupervisorSelect = () => {
  const { setUser } = useAuth(); 
  const [selectedSupervisor, setSelectedSupervisor] = useState(null);
  const navigate = useNavigate();

  const [supervisors, setSupervisors] = useState([]);

  // Fetch supervisors when the component is first rendered
  useEffect(() => {
    (async() => {
      let supervisors = await internshipGateway.supervisors()
      setSupervisors(supervisors)

    })
    ()
  }, []);

  return (
    <center>
      <br/>
      <br/>
      <br/>
      <p><i>Choose a user for demonstration purpose. todo: integrate Arqus login API</i></p>
      <br/>
      <br/>
      <form onSubmit={(e) => {
          e.preventDefault(); // Prevent default form submission
          if (selectedSupervisor) {
            setUser(selectedSupervisor); // Set selected supervisor in AuthProvider
            navigate('/')
          }
        }}>
        <select className="border-2 border-golden px-3 py-2 rounded outline-none focus:outline-none" onChange={(e) => setSelectedSupervisor(JSON.parse(e.target.value))}>
          <option key="999">---</option>
          {supervisors.length
            ? supervisors.map((s) =>          
              <option key={s.id} value={JSON.stringify(s)}>{s.firstname} | {s.email} | {s.university.name}</option>)
            : 
              <option>Loading...</option>}
        </select>
        <br/>
        <br/>
        <input className="rounded bg-golden px-4 text-white outline-none focus:outline-none py-2 h-full flex items-center cursor-pointer" type="submit" value="Login" />
      </form>
    </center>
  );
};

export default SupervisorSelect;
