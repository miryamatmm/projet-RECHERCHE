import { Internship, Supervisor, University, Discipline, InternshipAutoExtract, SearchResults, SearchParams, emptySearchPparams } from '../../types';
import { InternshipGateway } from '../index';



export const gateway: InternshipGateway = {
    search: async (params: SearchParams) => {
        return {
            data: [
                 {
                    "title": "Research Intern in Biology at UCBL",
                    "summary": "Université Claude Bernard Lyon 1, a member of the Arqus European University Alliance, is seeking a motivated research intern in biology to assist in ongoing research projects related to molecular biology, ecology, and microbiology, offering hands-on experience in an international academic environment.",
                    "end": "2026-01-02",
                    "supervisor_id": 2,
                    "id": 2,
                    "start": "2025-01-09",
                    "pdf_path": "37da0430-9a13-4878-8bfd-19b7da638271.pdf",
                    "keywords": [
                        {
                            "name": " Laboratory",
                            "internship_id": 2,
                            "id": 14
                        },
                    ],
                    "supervisor": {
                        "id": 2,
                        "role": "internship_manager",
                        "university_id": 1,
                        "lastname": "Johnson",
                        "firstname": "Bob",
                        "email": "bob.johnson@test.edu",
                        "university": {
                            "country": "France",
                            "name": "Université Claude Bernard Lyon 1",
                            "id": 1,
                            "website": "https://www.univ-lyon1.fr/"
                        }
                    },
                    "disciplines": [
                        {
                            "internship_id": 2,
                            "discipline_id": 4,
                            "discipline": {
                                "id": 4,
                                "name": "Microbiology",
                                "parent_id": 1
                            }
                        },
                    ]
                }
            ],
            total: 1,
            page: 1,
            page_size: 10,
            total_pages: 1
        } as SearchResults;
    },
    universities: async () => {
        return [
            { 
                id: 0,
                name: "UCBL",
                website: "ucbl.fr",
                country: "France"
            }
          ] as University[];
    },
    supervisors: async () => {
        return [
            { 
                id: 0,
                firstname: "John",
                lastname: "Doe",
                role: "internship_manager",
                university_id: 0,
                university: await gateway.universities()[0],
                email: "john@ucbl.fr"
            }
          ] as Supervisor[];
    },
    disciplines: async() => {
        return [
            {
                id: 0,
                name: "Biology",
                parent_id: null
            }
        ] as Discipline[];
    },
    upload: async(formData) => {
    },
    extract: async(formData) => {
        return {
            title: 'Microbiology Internship',
            summary: 'Microbiology Internship at UCBL. Labs expiriments for a Master Thesis on proteins DNA.',
            start: '2025-01-01',
            end: '2026-02-01',
            pdf_path: '1.pdf',
            disciplines: [await gateway.disciplines()[0]],
            keywords: ['Labs', 'Experiments']
        } as InternshipAutoExtract
    },

    posted_by: async (id) => {
        return (await gateway.search(emptySearchPparams)).data as Internship[];
    },

    delete: async (id) => {
    },
}

