import { Internship, Supervisor, University, Discipline, InternshipAutoExtract, SearchResults, SearchParams } from "../types"

export type InternshipGateway = {
    search: (params: SearchParams) => Promise<SearchResults>
    posted_by: (id) => Promise<Internship[]>
    universities: () => Promise<University[]>
    supervisors: () => Promise<Supervisor[]>
    disciplines: () => Promise<Discipline[]>
    extract:(formData) => Promise<InternshipAutoExtract>
    upload:(formData) => Promise<void>
    delete: (id) => Promise<void>

}

import {gateway} from "./Implementations/DatabaseInternshipGateway"
//import InMemWay from "./Implementations/InMemoryinternshipGateway"


export const internshipGateway: InternshipGateway = gateway