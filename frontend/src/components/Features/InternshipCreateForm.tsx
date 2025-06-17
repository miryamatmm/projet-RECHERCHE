import FileInput from '../UI/Inputs/FileInput';
import PeriodInput from '../UI/Inputs/PeriodInput';
import TextInput from '../UI/Inputs/TextInput';
import TextArea from '../UI/Inputs/TextArea';
import MultiSelect from '../UI/Inputs/MultiSelect';
import Loader from "../UI/Loader"
import React, { useEffect, useState } from 'react';
import {internshipGateway} from "../../adapters"
import { useAuth } from "../../providers/Auth";
import { buildHierarchy } from '../../utils';
import { useNavigate } from 'react-router-dom';

// This form handles the creation of a new internship by collecting user's input
function Form() {
    const navigate = useNavigate()
    const {user} = useAuth();
    const [loading, setLoadingValue] = useState(false) 

    const [titleValue, setTitleValue] = useState(""); 
    const [summaryValue, setsummaryValue] = useState("");
    const [periodValue, setPeriodValue] = useState([null, null]); 
    const [selectedOptions, setSelectedOptions] = useState([]); 
    const [options, setOptions] = useState([]); 

    const [keywordsValue, setKeywords] = useState(""); 
    const [file, setFile] = useState(null) 

    // Load the available disciplines when the component is initialized
    useEffect(() => {
      const fetchData = async () => {
        const disciplines = await internshipGateway.disciplines();
        const h = buildHierarchy(disciplines)
        setOptions(h);
      };
  
      fetchData();
    }, []);

    // Handle the file change (PDF upload)
    const handleFileChange = async (event: React.ChangeEvent<HTMLInputElement>) => {
      const selectedFile = event.target.files?.[0];
      if (selectedFile && selectedFile.type === "application/pdf") {
        setFile(selectedFile);
        const formData = new FormData();
        formData.append("file", selectedFile);
        
        try {
          setLoadingValue(true)
          const response = await internshipGateway.extract(formData)
          setLoadingValue(false)
          setTitleValue(response.title)
          setsummaryValue(response.summary)
          setPeriodValue([new Date(response.start), response.end ? new Date(response.end) : null ]);
          const selected = options.filter(option => response.disciplines.includes(option.id));
          setSelectedOptions(selected);
          setKeywords(response.keywords.join(", "))
        } catch (error) {
          console.error("Erreur:", error);
          alert("Une erreur s'est produite lors de l'extraction du PDF.");
        }
      } else {
        alert("Veuillez sélectionner un fichier PDF.");
      }
    };
  
    return (
      <form onSubmit={(e) => {
        e.preventDefault();

        (async() => 
        {
          let formData = new FormData();
          formData.append("file", file)

          formData.append("title", titleValue)
          formData.append("summary", summaryValue)
          formData.append("start", periodValue[0].toISOString())
          if (periodValue[1]) {
            formData.append("end", periodValue[1].toISOString())
          }
          formData.append("supervisor_id", user.id)
          formData.append("keywords", keywordsValue)
          formData.append("disciplines", selectedOptions.map(option => option.id).join(","))
          
          try {
            await internshipGateway.upload(formData)
           
            
            alert("Données envoyées avec succès");
            navigate("/")
          } catch (error) {
            console.error("Erreur:", error);
            alert("Une erreur s'est produite lors de l'envoi du formulaire.");
          }
        })()
    
      }}>
        <div className='w-full mt-5'>
          <div className='flex mx-auto justify-center items-center gap-3 flex-col'>
            <div className="block mb-2">
              <FileInput handleFileChange={handleFileChange} label="Add PDF"/>
              {loading && 
                <Loader />
              }
            </div>
            <div className="w-full flex flex-col items-center mb-2">
              <center><h2>Title</h2></center>
              <TextInput value={titleValue} onChange={setTitleValue} placeholder="Internship title..." /> 
            </div>
            <div className="w-full flex flex-col items-center mb-2">
              <center><h2>Period</h2></center>
              <PeriodInput range={periodValue} setRange={setPeriodValue} />
            </div>
            <div className="w-full flex flex-col items-center mb-2">
              <center><h2>Keywords</h2></center>
              <TextInput value={keywordsValue} onChange={setKeywords} placeholder="Keyword1, keyword2, keyword3..." /> 
            </div>
            <div className="w-full flex flex-col items-center mb-2">
              <center><h2>Scientific disciplines</h2></center>
              <MultiSelect options={options} setOptions={setOptions} setSelectedOptions={setSelectedOptions} selectedOptions={selectedOptions} />
            </div>
  
            <div className="w-full flex flex-col items-center">
              <center><h2>Summary</h2></center>
              <TextArea value={summaryValue} onChange={setsummaryValue} placeholder="Internship summary..." /> 
            </div>
            <div className="block">
              <input type="submit" value="Add" className={'rounded bg-golden px-4 text-white outline-none focus:outline-none py-2 h-full flex items-center cursor-pointer'}
              />
            </div>
          </div>
        </div>
      </form>
    );
}

export default Form;