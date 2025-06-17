import { useState } from "react";
import {internshipGateway} from "../../adapters"

type UniversitySelectorProps = {
  onSelectuniv: (univ: string) => void;
};

// This component provides a dropdown list of universities fetched from the API. 
const UniversitySelector = ({ onSelectuniv }: UniversitySelectorProps) => {
  const [selecteduniv, setSelecteduniv] = useState(-1); 
  const [univs, setUnivs] = useState([])

  // Load the universities data from the API when the component is first rendered
  useState(async() => {
    setUnivs(await internshipGateway.universities())
  })

   // Store the selected university ID and notify the parent component of the selection
  const handleChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    const univ = e.target.value;
    setSelecteduniv(parseInt(univ));
    onSelectuniv(univ);
  };

  return (
    <div className="border-2 border-golden rounded h-full">
      <select id="univSelect" className="border-none pe-3 py-2 rounded outline-none focus:outline-none" value={selecteduniv} onChange={handleChange}>
        <option key={-1} value={-1}>University</option>
        {univs.map((univ) => (
          <option key={univ.id} value={univ.id}>
            {univ.name}
          </option>
        ))}
      </select>
    </div>
  );
};

export default UniversitySelector;
