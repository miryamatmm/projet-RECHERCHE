import { Internship } from '../../types';
import '../../App.css';
import { useAuth } from '../../providers/Auth';
import {internshipGateway} from "../../adapters"


type InternshipCardProps = {
  internship: Internship, 
  onDelete, 
  isMainPage 
}

// This form displays the details of an internship
const InternshipCard = (props: InternshipCardProps) => {
  const offer = props.internship; 
  const {user} = useAuth(); 

  return (
    <div className="sm:w-1/2 p-2 mt-3 border-l-4 border-golden p-3">
      <div className='flex justify-between'>
        <h1 className="title">{ offer.title }</h1>
        {
          !props.isMainPage
          &&
          user && user.id == offer.supervisor.id
          &&
          <button 
          className='px-3 py-1 outline-none focus:outline-none' 
          style={{borderColor: 'transparent', height: "40px", width:"40px"}} 
          onClick={async() => { 
            await internshipGateway.delete(offer.id); props.onDelete(offer.id)

          }} >&times;</button>
        }
      </div>

      <h2>Dates: {offer.start} to {offer.end ?? 'permanent'}</h2>
      <br/>
      <h3>{offer.summary}</h3>
      <strong><u>Posted by:</u></strong><i> {offer.supervisor.firstname} {offer.supervisor.lastname} ({offer.supervisor.email})</i><br/>
      <strong><u>Keywords:</u></strong><i> {offer.keywords.map((e) => e.name).join(", ")}</i> <br/>
      <strong><u>Disciplines:</u></strong><i> {offer.disciplines.map((e) => e.discipline.name).join(", ")}</i>
      <br/>
      <div className="internships_box text-right sm:me-5">
        <a href={offer.pdf_path} target="_blank">
          DOWNLOAD OFFER
        </a>
      </div>
    </div>  
  )
}

export default InternshipCard;
